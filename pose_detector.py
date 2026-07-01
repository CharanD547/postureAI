from pathlib import Path

import cv2
import numpy as np
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import (
    PoseLandmarker,
    PoseLandmarkerOptions,
    PoseLandmarksConnections,
    RunningMode,
    drawing_styles,
    drawing_utils,
)
from mediapipe.tasks.python.vision.core import image as mp_image

MODEL_PATH = Path(__file__).resolve().parent / "models" / "pose_landmarker.task"


class PoseDetector:
    """Detect body pose landmarks using MediaPipe Pose Landmarker (Tasks API)."""

    def __init__(self):
        if not MODEL_PATH.is_file() or MODEL_PATH.stat().st_size == 0:
            raise FileNotFoundError(
                f"Pose model not found at {MODEL_PATH}. "
                "Download pose_landmarker_lite.task from Google's MediaPipe model "
                "host and save it as models/pose_landmarker.task."
            )

        options = PoseLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=str(MODEL_PATH)),
            running_mode=RunningMode.IMAGE,
            num_poses=1,
            min_pose_detection_confidence=0.5,
        )
        self._landmarker = PoseLandmarker.create_from_options(options)

    def detect(self, rgb_image):
        """
        Run pose detection on an RGB image.

        Returns:
            landmarks: list of (x, y, visibility) in normalized [0, 1] coords, or None
            annotated_image: RGB image with skeleton drawn
        """
        rgb_array = np.ascontiguousarray(rgb_image)
        mp_img = mp_image.Image(
            image_format=mp_image.ImageFormat.SRGB,
            data=rgb_array,
        )
        result = self._landmarker.detect(mp_img)

        if not result.pose_landmarks:
            return None, rgb_image.copy()

        pose_landmarks = result.pose_landmarks[0]
        landmarks = []
        for lm in pose_landmarks:
            visibility = lm.visibility
            if visibility is None:
                visibility = lm.presence if lm.presence is not None else 1.0
            landmarks.append((lm.x, lm.y, visibility))

        annotated_bgr = cv2.cvtColor(rgb_image.copy(), cv2.COLOR_RGB2BGR)
        drawing_utils.draw_landmarks(
            annotated_bgr,
            pose_landmarks,
            PoseLandmarksConnections.POSE_LANDMARKS,
            landmark_drawing_spec=drawing_styles.get_default_pose_landmarks_style(),
        )
        annotated_rgb = cv2.cvtColor(annotated_bgr, cv2.COLOR_BGR2RGB)

        return landmarks, annotated_rgb

    def landmarks_to_pixels(self, landmarks, image_shape):
        """Convert normalized landmarks to pixel (x, y) coordinates."""
        height, width = image_shape[:2]
        pixels = []
        for x, y, _visibility in landmarks:
            pixels.append((int(x * width), int(y * height)))
        return pixels

    def close(self):
        self._landmarker.close()
