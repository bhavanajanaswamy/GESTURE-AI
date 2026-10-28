# GestureSpeak AI

A beginner-friendly, webcam-based gesture recognition prototype. It uses MediaPipe's pretrained hand-landmark model and simple geometric rules to recognize five gestures, turn them into short text phrases, and optionally speak the composed message.

> **Important:** This is not a complete sign-language translator and should not be used for essential communication. Gesture recognition may fail with unusual hand angles, poor lighting, or different camera positions.

## Features

- Real-time webcam feed with hand landmark overlay
- Five supported gestures: open palm, fist, thumbs-up, peace sign, pointing finger
- Frame smoothing to reduce flicker
- Press Space to add a phrase to the message
- Press S to speak the composed message
- Press Backspace to undo and C to clear
- Runs locally; camera frames are not uploaded by this application

## Technology

- Python
- OpenCV (`opencv-python`) for webcam capture and display
- MediaPipe Hands for pretrained hand landmark detection
- Rule-based classification in `gestures.py`
- `pyttsx3` for optional local text-to-speech

MediaPipe is an open-source framework. Review the current licenses and package requirements for all dependencies before distributing a build.

## Requirements

- Windows 10/11
- Python 3.11 (recommended for a beginner setup)
- VS Code and the Microsoft Python extension
- A working webcam

## Setup on Windows

Open PowerShell in the project folder:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PowerShell blocks environment activation, use Command Prompt instead:

```bat
py -3.11 -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
```

In VS Code, select the `.venv` interpreter:
`Ctrl+Shift+P` → `Python: Select Interpreter` → choose `.venv`.

## Run

```powershell
python app.py
```

A webcam window should open. Hold one supported gesture steadily, then press Space to add its phrase to the message.

### Keyboard controls

| Key | Action |
|---|---|
| Space | Add current recognized gesture to the message |
| S | Speak the message |
| Backspace | Undo last phrase |
| C | Clear the message |
| Q or Esc | Quit |

## Gesture vocabulary

| Gesture | Message |
|---|---|
| Open palm | Hello |
| Fist | Stop |
| Thumbs-up | Yes |
| Peace sign | Peace |
| Pointing finger | Look there |

These are generic hand gestures and are not claims about the meaning of gestures in any sign language.

## Troubleshooting

**`py` is not recognized:** Install Python from https://www.python.org/downloads/windows/ and select “Add Python to PATH”. Restart VS Code.

**PowerShell activation error:** Use the Command Prompt activation commands above, or run `.venv\Scripts\python.exe app.py` after installation.

**Camera cannot open:** Check Windows Settings → Privacy & security → Camera, allow desktop apps to access the camera, and close Zoom/Teams/browser tabs using it. If you have multiple cameras, edit `cv2.VideoCapture(0, ...)` in `app.py` to try `1`.

**No hand landmarks:** Improve lighting, show one hand, keep the palm visible, and hold it upright in the frame.

**Speech does not work:** Try `pip install --upgrade pyttsx3`. The app still works without speech.

**Package installation fails:** Confirm you are using 64-bit Python 3.11 and the `.venv` interpreter. Then try `python -m pip install -r requirements.txt`.

## Project structure

```text
GestureSpeak_AI/
├── app.py
├── gestures.py
├── requirements.txt
├── README.md
├── LICENSE
├── .gitignore
├── PRESENTATION_GUIDE.md
└── tests/
    └── test_gestures.py
```

## Testing

Run the simple rule tests:

```powershell
python -m unittest discover -s tests -v
```

Then run the webcam application and test each gesture under good lighting. Results may vary because the gesture rules are geometric heuristics.

## GitHub publishing

1. Create a new **public** repository on GitHub named `GestureSpeak-AI`.
2. Do not initialize it with a README if you already have this project README.
3. In the project folder terminal, run:

```powershell
git init
git add .
git commit -m "Build GestureSpeak AI prototype"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/GestureSpeak-AI.git
git push -u origin main
```

4. Replace `YOUR-USERNAME` with your actual GitHub username. The repository link will be `https://github.com/YOUR-USERNAME/GestureSpeak-AI`.
5. If Git asks you to sign in, follow GitHub's official sign-in prompt. Never put a password or access token in source code.

## Future improvements

- Collect consent-based samples and train a small classifier for a custom vocabulary
- Add support for more users and hand orientations
- Add language selection and configurable phrases
- Add a visual tutorial and confidence feedback
- Evaluate accuracy on a documented test set

## License

This project code is released under the MIT License. Third-party dependencies and their pretrained models have their own licenses; check them separately.
