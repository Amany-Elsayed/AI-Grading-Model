import os
from fastapi import Header, HTTPException
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, util

app = FastAPI(title="AI Grading API")
API_KEY = os.getenv("API_KEY")

if API_KEY is None:
    raise RuntimeError("API_KEY environment variable is not set")


model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L3-v2")

def score_paragraph(reference_answer, student_answer):
    ref_emb = model.encode(reference_answer, convert_to_tensor=True)
    stu_emb = model.encode(student_answer, convert_to_tensor=True)

    similarity = util.cos_sim(ref_emb, stu_emb).item()
    similarity = max(0, similarity)
    score = similarity * 100
    return round(score, 2)


def grade_exam(questions, student_answers):
    results = {}
    total = 0
    max_total = 0

    for q_id, q_data in questions.items():
        points = q_data["points"]
        max_total += points

        if q_data["type"] == "paragraph":
            similarity_score = score_paragraph(
                q_data["answer"],
                student_answers.get(q_id, "")
            )
            earned = round(points * (similarity_score / 100))
        else:
            earned = 0

        results[q_id] = earned
        total += earned

    return results, total, max_total

#input format

class GradeRequest(BaseModel):
    exam_name: str
    student_name: str
    questions: dict
    student_answers: dict

#endpoint

@app.get("/")
def root():
    return {"status": "AI Grading API is running"}


@app.post("/grade")
def grade(
    data: GradeRequest,
    x_api_key: str = Header(None)
):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")

    results, total, max_total = grade_exam(
        data.questions,
        data.student_answers
    )

    return {
        "exam": data.exam_name,
        "student": data.student_name,
        "scores": results,
        "total": total,
        "max_total": max_total
    }

