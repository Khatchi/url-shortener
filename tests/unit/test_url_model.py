import uuid

from sqlalchemy import inspect

from app.models.url import URL


def test_url_model_has_expected_columns():
    mapper = inspect(URL)
    columns = { column.key for column in mapper.columns }

    assert columns == {
        "id",
        "original_url",
        "short_code",
        "created_at",
    }

def test_url_model_uses_uuid_primary_key():
    mapper = inspect(URL)
    primary_key = mapper.primary_key[0]

    assert primary_key.key == "id"
    assert primary_key.type.python_type is uuid.UUID


def test_url_model_short_code_is_unique():
    mapper = inspect(URL)
    short_code = mapper.columns.short_code

    assert short_code.unique is True


def test_url_model_required_columns_are_not_nullable():
    mapper = inspect(URL)

    assert mapper.columns.id.nullable is False
    assert mapper.columns.original_url.nullable is False
    assert mapper.columns.short_code.nullable is False
    assert mapper.columns.created_at.nullable is False


def test_url_model_short_code_has_length_six():
    mapper = inspect(URL)

    assert mapper.columns.short_code.type.length == 6
