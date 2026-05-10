def evaluate_candidate_with_llm(
    jd_data,
    candidate_data,
    similarity_score
):
    # FIX: JD extractor returns "required_skills", not "skills"
    required_skills = jd_data.get("required_skills", [])
    preferred_skills = jd_data.get("preferred_skills", [])
    candidate_skills = candidate_data.get("skills", [])

    candidate_skills_lower = [s.lower() for s in candidate_skills]

    matched_required = [
        skill for skill in required_skills
        if skill.lower() in candidate_skills_lower
    ]

    matched_preferred = [
        skill for skill in preferred_skills
        if skill.lower() in candidate_skills_lower
    ]

    skill_match_percentage = 0
    if len(required_skills) > 0:
        skill_match_percentage = (
            len(matched_required) / len(required_skills)
        ) * 100

    if skill_match_percentage >= 85:
        skills_score = 10
    elif skill_match_percentage >= 50:
        skills_score = 7
    elif skill_match_percentage >= 25:
        skills_score = 4
    else:
        skills_score = 2

    # FIX: Actually evaluate experience instead of hardcoding 5
    experience = candidate_data.get("experience", [])
    jd_experience_required = jd_data.get("experience_required", "")

    if len(experience) >= 3:
        experience_score = 9
    elif len(experience) == 2:
        experience_score = 7
    elif len(experience) == 1:
        experience_score = 5
    else:
        experience_score = 2

    # FIX: Actually evaluate education
    education = candidate_data.get("education", [])
    jd_education_required = jd_data.get("education_required", "")

    if len(education) >= 2:
        education_score = 9
    elif len(education) == 1:
        education_score = 7
    else:
        education_score = 4

    # FIX: Actually evaluate projects
    projects = candidate_data.get("projects", [])
    if len(projects) >= 3:
        project_score = 10
    elif len(projects) == 2:
        project_score = 7
    elif len(projects) == 1:
        project_score = 5
    else:
        project_score = 2

    # Certifications as a proxy for communication/polish
    certifications = candidate_data.get("certifications", [])
    if len(certifications) >= 2:
        communication_score = 9
    elif len(certifications) == 1:
        communication_score = 7
    else:
        communication_score = 6

    total_score = (
        skills_score      * 0.30 +
        experience_score  * 0.25 +
        education_score   * 0.15 +
        project_score     * 0.20 +
        communication_score * 0.10
    )

    return {
        "skills_match": {
            "score": skills_score,
            "matched_required": matched_required,
            "matched_preferred": matched_preferred,
            "reason": f"Matched {len(matched_required)}/{len(required_skills)} required skills."
        },
        "experience_relevance": {
            "score": experience_score,
            "reason": f"Found {len(experience)} experience entries."
        },
        "education": {
            "score": education_score,
            "reason": f"Found {len(education)} education entries."
        },
        "projects": {
            "score": project_score,
            "reason": f"Found {len(projects)} projects."
        },
        "communication": {
            "score": communication_score,
            "reason": f"Found {len(certifications)} certifications."
        },
        "total_score": round(total_score, 2)
    }