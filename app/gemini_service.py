import os
import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    os.getenv("AI_MODEL")
)



def ask_gemini(context: str, question: str):

    prompt = f"""
    Answer the question ONLY using the provided context.

    Context:
    {context}

    Question:
    {question}
    """

    response = model.generate_content(
        prompt
    )

    return response.text