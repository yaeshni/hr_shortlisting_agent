from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def convert_to_text(data):

    if isinstance(data, dict):

        text = ""

        for key, value in data.items():

            text += f"{key}: {value}\n"

        return text

    return str(data)


def calculate_similarity(

    jd_data,

    candidate_data

):

    jd_text = convert_to_text(
        jd_data
    )

    candidate_text = convert_to_text(
        candidate_data
    )

    jd_embedding = model.encode(
        jd_text
    )

    candidate_embedding = model.encode(
        candidate_text
    )

    similarity = cosine_similarity(

        [jd_embedding],

        [candidate_embedding]
    )[0][0]

    return float(

    round(
        similarity * 100,
        2
    )
)