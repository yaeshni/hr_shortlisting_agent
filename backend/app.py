from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

import os
import uuid

from services.parser import extract_text_from_file
from services.llm_extractor import extract_jd_data, extract_resume_data
from services.embeddings import calculate_similarity
from services.scorer import evaluate_candidate_with_llm


app = FastAPI()


# FIX: allow_credentials=True is incompatible with allow_origins=["*"].
# Either allow credentials with specific origins, or use wildcard without credentials.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def save_upload(upload: UploadFile, content: bytes) -> str:
    # FIX: Use uuid prefix to avoid race conditions when two uploads
    # have the same filename at the same time.
    unique_name = f"temp_{uuid.uuid4().hex}_{upload.filename}"
    with open(unique_name, "wb") as f:
        f.write(content)
    return unique_name


@app.get("/")
def home():
    return {"message": "HR Resume Shortlisting Backend Running"}


@app.post("/evaluate/")
async def evaluate_candidate(
    jd: UploadFile = File(...),
    resume: UploadFile = File(...)
):
    jd_path = None
    resume_path = None

    try:
        jd_content = await jd.read()
        resume_content = await resume.read()

        jd_path = save_upload(jd, jd_content)
        resume_path = save_upload(resume, resume_content)

        jd_text = extract_text_from_file(jd_path)
        resume_text = extract_text_from_file(resume_path)

        if not jd_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from JD file.")
        if not resume_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from resume file.")

        jd_data = extract_jd_data(jd_text)
        candidate_data = extract_resume_data(resume_text)

        similarity_score = calculate_similarity(jd_data, candidate_data)
        evaluation = evaluate_candidate_with_llm(jd_data, candidate_data, similarity_score)

        return {
            "candidate": candidate_data.get("name", "Unknown"),
            "similarity_score": similarity_score,
            "evaluation": evaluation,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        # FIX: Always clean up temp files, even if an error occurred.
        for path in [jd_path, resume_path]:
            if path and os.path.exists(path):
                os.remove(path)


@app.post("/evaluate-multiple/")
async def evaluate_multiple_candidates(
    jd: UploadFile = File(...),
    resumes: list[UploadFile] = File(...)
):
    jd_path = None
    resume_paths = []

    try:
        jd_content = await jd.read()
        jd_path = save_upload(jd, jd_content)

        jd_text = extract_text_from_file(jd_path)
        if not jd_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from JD file.")

        jd_data = extract_jd_data(jd_text)
        results = []

        for resume in resumes:
            resume_content = await resume.read()
            resume_path = save_upload(resume, resume_content)
            resume_paths.append(resume_path)

            resume_text = extract_text_from_file(resume_path)
            if not resume_text.strip():
                continue  # Skip unreadable resumes instead of crashing

            candidate_data = extract_resume_data(resume_text)
            similarity_score = calculate_similarity(jd_data, candidate_data)
            evaluation = evaluate_candidate_with_llm(jd_data, candidate_data, similarity_score)

            results.append({
                "candidate": candidate_data.get("name", "Unknown"),
                "similarity_score": similarity_score,
                "evaluation": evaluation,
            })

        ranked_results = sorted(
            results,
            key=lambda x: x["evaluation"]["total_score"],
            reverse=True
        )

        return {"ranked_candidates": ranked_results}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        for path in [jd_path] + resume_paths:
            if path and os.path.exists(path):
                os.remove(path)