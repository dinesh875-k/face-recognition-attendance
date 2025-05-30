

from google.colab import userdata
userdata.get('DineshHUG')

!pip install insightface
!pip install onnxruntime
from insightface.app import FaceAnalysis
import cv2
import numpy as np

# Initialize InsightFace model
app = FaceAnalysis()
app.prepare(ctx_id=0)  # set to -1 if running on CPU

reference_img = cv2.imread("/WhatsApp Image 2025-05-13 at 19.57.48_3eb632e6.jpg")  # <-- Replace with your image
reference_img = cv2.cvtColor(reference_img, cv2.COLOR_BGR2RGB)
ref_faces = app.get(reference_img)

if len(ref_faces) == 0:
    print("No face found in reference image.")
else:
    reference_embedding = ref_faces[0].embedding

video_path = "/dinesh123.mp4"  # <-- Replace with your video
cap = cv2.VideoCapture(video_path)

matched = False
frame_count = 0

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = app.get(frame_rgb)

    for face in faces:
        sim = np.dot(reference_embedding, face.embedding) / (
            np.linalg.norm(reference_embedding) * np.linalg.norm(face.embedding)
        )
        if sim > 0.6:  # Threshold can be tuned (0.6–0.8 is common)
            matched = True
            break

    frame_count += 1
    if matched:
        break

cap.release()

import pandas as pd
from datetime import datetime

# Prepare attendance data
status = "Present" if matched else "Absent"
name = "dinesh"
date = datetime.now().strftime("%Y-%m-%d")

attendance = pd.DataFrame([[name, date, status]], columns=["Name", "Date", "Status"])

# Save to Excel file
attendance.to_excel("/content/attendance.xlsx", index=False)
print("Attendance recorded:", status)

