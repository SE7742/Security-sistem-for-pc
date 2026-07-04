import importlib


def load_database(monkeypatch, tmp_path):
    face_database = importlib.import_module("face_database")
    known_faces_dir = tmp_path / "known_faces"
    known_faces_dir.mkdir()
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(face_database, "KNOWN_FACES_DIR", str(known_faces_dir))
    return face_database.FaceDatabase(), known_faces_dir


def test_known_faces_count_is_empty_for_empty_directory(monkeypatch, tmp_path):
    database, _ = load_database(monkeypatch, tmp_path)

    assert database.get_known_names() == []
    assert database.get_known_faces_count() == 0


def test_known_faces_count_deduplicates_timestamped_files(monkeypatch, tmp_path):
    database, known_faces_dir = load_database(monkeypatch, tmp_path)
    (known_faces_dir / "Ali_20240101_120000.jpg").write_bytes(b"fake")
    (known_faces_dir / "Ali_20240102_120000.jpeg").write_bytes(b"fake")
    (known_faces_dir / "Ayse.png").write_bytes(b"fake")
    (known_faces_dir / "notes.txt").write_text("ignored", encoding="utf-8")

    assert set(database.get_known_names()) == {"Ali", "Ayse"}
    assert database.get_known_faces_count() == 2


def test_add_person_copies_image_into_known_faces(monkeypatch, tmp_path):
    database, known_faces_dir = load_database(monkeypatch, tmp_path)
    source = tmp_path / "source.jpg"
    source.write_bytes(b"fake")

    assert database.add_person(str(source), "Zeynep") is True
    assert (known_faces_dir / "Zeynep.jpg").exists()


def test_delete_person_removes_only_matching_images(monkeypatch, tmp_path):
    database, known_faces_dir = load_database(monkeypatch, tmp_path)
    ali_file = known_faces_dir / "Ali_20240101_120000.jpg"
    veli_file = known_faces_dir / "Veli_20240101_120000.jpg"
    ali_file.write_bytes(b"fake")
    veli_file.write_bytes(b"fake")

    success, message = database.delete_person("Ali")

    assert success is True
    assert "1 dosya" in message
    assert not ali_file.exists()
    assert veli_file.exists()
