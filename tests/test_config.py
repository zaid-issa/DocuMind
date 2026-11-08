import pytest

from app.config import DEFAULT_GROQ_MODEL, get_settings


@pytest.fixture(autouse=True)
def clean_environment(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    monkeypatch.delenv("GROQ_MODEL", raising=False)


def test_settings_are_read_from_env_file(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("GROQ_API_KEY=test-key\nGROQ_MODEL=test-model\n")

    settings = get_settings(env_file)

    assert settings.groq_api_key == "test-key"
    assert settings.groq_model == "test-model"


def test_environment_variable_overrides_env_file(tmp_path, monkeypatch):
    env_file = tmp_path / ".env"
    env_file.write_text("GROQ_API_KEY=from-file\n")
    monkeypatch.setenv("GROQ_API_KEY", "from-environment")

    assert get_settings(env_file).groq_api_key == "from-environment"


def test_missing_api_key_raises(tmp_path):
    with pytest.raises(RuntimeError):
        get_settings(tmp_path / "missing.env")


def test_model_has_a_default(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("GROQ_API_KEY=test-key\n")

    assert get_settings(env_file).groq_model == DEFAULT_GROQ_MODEL