import string

from app.core.short_code import generate_short_code

def test_generate_short_code_has_expected_length():
    short_code = generate_short_code()

    assert len(short_code) == 6


def test_generate_short_code_uses_base62_characters():
    short_code = generate_short_code()
    base62_characters = string.ascii_letters + string.digits

    assert all(character in base62_characters for character in short_code)


def test_generate_short_code_generates_different_values():
    first = generate_short_code()
    second = generate_short_code()

    assert first != second


