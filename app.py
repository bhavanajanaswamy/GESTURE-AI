"""
GestureSpeak AI — webcam-based hand gesture communication prototype.

Controls:
  SPACE     Add the currently detected gesture to the message
  BACKSPACE Undo the last message item
  C         Clear the message
  S         Speak the current message (requires pyttsx3)
  Q or ESC  Quit

This is a small-vocabulary gesture prototype, NOT a full sign-language translator.
"""
from collections import deque
import time

import cv2
import mediapipe as mp

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None

from gestures import classify_gesture, GESTURE_MESSAGES


WINDOW_NAME = "GestureSpeak AI | Q: quit | SPACE: add | S: speak | C: clear"


def speak_text(text: str) -> None:
    """Speak text if pyttsx3 is installed and a message exists."""
    if not text.strip():
        return
    if pyttsx3 is None:
        print("Text-to-speech is not installed. Run: pip install pyttsx3")
        return
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as exc:
        print(f"Speech could not be played: {exc}")


def draw_panel(frame, gesture, message_parts, fps):
    """Draw the app's readable status and message panel."""
    h, w = frame.shape[:2]
    overlay = frame.copy()
    panel_top = max(0, h - 142)
    cv2.rectangle(overlay, (0, panel_top), (w, h), (18, 24, 38), -1)
    cv2.addWeighted(overlay, 0.82, frame, 0.18, 0, frame)

    meaning = GESTURE_MESSAGES.get(gesture, "No message mapped")
    cv2.putText(frame, f"Gesture: {gesture or 'No hand detected'}",
                (18, panel_top + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.72,
                (90, 230, 180), 2, cv2.LINE_AA)
    cv2.putText(frame, f"Meaning: {meaning if gesture else 'Show one hand to the camera'}",
                (18, panel_top + 60), cv2.FONT_HERSHEY_SIMPLEX, 0.55,
                (245, 245, 245), 1, cv2.LINE_AA)

    message = " ".join(message_parts).strip() or "(your message will appear here)"
    max_chars = max(25, int((w - 30) / 10))
    if len(message) > max_chars:
        message = "..." + message[-(max_chars - 3):]
    cv2.putText(frame, f"Message: {message}", (18, panel_top + 91),
                cv2.FONT_HERSHEY_SIMPLEX, 0.52, (255, 220, 120), 1, cv2.LINE_AA)
    cv2.putText(frame, f"FPS: {fps:.0f}", (w - 105, 28),
                cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, "SPACE add | S speak | BACKSPACE undo | C clear | Q quit",
                (18, h - 12), cv2.FONT_HERSHEY_SIMPLEX, 0.43,
                (210, 215, 225), 1, cv2.LINE_AA)


def main():
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    mp_styles = mp.solutions.drawing_styles

    camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not camera.isOpened():
        camera.release()
        camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("ERROR: Could not open webcam.")
        print("Check Windows camera permissions and close other apps using the camera.")
        return

    message_parts = []
    recent_predictions = deque(maxlen=5)
    previous_time = time.time()
    fps = 0.0

    print("GestureSpeak AI started.")
    print("Show a gesture, then press SPACE to add its message.")
    print("Press Q to quit.")

    try:
        with mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            model_complexity=0,
            min_detection_confidence=0.60,
            min_tracking_confidence=0.55,
        ) as hands:
            while True:
                ok, frame = camera.read()
                if not ok:
                    print("Could not read a frame from the webcam.")
                    break

                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                rgb.flags.writeable = False
                result = hands.process(rgb)
                rgb.flags.writeable = True

                raw_gesture = None
                if result.multi_hand_landmarks:
                    hand_landmarks = result.multi_hand_landmarks[0]
                    mp_draw.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_styles.get_default_hand_landmarks_style(),
                        mp_styles.get_default_hand_connections_style(),
                    )
                    raw_gesture = classify_gesture(hand_landmarks.landmark)

                recent_predictions.append(raw_gesture)
                # Only show a gesture when at least 3 of the last 5 frames agree.
                stable_gesture = None
                nonempty = [g for g in recent_predictions if g is not None]
                if nonempty:
                    candidate = max(set(nonempty), key=nonempty.count)
                    if nonempty.count(candidate) >= 3:
                        stable_gesture = candidate

                now = time.time()
                elapsed = now - previous_time
                if elapsed > 0:
                    instant_fps = 1.0 / elapsed
                    fps = instant_fps if fps == 0 else 0.85 * fps + 0.15 * instant_fps
                previous_time = now

                draw_panel(frame, stable_gesture, message_parts, fps)
                cv2.imshow(WINDOW_NAME, frame)

                key = cv2.waitKey(1) & 0xFF
                if key in (ord("q"), 27):
                    break
                elif key == 32:  # Space
                    if stable_gesture:
                        message_parts.append(GESTURE_MESSAGES[stable_gesture])
                        print("Message:", " ".join(message_parts))
                    else:
                        print("No stable gesture yet. Hold your hand steady and try again.")
                elif key in (ord("c"), ord("C")):
                    message_parts.clear()
                elif key in (8, 127):  # Backspace/Delete
                    if message_parts:
                        message_parts.pop()
                elif key in (ord("s"), ord("S")):
                    speak_text(" ".join(message_parts))

    finally:
        camera.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
