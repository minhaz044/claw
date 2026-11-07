from dotenv import load_dotenv

load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

GOOGLE_LLM_MODEL_NAME = "gemini-3.5-flash-lite"
OPEN_AI_LLM_LUNA_MODEL_NAME = "gpt-6-luna"

_gemini_llm = ChatGoogleGenerativeAI(model=GOOGLE_LLM_MODEL_NAME)
_luna_llm = ChatOpenAI(model=OPEN_AI_LLM_LUNA_MODEL_NAME)

llm = _luna_llm
