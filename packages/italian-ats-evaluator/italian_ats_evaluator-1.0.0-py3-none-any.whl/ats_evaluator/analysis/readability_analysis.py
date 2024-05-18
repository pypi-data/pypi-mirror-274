def eval_ttr(words: int, tokens: int):
    return float(words) / tokens * 100.0


def eval_gulpease(chars: int, tokens: int, sentences: int):
    return 89 + ((300.0 * sentences) - (10.0 * chars)) / float(tokens)


def eval_flesch_vacca(syllables: int, tokens: int, sentences: int):
    return 206 - (0.65 * (syllables / tokens) * 100.0) - (1.0 * (tokens / sentences))


def eval_lexical_density(nouns: int, adverbs: int, adjectives: int, verbs: int, tokens: int):
    return (nouns + adverbs + adjectives + verbs) / tokens


def do_readability_analysis(overall: dict, pos: dict):
    return {
        "ttr": eval_ttr(len(overall["words"]), len(overall["tokens"])),
        "gulpease": eval_gulpease(len(overall["chars"]), len(overall["tokens"]), len(overall["sentences"])),
        "flesch_vacca": eval_flesch_vacca(len(overall["syllables"]), len(overall["tokens"]), len(overall["sentences"])),
        "lexical_density": eval_lexical_density(len(pos["nouns"]), len(pos["adverbs"]), len(pos["adjectives"]), len(pos["verbs"]), len(overall["tokens"]))
    }
