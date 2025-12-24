#!/usr/bin/env python3
"""
AcmeCloud RAG Evaluation Runner

Evaluates the RAG pipeline against the internal evaluation question set.
Run with: python run_eval.py
"""
from src.data_loader import load_eval_questions
from src.rag_pipeline import answer_question, initialize


def run_evaluation():
    print("=" * 60)
    print("AcmeCloud RAG Prototype - Evaluation Run")
    print("=" * 60)
    print()

    print("Initializing RAG pipeline...")
    initialize()
    print()

    questions = load_eval_questions()
    print(f"Loaded {len(questions)} evaluation questions")
    print("-" * 60)
    print()

    results = []
    
    for i, q in enumerate(questions, 1):
        print(f"Question {i}/{len(questions)}: {q['question'][:50]}...")
        
        try:
            answer = answer_question(q["question"])
            results.append({
                "id": q["id"],
                "question": q["question"],
                "generated_answer": answer,
                "reference_answer": q["reference_answer"],
                "difficulty": q["difficulty"],
                "success": True
            })
            print(f"  ✓ Generated answer ({len(answer)} chars)")
        except Exception as e:
            results.append({
                "id": q["id"],
                "question": q["question"],
                "generated_answer": None,
                "reference_answer": q["reference_answer"],
                "difficulty": q["difficulty"],
                "success": False,
                "error": str(e)
            })
            print(f"  ✗ Error: {e}")
        
        print()

    print("=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)
    
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    
    print(f"Total questions: {len(results)}")
    print(f"Successful: {len(successful)}")
    print(f"Failed: {len(failed)}")
    print()
    
    if successful:
        print("Difficulty breakdown (successful):")
        for diff in ["easy", "medium", "hard"]:
            count = len([r for r in successful if r["difficulty"] == diff])
            total = len([r for r in results if r["difficulty"] == diff])
            print(f"  {diff}: {count}/{total}")
    
    print()
    print("-" * 60)
    print("Sample Outputs:")
    print("-" * 60)
    
    for r in successful[:3]:
        print(f"\nQ: {r['question']}")
        print(f"A: {r['generated_answer'][:200]}...")
        print(f"Reference: {r['reference_answer'][:100]}...")
    
    print()
    print("=" * 60)
    print("Evaluation complete. Review outputs above for quality assessment.")
    print("=" * 60)


if __name__ == "__main__":
    run_evaluation()

