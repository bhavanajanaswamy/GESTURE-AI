"""Rule-based gesture classification from MediaPipe's 21 hand landmarks."""

# Human-readable phrases used by the message builder.
GESTURE_MESSAGES = {
    "OPEN_PALM": "Hello",
    "FIST": "Stop",
    "THUMBS_UP": "Yes",
    "PEACE": "Peace",
    "POINTING": "Look there",
}


def _finger_is_up(landmarks, tip_idx, pip_idx):
    """For a mirrored, upright hand image, fingertips are usually above PIP joints."""
    return landmarks[tip_idx].y < landmarks[pip_idx].y


def _thumb_is_up(landmarks):
    # With the mirrored webcam view, thumb tip tends to be farther outward than IP.
    # Use distance from the index-finger MCP to avoid relying on left/right labels.
    thumb_tip = landmarks[4]
    thumb_ip = landmarks[3]
    index_mcp = landmarks[5]
    tip_dist = abs(thumb_tip.x - index_mcp.x)
    ip_dist = abs(thumb_ip.x - index_mcp.x)
    return tip_dist > ip_dist * 1.18


def classify_gesture(landmarks):
    """
    Return a supported gesture name or None.

    `landmarks` should be the 21 landmark objects from MediaPipe Hands.
    These simple geometric rules work best with one upright hand, good lighting,
    and the palm facing the camera. This is a prototype, not a sign-language model.
    """
    if landmarks is None or len(landmarks) < 21:
        return None

    index_up = _finger_is_up(landmarks, 8, 6)
    middle_up = _finger_is_up(landmarks, 12, 10)
    ring_up = _finger_is_up(landmarks, 16, 14)
    pinky_up = _finger_is_up(landmarks, 20, 18)
    thumb_up = _thumb_is_up(landmarks)

    four_fingers = [index_up, middle_up, ring_up, pinky_up]
    count_up = sum(four_fingers)

    if all(four_fingers):
        return "OPEN_PALM"
    if index_up and middle_up and not ring_up and not pinky_up:
        return "PEACE"
    if index_up and not middle_up and not ring_up and not pinky_up:
        return "POINTING"
    if thumb_up and count_up == 0:
        return "THUMBS_UP"
    if not any(four_fingers) and not thumb_up:
        return "FIST"
    return None
