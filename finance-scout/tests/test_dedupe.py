from app.nlp.embeddings import cosine_similarity, embed_text


def test_dedupe_similarity() -> None:
    vec_a = embed_text("Gold rises on safe haven demand")
    vec_b = embed_text("Gold rises on safe haven demand")
    assert cosine_similarity(vec_a, vec_b) > 0.9
