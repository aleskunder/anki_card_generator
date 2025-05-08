def add_german_metadata(word, word_type):
    # Add noun and verb metadata
    if word_type == 'noun':
        return f"metadata for noun: {word}"
    elif word_type == 'verb':
        return f"metadata for verb: {word}"
    return ""
