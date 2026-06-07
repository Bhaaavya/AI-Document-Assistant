from sqlalchemy.orm import Session

from app.models import DocumentChunk


def retrieve_relevant_chunks(
    db: Session,
    document_id: int,
    question: str,
    limit: int = 3
):
    words = question.lower().split()

    chunks = db.query(DocumentChunk).filter(
        DocumentChunk.document_id == document_id
    ).all()

    matched_chunks = []

    for chunk in chunks:
        chunk_text = chunk.content.lower()

        if any(word in chunk_text for word in words):
            matched_chunks.append(chunk.content)

    return matched_chunks[:limit]