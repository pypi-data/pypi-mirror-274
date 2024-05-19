from .utils import nlp_utils

from .analysis import basic_analysis
from .analysis import diff_analysis
from .analysis import pos_analysis
from .analysis import readability_analysis
from .analysis import similarity_analysis
from .analysis import vdb_analysis


def analyze_text(text):
    text = text.strip()
    text = text.replace("\r\n", " ")
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("\t", " ")
    text = " ".join(text.split())

    nlp = nlp_utils.get_model()
    text_processed = nlp(text)

    # open("output.html", "w").write(spacy.displacy.render(text_processed.sents, style="dep", page=True))

    overall = basic_analysis.do_basic_analysis(text_processed)
    pos, verbs = pos_analysis.do_pos_analysis(text_processed)
    readability = readability_analysis.do_readability_analysis(overall, pos)
    vdb = vdb_analysis.do_vdb_analysis(overall["lemmas"])

    data = {
        "overall": overall,
        "readability": readability,
        "pos": pos,
        "verbs": verbs,
        "vdb": vdb
    }

    stats = {
        "overall": {k: len(v) for k, v in overall.items()},
        "readability": readability,
        "pos": {k: len(v) for k, v in pos.items()},
        "pos_percentage": {k: len(v) / len(overall["tokens_all"]) * 100 for k, v in pos.items()},
        "verbs": {k: len(v) for k, v in verbs.items()},
        "verbs_percentage": {k: len(v) / len(pos["verbs"]) * 100 for k, v in verbs.items()},
        "vdb": {k: len(v) for k, v in vdb.items()},
        "vdb_percentage": {k: len(v) / len(overall["lemmas"]) * 100 for k, v in vdb.items()}
    }
    return {
        'data': data,
        'stats': stats
    }


def compare(ref_text, simplified_text):
    ref_analyzed = analyze_text(ref_text)
    simplified_analyzed = analyze_text(simplified_text)

    similarity = similarity_analysis.do_similarity_analysis(ref_text, simplified_text)
    token_diff = diff_analysis.do_token_diff_analysis(ref_analyzed['data']["overall"], simplified_analyzed['data']["overall"])
    char_diff = diff_analysis.do_char_diff_analysis(ref_analyzed['data']["overall"], simplified_analyzed['data']["overall"])

    comparison_data = {
        "similarity": similarity,
        "token_diff": token_diff,
        "char_diff": char_diff
    }

    comparison_stats = {
        "similarity": similarity,
        "char_diff": char_diff,
        "token_diff": {k: len(v) for k, v in token_diff.items()},
        "char_diff_saled": {k: v / len(ref_analyzed['data']["overall"]["chars"]) * 100 for k, v in char_diff.items()},
        "token_diff_scaled": {k: len(v) / len(ref_analyzed['data']["overall"]["tokens"]) * 100 for k, v in token_diff.items()},
    }

    comparison = {
        'data': comparison_data,
        'stats': comparison_stats
    }

    return ref_analyzed, simplified_analyzed, comparison
