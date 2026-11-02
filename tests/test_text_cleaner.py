from app.services.text_cleaner import clean_text


def test_clean_text_joins_wrapped_lines():
    assert clean_text("machine learning in \nPython") == "machine learning in Python"


def test_clean_text_keeps_paragraph_breaks():
    raw = "First paragraph. \n \nSecond paragraph."
    assert clean_text(raw) == "First paragraph.\n\nSecond paragraph."


def test_clean_text_collapses_spaces():
    assert clean_text("too    many   spaces") == "too many spaces"