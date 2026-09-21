import json
import os
from pathlib import Path
from typing import TypedDict, cast

from calculator.calculator_engine import Number

APP_NAME = "SimpleScientificCalculator"


class HistoryEntry(TypedDict):
    timestamp: str
    expression: str
    result: Number


History = list[HistoryEntry]
Memory = dict[str, Number]


class Settings(TypedDict):
    angle_mode: str
    geometry: str


DEFAULT_SETTINGS: Settings = {
    "angle_mode": "radians",
    "geometry": "",
}


def get_data_file() -> Path:
    if os.name == "nt":
        local_app_data = os.getenv("LOCALAPPDATA")

        if local_app_data:
            base_directory = Path(local_app_data)
        else:
            base_directory = Path.home() / "AppData" / "Local"
    else:
        base_directory = Path.home() / ".local" / "share"

    app_directory = base_directory / APP_NAME

    app_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    return app_directory / "calculator_data.json"


DATA_FILE = get_data_file()


def _read_data(
    file_path: Path,
) -> dict[str, object]:
    if not file_path.exists():
        return {}

    try:
        with file_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

    except (
        json.JSONDecodeError,
        OSError,
    ):
        return {}

    if not isinstance(
        data,
        dict,
    ):
        return {}

    return data


def _parse_history(
    data: dict[str, object],
) -> History:
    raw_history = data.get(
        "history",
        [],
    )

    if isinstance(
        raw_history,
        list,
    ):
        return cast(
            History,
            raw_history,
        )

    return []


def _parse_memory(
    data: dict[str, object],
) -> Memory:
    raw_memory = data.get(
        "memory",
        {},
    )

    if isinstance(
        raw_memory,
        dict,
    ):
        return cast(
            Memory,
            raw_memory,
        )

    return {}


def _parse_last_result(
    data: dict[str, object],
) -> Number | None:
    raw_last_result = data.get("last_result")

    if isinstance(
        raw_last_result,
        (int, float),
    ) and not isinstance(
        raw_last_result,
        bool,
    ):
        return raw_last_result

    return None


def _parse_settings(
    data: dict[str, object],
) -> Settings:
    settings = DEFAULT_SETTINGS.copy()

    raw_settings = data.get(
        "settings",
        {},
    )

    if not isinstance(
        raw_settings,
        dict,
    ):
        return settings

    angle_mode = raw_settings.get("angle_mode")

    geometry = raw_settings.get("geometry")

    if isinstance(
        angle_mode,
        str,
    ):
        settings["angle_mode"] = angle_mode

    if isinstance(
        geometry,
        str,
    ):
        settings["geometry"] = geometry

    return settings


def load_data(
    file_path: Path | None = None,
) -> (
    tuple[
        History,
        Memory,
        Number | None,
    ]
    | tuple[
        History,
        Memory,
        Number | None,
        Settings,
    ]
):
    use_legacy_return = file_path is not None

    target_file = file_path if file_path is not None else DATA_FILE

    data = _read_data(target_file)

    history = _parse_history(data)

    memory = _parse_memory(data)

    last_result = _parse_last_result(data)

    if use_legacy_return:
        return (
            history,
            memory,
            last_result,
        )

    settings = _parse_settings(data)

    return (
        history,
        memory,
        last_result,
        settings,
    )


def save_data(
    history: History,
    memory: Memory,
    last_result: Number | None,
    settings_or_file: (Settings | Path | None) = None,
    file_path: Path | None = None,
) -> None:
    settings: Settings | None

    if isinstance(
        settings_or_file,
        Path,
    ):
        settings = None
        target_file = settings_or_file

    else:
        settings = settings_or_file

        target_file = file_path if file_path is not None else DATA_FILE

    data: dict[str, object] = {
        "history": history,
        "memory": memory,
        "last_result": last_result,
    }

    if settings is not None:
        data["settings"] = settings

    with target_file.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            data,
            file,
            indent=4,
        )
