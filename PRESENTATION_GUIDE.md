# Presentation Guide — GestureSpeak AI

## 60–90 second pitch

Hello judges. My project is GestureSpeak AI, a webcam-based gesture recognition prototype. The goal is to demonstrate how computer vision can help turn a small set of hand gestures into simple text messages and spoken output.

The app uses MediaPipe to detect 21 hand landmarks. OpenCV captures the webcam video and draws the landmarks. A Python rule-based classifier checks the relative positions of the fingers to recognize five supported gestures. Users press Space to add a phrase, and press S to speak the composed message.

The prototype runs locally and does not upload camera frames. It is not a full sign-language translator, and its current vocabulary is limited. The next steps are to collect carefully labeled data with consent, train and evaluate a classifier, improve robustness across different hands and camera angles, and work with sign-language users and accessibility experts before making broader claims.

Thank you. I am happy to demonstrate the system and explain its design.

## Live demo plan

1. Start `python app.py`.
2. Hold an open palm and wait for the label to stabilize.
3. Press Space; show “Hello” in the message line.
4. Try a peace sign or pointing gesture and press Space again.
5. Press S to speak the composed message.
6. Press C to clear the message.
7. Explain the limitations and next steps.

## Suggested judge questions and answers

**Q: Is this a real AI model?**  
A: The hand landmark detector is a pretrained MediaPipe model. The current mapping from landmarks to five gestures is a transparent rule-based classifier. A future version can train a separate classifier on labeled gesture examples.

**Q: Is it a sign-language translator?**  
A: No. It is a small-vocabulary gesture recognition prototype. Sign languages have their own grammar, movement, and context; this prototype does not translate them.

**Q: Does it need internet?**  
A: After packages are installed, the webcam inference runs locally and does not send camera frames to a server.

**Q: What are the limitations?**  
A: Lighting, camera angle, hand orientation, and the simple geometric rules can affect recognition. It recognizes only five gestures and needs more evaluation.

**Q: What makes it useful?**  
A: It demonstrates an accessible interaction pattern, combining vision, text, and speech in one local prototype. It is a starting point for further user-centered research, not a replacement for established communication aids.

**Q: How would you improve accuracy?**  
A: Collect diverse, consent-based samples, split them into train/validation/test sets, compare a trained classifier with the rules, measure per-class precision and recall, and test with users in realistic conditions.
