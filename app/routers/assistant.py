from hmac import new
from fastapi import APIRouter
from app.models.schema import QueryRequest, QueryResponse
from app.chains.book_rag_chain import get_rag_chain

router = APIRouter()


@router.post("/ask", response_model=QueryResponse)
def ask_book_assistant(request: QueryRequest):
    query = request.query
    print(f"Received query: {query}")

    text = get_rag_chain().invoke(query)
    res = QueryResponse(answer=text)
    return res
