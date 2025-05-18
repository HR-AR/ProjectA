from llm import summarise, classify


def test_classify_simple():
    tasks = ["Call Bob [Business]", "Buy milk [Personal]"]
    result = classify(tasks)
    assert result["business"] == ["Call Bob [Business]"]
    assert result["personal"] == ["Buy milk [Personal]"]
