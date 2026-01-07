from sentence_transformers import SentenceTransformer, util
import json, os

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

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
            
            raw_points = points * (similarity_score / 100)
            earned = round(raw_points)

        else:
            earned = 0

        results[q_id] = earned
        total += earned

    return results, total, max_total

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
    

def save_results(exam_name, student_name, results, total, max_total):

    os.makedirs(f"data/results/{exam_name}", exist_ok=True)
    path = f"data/results/{exam_name}/{student_name}_results.json"

    output_data = {
        "exam": exam_name,
        "student": student_name,
        "scores": results,
        "total": total,
        "max_total": max_total
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"Saved results for {student_name} in {path}")


def process_exam(exam_file):
    exam_name = exam_file.replace(".json", "")
    exam_path = f"data/exams/{exam_file}"

    print(f"\n processing exam: {exam_name}")

    exam_data = load_json(exam_path)

    students_folder = f"data/students/{exam_name}"
    if not os.path.exists(students_folder):
        print(f"No students folder found for this exam: {students_folder}")
        return
    
    for student_file in os.listdir(students_folder):
        if student_file.endswith(".json"):
            student_name = student_file.replace(".json", "")
            student_path = os.path.join(students_folder, student_file)

            print(f"scoring student: {student_name}")

            student_answers = load_json(student_path)

            results, total, max_total = grade_exam(exam_data, student_answers)

            save_results(exam_name, student_name, results, total, max_total)

            print(f"score: {total} / {max_total}")


if __name__ == "__main__":
    exams_folder = "data/exams/"

    for exam_file in os.listdir(exams_folder):
        if exam_file.endswith(".json"):
            process_exam(exam_file)
