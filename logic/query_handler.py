# from utils.market_data import get_market_price
# from utils.voice_output import speak

# async def handle_query(query, ws):
#     if query.lower() in ["stop", "exit", "close", "बंद करो"]:
#         print("Shutting down.")
#         return

#     if "price" in query:
#         product = next((word for word in query.split() if word in ["wheat", "rice", "potato"]), None)
#         location = next((word for word in query.split() if word in ["karnataka", "up", "maharashtra"]), None)
#         if product:
#             response = get_market_price(product, location)
#             print(response)
#             speak(response)
#         else:
#             print("Couldn't understand the product.")
#     else:
#         print("Fetching from Gemini...")
#         await ws.send(json.dumps({"realtime_input": {"text": {"text": query}}}))

# from utils.market_data import get_market_price

# async def handle_query(query):
#     query_lower = query.lower()
    
#     if "price" in query_lower and any(x in query_lower for x in ["of", "for"]):
#         # Example query: "price of wheat in karnataka"
#         commodity = next((word for word in query_lower.split() if word in ["wheat", "rice", "potato"]), None)
#         state = next((word for word in query_lower.split() if word in ["karnataka", "maharashtra", "up"]), None)
#         return get_market_price(commodity, state)

#     if "scheme" in query_lower:
#         category = "farmer" if "farmer" in query_lower else None
#         state = next((word for word in query_lower.split() if word in ["karnataka", "maharashtra", "up"]), None)
#         return get_applicable_schemes(category, state)

#     return "Sorry, I didn't understand your request."

# from utils.market_data import get_market_price
# from utils.scheme_data import get_applicable_schemes  # We'll define this in a new file

# async def handle_query(query):
#     query_lower = query.lower()
    
#     # Handle market price queries
#     if "price" in query_lower and any(x in query_lower for x in ["of", "for"]):
#         commodity = next((word for word in query_lower.split() if word in ["wheat", "rice", "potato"]), None)
#         state = next((word for word in query_lower.split() if word in ["karnataka", "maharashtra", "up"]), None)
#         return get_market_price(commodity, state)

#     # Handle government schemes queries
#     if "scheme" in query_lower:
#         category = None
#         for keyword in ["farmer", "student", "entrepreneur", "woman", "disabled"]:
#             if keyword in query_lower:
#                 category = keyword
#                 break
        
#         state = next((word for word in query_lower.split() if word in ["karnataka", "maharashtra", "up"]), None)
#         results = get_applicable_schemes(category, state)

#         if results:
#             response_lines = []
#             for scheme in results[:3]:  # Limit to top 3 matches
#                 line = f"Scheme: {scheme['name']}\nDetails: {scheme['description']}\nRegister: {scheme['registration_link']}"
#                 response_lines.append(line)
#             return "\n\n".join(response_lines)
#         else:
#             return "No matching government schemes found for your category or location."

#     return "Sorry, I didn't understand your request."

import os
import json
from typing import Any, Dict, List

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.schema import Document

# ─────────── CONFIG ───────────

# Make sure you've set:
#   export OPENROUTER_API_KEY="your_openrouter_key"
# (or otherwise in your environment)
OPENROUTER_API_KEY = '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'
OPENROUTER_API_BASE = "https://openrouter.ai/api/v1"

# How many schemes to pull semantically before eligibility filtering
RETRIEVE_K = 5

# Path to your schemes file
SCHEMES_JSON_PATH = os.path.join(os.path.dirname(__file__), "data", "schemes.json")


# ─────────── LOAD & INDEX ───────────

def load_schemes() -> List[Dict[str, Any]]:
    with open(SCHEMES_JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# Build FAISS index once at import
_schemes = load_schemes()

# Wrap each scheme JSON blob as a Document
_docs = [
    Document(page_content=json.dumps(scheme), metadata={"scheme_id": scheme["scheme_id"]})
    for scheme in _schemes
]

# Use OpenRouter for embeddings
_embeddings = OpenAIEmbeddings(
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base=OPENROUTER_API_BASE,
)

_vectorstore = FAISS.from_documents(_docs, _embeddings)
_retriever = _vectorstore.as_retriever(search_kwargs={"k": RETRIEVE_K})


# ─────────── ELIGIBILITY LOGIC ───────────

def check_eligibility(user_info: Dict[str, Any], scheme: Dict[str, Any]) -> bool:
    e = scheme.get("eligibility", {})

    if "occupation" in e and e["occupation"] != user_info.get("occupation"):
        return False

    if "age" in e:
        lo, hi = map(int, e["age"].split("-"))
        age = int(user_info.get("age", 0))
        if age < lo or age > hi:
            return False

    if "state" in e and user_info.get("state") not in e["state"]:
        return False

    return True


# ─────────── RAG + LLM SETUP ───────────

_llm = OpenAI(
    model="google/gemini-2.0-flash-exp:free",
    openai_api_key=OPENROUTER_API_KEY,
    openai_api_base=OPENROUTER_API_BASE,
    temperature=0.0,
)

_qa_chain = RetrievalQA.from_chain_type(
    llm=_llm,
    chain_type="stuff",            # simple “stuff” chain
    retriever=_retriever,
    return_source_documents=False, # we don’t need the raw docs in output
)


# ─────────── QUERY HANDLER ───────────

async def handle_query(query: str, user_info: Dict[str, Any]) -> str:
    if "scheme" not in query.lower():
        return "Sorry, I didn't understand your request."

    # 1) semantically retrieve top-k
    candidate_docs = _retriever.get_relevant_documents(query)

    # 2) decode & filter by your eligibility
    eligible_jsons = []
    for doc in candidate_docs:
        scheme = json.loads(doc.page_content)
        if check_eligibility(user_info, scheme):
            eligible_jsons.append(doc.page_content)

    if not eligible_jsons:
        return "Sorry, you are not eligible for any schemes based on the provided information."

    # 3) ask Gemini to format name + registration_link
    prompt = (
        "You are given JSON objects of eligible government schemes. "
        "For each, output a bullet (–) with the scheme_name and its registration_link.\n\n"
        + "\n\n---\n\n".join(eligible_jsons)
        + "\n\nAnswer:"
    )

    answer = _llm(prompt)
    return answer.strip()
