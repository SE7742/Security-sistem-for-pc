import sys
import types

import pytest


@pytest.fixture(autouse=True)
def config_stub(monkeypatch, tmp_path):
    config = types.ModuleType("config")
    config.TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
    config.CHAT_ID = "YOUR_CHAT_ID_HERE"
    config.NOTIFICATION_COOLDOWN = 30
    config.KNOWN_FACES_DIR = str(tmp_path / "known_faces")
    config.LOGS_DIR = str(tmp_path / "logs")
    config.TEMP_DIR = str(tmp_path / "temp")
    config.CAMERA_INDEX = 0
    config.FRAME_WIDTH = 640
    config.FRAME_HEIGHT = 480
    config.FACE_RECOGNITION_TOLERANCE = 0.6
    monkeypatch.setitem(sys.modules, "config", config)
    return config
