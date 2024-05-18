from sentence_transformers import SentenceTransformer, util

sentence_transformer_model = None


def eval_similarity_similarity(ref_text: str, simplified_text: str):
    global sentence_transformer_model
    if sentence_transformer_model is None:
        sentence_transformer_model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

    embeddings1 = sentence_transformer_model.encode([ref_text], convert_to_numpy=True)
    embeddings2 = sentence_transformer_model.encode([simplified_text], convert_to_numpy=True)
    cosine_scores = util.cos_sim(embeddings1, embeddings2)
    return float(cosine_scores[0][0]) * 100.0


def do_similarity_analysis(ref_text: str, simplified_text: str):
    return {
        "similarity_similarity": eval_similarity_similarity(ref_text, simplified_text)
    }
