import os
import shutil

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Document
from app.schemas import DocumentResponse
from app.auth import get_current_user

from uuid import uuid4
from app.pdf_utils import extract_text_from_pdf
from app.chunking import split_text_into_chunks
from app.models import DocumentChunk
from app.schemas import QuestionRequest, ChunkSearchResponse
from app.retrieval import retrieve_relevant_chunks

from app.gemini_service import ask_gemini
from app.models import ChatMessage

from app.schemas import DocumentResponse, QuestionRequest, ChunkSearchResponse, ChatHistoryResponse

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


UPLOAD_DIR = os.getenv("UPLOAD_DIR", "uploads")


@router.post("/upload", response_model=DocumentResponse)
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are allowed"
        )

    os.makedirs(UPLOAD_DIR, exist_ok=True)

    file_path = os.path.join(
         UPLOAD_DIR,
         file.filename

    )

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(file_path)

    new_document = Document(
        user_id=current_user.id,
        filename=file.filename,
        file_path=file_path,
        file_size=file_size,
        status="uploaded"
    )

    db.add(new_document)
    db.commit()
    db.refresh(new_document)

    text = extract_text_from_pdf(file_path)
    chunks = split_text_into_chunks(text)
    for index, chunk in enumerate(chunks):
        document_chunk = DocumentChunk(
            document_id=new_document.id,
             chunk_index=index,
             content=chunk
        )

        db.add(document_chunk)

    new_document.status = "processed"
    db.commit()
    db.refresh(new_document)

    return new_document

@router.get("/test-extract/{document_id}")
def test_extract(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.id == document_id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    text = extract_text_from_pdf(document.file_path)

    return {
        "text": text[:2000]
    }

@router.post("/{document_id}/search", response_model=ChunkSearchResponse)
def search_document_chunks(
    document_id: int,
    request: QuestionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    matched_chunks = retrieve_relevant_chunks(
        db=db,
        document_id=document_id,
        question=request.question
    )


    return {
        "document_id": document_id,
        "question": request.question,
        "matched_chunks": matched_chunks[:3]
    }

@router.post("/{document_id}/ask")
def ask_document(
    document_id: int,
    request: QuestionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    matched_chunks = retrieve_relevant_chunks(
        db=db,
        document_id=document_id,
        question=request.question
    )

    if not matched_chunks:
        raise HTTPException(
            status_code=404,
            detail="No relevant content found in document"
        )

    context = "\n\n".join(matched_chunks)

    answer = ask_gemini(
        context=context,
        question=request.question
    )

    chat = ChatMessage(
        user_id=current_user.id,
        document_id=document_id,
        question=request.question,
        answer=answer
    )

    db.add(chat)
    db.commit()

    return {
        "document_id": document_id,
        "question": request.question,
        "answer": answer
    }

    
@router.get("/", response_model=list[DocumentResponse])
def get_my_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Document).filter(
        Document.user_id == current_user.id
    ).all()


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return document


@router.get("/{document_id}/chat-history", response_model=list[ChatHistoryResponse])
def get_chat_history(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    return db.query(ChatMessage).filter(
        ChatMessage.document_id == document_id,
        ChatMessage.user_id == current_user.id
    ).all()

@router.delete("/{document_id}")
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = db.query(Document).filter(
        Document.id == document_id,
        Document.user_id == current_user.id
    ).first()

    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if os.path.exists(document.file_path):
        os.remove(document.file_path)

    db.delete(document)
    db.commit()

    return {"message": "Document deleted successfully"}