import editdistance

from .vdb_analysis import is_vdb


def do_char_diff_analysis(ref_overall_data, simplified_overall_data):
    return {
        "editdistance": editdistance.eval(''.join(ref_overall_data['chars']).lower(), ''.join(simplified_overall_data['chars']).lower())
    }


def do_token_diff_analysis(ref_overall_data, simplified_overall_data):
    added_tokens = []
    added_vdb_tokens = []
    for token, lemma in zip(simplified_overall_data['tokens'], simplified_overall_data['lemmas']):
        if token not in ref_overall_data['tokens']:
            added_tokens.append(token)
            if is_vdb(lemma):
                added_vdb_tokens.append(token)

    deleted_tokens = []
    deleted_vdb_tokens = []
    for token, lemma in zip(ref_overall_data['tokens'], ref_overall_data['lemmas']):
        if token not in simplified_overall_data['tokens']:
            deleted_tokens.append(token)
            if is_vdb(lemma):
                deleted_vdb_tokens.append(token)

    return {
        "added_tokens": added_tokens,
        "deleted_tokens": deleted_tokens,
        "added_vdb_tokens": added_vdb_tokens,
        "deleted_vdb_tokens": deleted_vdb_tokens
    }
