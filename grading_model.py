#بسم الله الرحمن الرحيم

from sentence_transformers import SentenceTransformer, util
import json, os

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def score_paragraph(reference_answer, student_answer):

    ref_emb = model.encode(reference_answer, convert_to_tensor=True)
    stu_emb = model.encode(student_answer, convert_to_tensor=True)

    similarity = util.cos_sim(ref_emb, stu_emb).item() # بيحط الخرج في دالة مبين 1و-1
    similarity = max(0, similarity) #علشان الغي السالب
    score = similarity * 100 #بيحولها لنسبة مئوية

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
            
            raw_points = points * (similarity_score / 100) #بيحسب الدرجة 
            earned = round(raw_points) # بيقرب الدرجة لاقرب عدد صحيح

        else:
            earned = 0 #لو السؤال مش فقرة هيتم تجاهله

        results[q_id] = round(earned, 2)
        total += earned

    return results, round(total, 2), max_total

def load_exam_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    

def load_student_file(path): 
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    

def save_results(student_name, results, total, max_total):
    output_data = {
        "student": student_name,
        "scores": results,
        "total": total,
        "max_total": max_total
    }

    os.makedirs("results", exist_ok=True)
    path = f"data/results/{student_name}_results.json"

    with open(path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"Saved results to {path}")
    
if __name__ == "__main__":

    exam_data = load_exam_file("data/exams/exam.json")
    
    STUDENT_FOLDER = "data/students/"

    for filename in os.listdir(STUDENT_FOLDER):
        if filename.endswith(".json"):
            student_name = filename.replace(".json", "")
            file_path = os.path.join(STUDENT_FOLDER, filename)

            print(f"\n Scoring student: {student_name}")

            student_data = load_student_file(file_path)

            results, total, max_total = grade_exam(exam_data, student_data)

            save_results(student_name, results, total, max_total)

            print(f"→ Total score for {student_name}: {total} / {max_total}")