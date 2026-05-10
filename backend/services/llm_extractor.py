from openai import OpenAI
from dotenv import load_dotenv

import os
import json

load_dotenv()

client = OpenAI(

    api_key=os.getenv("OPENROUTER_API_KEY"),

    base_url="https://openrouter.ai/api/v1"
)


def clean_json_response(text):

    text = text.replace("```json", "")
    text = text.replace("```", "")

    return text.strip()


def ask_llm(prompt):

    completion = client.chat.completions.create(

        model="openai/gpt-4o-mini",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )

    return completion.choices[0].message.content

    return completion.choices[0].message.content


def extract_resume_data(resume_text):

    prompt = f"""
    Extract resume information.

    Return ONLY valid JSON.

    {{
        "name": "",
        "skills": [],
        "experience": [],
        "education": [],
        "projects": [],
        "certifications": []
    }}

    Resume:
    {resume_text}
    """

    response = ask_llm(prompt)

    cleaned = clean_json_response(response)

    try:

        return json.loads(cleaned)

    except json.JSONDecodeError:

        print("Resume JSON Error:")
        print(cleaned)

        return {
            "name": "Unknown",
            "skills": [],
            "experience": [],
            "education": [],
            "projects": [],
            "certifications": []
        }


def extract_jd_data(jd_text):

    prompt = f"""
    Analyze this Job Description.

    Return ONLY valid JSON.

    {{
        "role": "",
        "required_skills": [],
        "preferred_skills": [],
        "experience_required": "",
        "education_required": ""
    }}

    JD:
    {jd_text}
    """

    response = ask_llm(prompt)

    cleaned = clean_json_response(response)

    try:

        return json.loads(cleaned)

    except json.JSONDecodeError:

        print("JD JSON Error:")
        print(cleaned)

        return {
            "role": "",
            "required_skills": [],
            "preferred_skills": [],
            "experience_required": "",
            "education_required": ""
        }