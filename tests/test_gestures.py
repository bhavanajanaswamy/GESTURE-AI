import unittest
import sys
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from gestures import classify_gesture


def make_hand(points):
    """Create 21 dummy landmarks from (x, y) pairs."""
    return [SimpleNamespace(x=x, y=y) for x, y in points]


def baseline_hand():
    # Default curled hand; tip y is below its PIP joint (larger y means lower).
    points = [(0.5, 0.5) for _ in range(21)]
    for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
        points[pip] = (0.5, 0.45)
        points[tip] = (0.5, 0.65)
    # Thumb tip and IP are close to index MCP for a curled thumb.
    points[5] = (0.55, 0.48)
    points[3] = (0.53, 0.53)
    points[4] = (0.54, 0.56)
    return points


class GestureClassifierTests(unittest.TestCase):
    def test_missing_landmarks_returns_none(self):
        self.assertIsNone(classify_gesture(None))
        self.assertIsNone(classify_gesture([]))

    def test_fist(self):
        self.assertEqual(classify_gesture(make_hand(baseline_hand())), "FIST")

    def test_open_palm(self):
        p = baseline_hand()
        for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
            p[tip] = (0.5, 0.25)
        self.assertEqual(classify_gesture(make_hand(p)), "OPEN_PALM")

    def test_peace(self):
        p = baseline_hand()
        p[8] = (0.5, 0.25)
        p[12] = (0.5, 0.24)
        self.assertEqual(classify_gesture(make_hand(p)), "PEACE")

    def test_pointing(self):
        p = baseline_hand()
        p[8] = (0.5, 0.25)
        self.assertEqual(classify_gesture(make_hand(p)), "POINTING")


if __name__ == "__main__":
    unittest.main()
