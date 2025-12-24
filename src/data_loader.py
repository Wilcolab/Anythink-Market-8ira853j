import json
from pathlib import Path
from typing import TypedDict


class Document(TypedDict):
    id: str
    title: str
    content: str
    source: str


class EvalQuestion(TypedDict):
    id: str
    question: str
    reference_answer: str
    expected_sources: list[str]
    difficulty: str


def load_documents() -> list[Document]:
    data_dir = Path(__file__).parent.parent / "data"
    documents: list[Document] = []

    with open(data_dir / "faq.json") as f:
        faq_data = json.load(f)
        for item in faq_data:
            documents.append({
                "id": item["id"],
                "title": item["title"],
                "content": item["content"],
                "source": "faq"
            })

    with open(data_dir / "escalation_notes.json") as f:
        escalation_data = json.load(f)
        for item in escalation_data:
            full_content = f"{item['scenario']} {item['resolution']}"
            if item.get("internal_notes"):
                full_content += f" Internal: {item['internal_notes']}"
            documents.append({
                "id": item["id"],
                "title": item["title"],
                "content": full_content,
                "source": "escalation"
            })

    return documents


def load_eval_questions() -> list[EvalQuestion]:
    data_dir = Path(__file__).parent.parent / "data"
    
    with open(data_dir / "eval_questions.json") as f:
        return json.load(f)

