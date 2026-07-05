import importlib

import numpy as np


class FakeCascade:
    def detectMultiScale(self, gray, scaleFactor, minNeighbors, minSize):
        if int(gray[0, 0, 0]) == 1:
            return [(0, 0, 10, 10)]
        return []


class FakeRecognizer:
    def __init__(self):
        self.trained_faces = None
        self.trained_labels = None

    def train(self, faces, labels):
        self.trained_faces = faces
        self.trained_labels = list(labels)


def make_image(has_face):
    image = np.zeros((20, 20, 3), dtype=np.uint8)
    image[0, 0, 0] = 1 if has_face else 0
    return image


def setup_detector(monkeypatch, tmp_path):
    face_detector = importlib.import_module("face_detector")
    known_faces_dir = tmp_path / "known_faces"
    known_faces_dir.mkdir()
    monkeypatch.setattr(face_detector, "KNOWN_FACES_DIR", str(known_faces_dir))
    monkeypatch.setattr(face_detector.cv2, "cvtColor", lambda image, code: image)
    monkeypatch.setattr(face_detector.cv2, "resize", lambda image, size: image)
    return face_detector, known_faces_dir


def test_load_known_faces_skips_images_without_detected_faces(monkeypatch, tmp_path):
    face_detector, known_faces_dir = setup_detector(monkeypatch, tmp_path)
    (known_faces_dir / "Ali.jpg").write_bytes(b"fake")
    recognizers = []

    monkeypatch.setattr(face_detector.cv2, "imread", lambda path: make_image(False))
    monkeypatch.setattr(
        face_detector.cv2.face,
        "LBPHFaceRecognizer_create",
        lambda: recognizers.append(FakeRecognizer()) or recognizers[-1],
    )

    detector = face_detector.FaceDetector.__new__(face_detector.FaceDetector)
    detector.face_cascade = FakeCascade()
    detector.face_recognizer = FakeRecognizer()

    detector._load_known_faces()

    assert detector.model_trained is False
    assert detector.face_labels == {}
    assert recognizers == []


def test_load_known_faces_trains_with_matching_faces_and_labels(monkeypatch, tmp_path):
    face_detector, known_faces_dir = setup_detector(monkeypatch, tmp_path)
    (known_faces_dir / "Ali.jpg").write_bytes(b"fake")
    (known_faces_dir / "Veli.jpg").write_bytes(b"fake")
    recognizer = FakeRecognizer()

    def fake_imread(path):
        return make_image(path.endswith("Ali.jpg"))

    monkeypatch.setattr(face_detector.cv2, "imread", fake_imread)
    monkeypatch.setattr(
        face_detector.cv2.face,
        "LBPHFaceRecognizer_create",
        lambda: recognizer,
    )

    detector = face_detector.FaceDetector.__new__(face_detector.FaceDetector)
    detector.face_cascade = FakeCascade()
    detector.face_recognizer = FakeRecognizer()

    detector._load_known_faces()

    assert detector.model_trained is True
    assert len(recognizer.trained_faces) == 1
    assert recognizer.trained_labels == [0]
    assert detector.face_labels == {0: "Ali"}
