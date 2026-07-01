"""
Analyze MediaPipe pose landmarks for common posture issues.

Landmark indices (MediaPipe Pose):
  0 nose, 7 left_ear, 8 right_ear
  11 left_shoulder, 12 right_shoulder
  23 left_hip, 24 right_hip
"""

NOSE = 0
LEFT_EAR = 7
RIGHT_EAR = 8
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12
LEFT_HIP = 23
RIGHT_HIP = 24

# Normalized-coordinate thresholds (tune for sensitivity)
SHOULDER_LEVEL_THRESHOLD = 0.03
HIP_LEVEL_THRESHOLD = 0.03
FORWARD_HEAD_THRESHOLD = 0.06
ROUNDED_SHOULDER_THRESHOLD = 0.08


def _visible(landmarks, index, min_visibility=0.5):
    return landmarks[index][2] >= min_visibility


def _midpoint(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


def analyze_posture(landmarks):
    """
    Inspect pose landmarks and return a list of findings.

    Each finding is a dict:
        issue: human-readable label
        recommendation_key: key for reccomendations.RECOMMENDATIONS
        detail: short explanation
    """
    if landmarks is None or len(landmarks) < 25:
        return []

    findings = []

    if (
        _visible(landmarks, LEFT_SHOULDER)
        and _visible(landmarks, RIGHT_SHOULDER)
    ):
        shoulder_drop = abs(
            landmarks[LEFT_SHOULDER][1] - landmarks[RIGHT_SHOULDER][1]
        )
        if shoulder_drop > SHOULDER_LEVEL_THRESHOLD:
            higher = "left" if landmarks[LEFT_SHOULDER][1] < landmarks[RIGHT_SHOULDER][1] else "right"
            findings.append(
                {
                    "issue": "Uneven shoulders",
                    "recommendation_key": "uneven_shoulders",
                    "detail": f"One shoulder sits higher than the other ({higher} side elevated).",
                }
            )

    if _visible(landmarks, LEFT_HIP) and _visible(landmarks, RIGHT_HIP):
        hip_drop = abs(landmarks[LEFT_HIP][1] - landmarks[RIGHT_HIP][1])
        if hip_drop > HIP_LEVEL_THRESHOLD:
            findings.append(
                {
                    "issue": "Uneven hips",
                    "recommendation_key": "uneven_hips",
                    "detail": "Hip line appears tilted, which can affect pelvic alignment.",
                }
            )

    if (
        _visible(landmarks, NOSE)
        and _visible(landmarks, LEFT_SHOULDER)
        and _visible(landmarks, RIGHT_SHOULDER)
    ):
        shoulder_mid = _midpoint(
            landmarks[LEFT_SHOULDER], landmarks[RIGHT_SHOULDER]
        )
        # Forward head: nose sits noticeably below shoulder midpoint (drooped head)
        head_offset = landmarks[NOSE][1] - shoulder_mid[1]
        if head_offset > FORWARD_HEAD_THRESHOLD:
            findings.append(
                {
                    "issue": "Forward head posture",
                    "recommendation_key": "forward_head",
                    "detail": "Head appears shifted forward relative to the shoulders.",
                }
            )

    if (
        _visible(landmarks, LEFT_SHOULDER)
        and _visible(landmarks, RIGHT_SHOULDER)
        and _visible(landmarks, LEFT_HIP)
        and _visible(landmarks, RIGHT_HIP)
    ):
        shoulder_mid = _midpoint(
            landmarks[LEFT_SHOULDER], landmarks[RIGHT_SHOULDER]
        )
        hip_mid = _midpoint(landmarks[LEFT_HIP], landmarks[RIGHT_HIP])
        # Rounded shoulders: shoulder midpoint sits in front of hip midpoint (wider x gap)
        shoulder_forward = shoulder_mid[0] - hip_mid[0]
        torso_width = abs(
            landmarks[LEFT_SHOULDER][0] - landmarks[RIGHT_SHOULDER][0]
        )
        if torso_width > 0.05 and abs(shoulder_forward) > ROUNDED_SHOULDER_THRESHOLD:
            findings.append(
                {
                    "issue": "Rounded shoulders",
                    "recommendation_key": "rounded_shoulders",
                    "detail": "Shoulders appear rolled forward relative to the torso.",
                }
            )

    return findings
