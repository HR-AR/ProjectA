from llm import split_into_chunks


def test_split_into_chunks():
    text = "\n".join([f"line{i}" for i in range(120)])
    chunks = split_into_chunks(text, max_tokens=50)
    assert len(chunks) > 1
