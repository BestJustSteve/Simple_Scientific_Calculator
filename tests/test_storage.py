import json

import pytest

from calculator.storage import (
    load_data,
    save_data,
)


def test_save_and_load_data(tmp_path):
    test_file = tmp_path / "test_data.json"

    history = [
        {
            "timestamp": "2026-09-20 12:00:00",
            "expression": "2 + 2",
            "result": 4,
        }
    ]

    memory = {
        "answer": 4,
    }

    last_result = 4

    save_data(
        history,
        memory,
        last_result,
        test_file,
    )

    loaded_history, loaded_memory, loaded_result = load_data(test_file)

    assert loaded_history == history
    assert loaded_memory == memory
    assert loaded_result == last_result


def test_load_missing_file(tmp_path):
    test_file = tmp_path / "does_not_exist.json"

    history, memory, last_result = load_data(test_file)

    assert history == []
    assert memory == {}
    assert last_result is None


def test_load_corrupt_json(tmp_path):
    test_file = tmp_path / "bad_data.json"

    test_file.write_text(
        "{ invalid json }",
        encoding="utf-8",
    )

    history, memory, last_result = load_data(test_file)

    assert history == []
    assert memory == {}
    assert last_result is None


def test_load_missing_history_key(tmp_path):
    test_file = tmp_path / "data.json"

    data = {
        "memory": {
            "tax": 0.08,
        },
        "last_result": 10,
    }

    test_file.write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    history, memory, last_result = load_data(test_file)

    assert history == []
    assert memory == {"tax": 0.08}
    assert last_result == 10


def test_load_missing_memory_key(tmp_path):
    test_file = tmp_path / "data.json"

    data = {
        "history": [],
        "last_result": 25,
    }

    test_file.write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    history, memory, last_result = load_data(test_file)

    assert history == []
    assert memory == {}
    assert last_result == 25


def test_load_missing_last_result_key(tmp_path):
    test_file = tmp_path / "data.json"

    data = {
        "history": [],
        "memory": {},
    }

    test_file.write_text(
        json.dumps(data),
        encoding="utf-8",
    )

    history, memory, last_result = load_data(test_file)

    assert history == []
    assert memory == {}
    assert last_result is None


def test_save_creates_valid_json(tmp_path):
    test_file = tmp_path / "data.json"

    history = []
    memory = {
        "subtotal": 149.99,
    }
    last_result = 149.99

    save_data(
        history,
        memory,
        last_result,
        test_file,
    )

    with open(
        test_file,
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    assert data == {
        "history": [],
        "memory": {
            "subtotal": 149.99,
        },
        "last_result": 149.99,
    }


def test_save_overwrites_existing_file(tmp_path):
    test_file = tmp_path / "data.json"

    save_data(
        [],
        {},
        10,
        test_file,
    )

    save_data(
        [],
        {
            "answer": 20,
        },
        20,
        test_file,
    )

    history, memory, last_result = load_data(test_file)

    assert history == []
    assert memory == {
        "answer": 20,
    }
    assert last_result == 20


def test_save_data_raises_oserror_for_invalid_location(tmp_path):
    invalid_file = tmp_path / "missing_folder" / "calculator_data.json"

    with pytest.raises(OSError):
        save_data(
            [],
            {},
            None,
            invalid_file,
        )


def test_get_data_file_creates_app_directory(tmp_path, monkeypatch):
    monkeypatch.setenv(
        "LOCALAPPDATA",
        str(tmp_path),
    )

    from calculator import storage

    data_file = storage.get_data_file()

    assert data_file.parent.exists()
    assert data_file.name == "calculator_data.json"
    assert data_file.parent.name == "SimpleScientificCalculator"
