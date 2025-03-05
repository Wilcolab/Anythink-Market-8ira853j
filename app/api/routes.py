from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from pydantic import BaseModel
from app.auth.jwt import get_current_user, User
from app.database.db_manager import (
    get_client_data, get_account_balance,
    get_recent_transactions
)
from app.models.llm_service import LLMService
import re

router = APIRouter()
llm_service = LLMService()


class QueryRequest(BaseModel):
    query: str


class QueryResponse(BaseModel):
    response: str


@router.post("/secure-query", response_model=QueryResponse)
async def secure_query(
    request: QueryRequest,
    current_user: User = Depends(get_current_user)
):
    pattern = r'(?i)(select|update|delete|insert|drop|alter)'
    query = re.sub(pattern, "", request.query)

    intent_tag = llm_service.interpret_user_intent(query)

    context = await get_context_for_intent(intent_tag, current_user.username)

    response = llm_service.generate_response(query, context)

    return QueryResponse(response=response)


async def get_context_for_intent(intent_tag: str, username: str) -> str:
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if intent_tag == "account_balance":
        accounts = await get_account_balance(username)
        if accounts:
            accounts_info = "\n".join(
                [f"{account['account_type'].capitalize()} account {account['account_number']}: ${account['balance']:.2f}" for account in accounts])
            return f"Account Information:\n{accounts_info}"
        return "No account information available."

    elif intent_tag in ["transaction_history", "spending_analysis"]:
        transactions = await get_recent_transactions(username)
        if transactions:
            trans_info = "\n".join(
                [f"{t['transaction_date'].split()[0]} - {t['description']} - ${t['amount']:.2f} ({t['transaction_type']})" for t in transactions])
            return f"Recent Transactions for {username}:\n{trans_info}"
        return "No recent transactions found for this user."

    else:
        data_items = await get_client_data(intent_tag) if intent_tag else []
        return "\n\n".join([item['info'] for item in data_items]) if data_items else ""
