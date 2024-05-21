from sentence_transformers import SentenceTransformer, util


class SimilarityAnalyzer:
    __model: SentenceTransformer

    semantic_similarity: float

    def __init__(self, reference_text: str, simplified_text: str):
        self.__model = SentenceTransformer('sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2')

        embeddings1 = self.__model.encode([reference_text], convert_to_numpy=True)
        embeddings2 = self.__model.encode([simplified_text], convert_to_numpy=True)
        cosine_scores = util.cos_sim(embeddings1, embeddings2)

        self.semantic_similarity = float(cosine_scores[0][0]) * 100.0


