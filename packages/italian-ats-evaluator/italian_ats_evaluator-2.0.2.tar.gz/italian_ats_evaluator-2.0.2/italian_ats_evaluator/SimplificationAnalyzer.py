from .TextAnalyzer import TextAnalyzer
from .analyzers.SimilarityAnalyzer import SimilarityAnalyzer
from .analyzers.DiffAnalyzer import DiffAnalyzer


class SimplificationAnalyzer:

    def __init__(self, reference_text: str, simplified_text: str):
        self.reference = TextAnalyzer(reference_text)
        self.simplified = TextAnalyzer(simplified_text)

        self.similarity = SimilarityAnalyzer(reference_text, simplified_text)
        self.diff = DiffAnalyzer(self.reference.basic, self.simplified.basic)
