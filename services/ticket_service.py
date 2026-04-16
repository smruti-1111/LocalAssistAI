from sqlalchemy.orm import Session
from database.models import Ticket
from utils.mask import mask_sensitive_data
from services.local_llm_service import analyze_text_local, generate_response_local


def create_ticket(db: Session, user_query: str):
    # Step 1: Mask sensitive data
    masked_query = mask_sensitive_data(user_query)

    # Step 2: Analyze using LLM
    llm_output = analyze_text_local(masked_query)

    sentiment = llm_output.get("sentiment", "unknown")
    summary = llm_output.get("summary", "")
    category = llm_output.get("category", "general")
    priority = llm_output.get("priority", "low")

    #  Context-aware response
    context = f"{sentiment}, priority={priority}"

    # Step 3: Generate response
    auto_reply = generate_response_local(masked_query, context)

    # Step 4: Decision logic
    escalation = priority == "high" or sentiment == "negative"

    # Step 5: Store in DB
    ticket = Ticket(
        user_query=masked_query,
        sentiment=sentiment,
        summary=summary,
        category=category,
        priority=priority,
        response=auto_reply
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    return {
        "ticket": {
            "id": ticket.id,
            "user_query": ticket.user_query,
            "sentiment": ticket.sentiment,
            "summary": ticket.summary,
            "category": ticket.category,
            "priority": ticket.priority,
            "response": ticket.response
        },
        "escalation_required": escalation
    }
