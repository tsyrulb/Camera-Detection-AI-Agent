# detection.py
#
# Demonstrates how you'd integrate MediaPipe (Hands) + MiDaS for depth,
# returning a 3D coordinate (rocket_x, rocket_y, rocket_z).

import cv2
import torch
import numpy as np


import mediapipe as mp

from config import (
    ROOM_MIN_X, ROOM_MAX_X,
    ROOM_MIN_Y, ROOM_MAX_Y,
    ROOM_MIN_Z, ROOM_MAX_Z
)

# ------------------ Setup MediaPipe Hands ------------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5,
)
mp_drawing = mp.solutions.drawing_utils

# ------------------ Setup MiDaS ------------------
model_type = "MiDaS_small"
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Using device for MiDaS:", device)

midas = torch.hub.load("intel-isl/MiDaS", model_type)
midas.to(device)
midas.eval()

midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")
transform = midas_transforms.small_transform

def detect_hand_3D(cap, old_xyz):
    """
    1) Grab a webcam frame
    2) Use MediaPipe to find wrist in 2D
    3) Use MiDaS to get depth map
    4) Convert (pixel_x, pixel_y, depth) -> (rocket_x, rocket_y, rocket_z)
    5) Return new (rocket_x, rocket_y, rocket_z)

    If detection fails => keep old_xyz.
    """
    rocket_x, rocket_y, rocket_z = old_xyz

    ret, frame = cap.read()
    if not ret:
        # No new frame => keep old coords
        return (rocket_x, rocket_y, rocket_z)

    frame = cv2.flip(frame, 1)
    frame_h, frame_w = frame.shape[:2]

    # 1) MediaPipe Hands
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    wrist_x_pix = None
    wrist_y_pix = None
    if results.multi_hand_landmarks:
        # Take first hand
        hand_landmarks = results.multi_hand_landmarks[0]
        # Wrist
        wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
        wrist_x_pix = int(wrist.x * frame_w)
        wrist_y_pix = int(wrist.y * frame_h)

    # 2) MiDaS => depth map
    frame_rgb2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    input_batch = transform(frame_rgb2).to(device)

    with torch.no_grad():
        prediction = midas(input_batch)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=frame_rgb2.shape[:2],
            mode="bicubic",
            align_corners=False
        ).squeeze()
    depth_map = prediction.cpu().numpy()
    depth_map = cv2.resize(depth_map, (frame_w, frame_h))
    depth_map = cv2.normalize(depth_map, None, 0, 1, cv2.NORM_MINMAX, cv2.CV_32F)

    # 3) If we have a wrist => compute rocket coords
    if wrist_x_pix is not None and wrist_y_pix is not None:
        depth_value = depth_map[
            min(max(0, wrist_y_pix), frame_h-1),
            min(max(0, wrist_x_pix), frame_w-1)
        ]
        # Example: invert depth so 0 => far, 1 => near, then map to ROOM's Z range
        rocket_z = ROOM_MIN_Z + (1.0 - depth_value) * (ROOM_MAX_Z - ROOM_MIN_Z)
        # X range
        rocket_x = ROOM_MIN_X + (wrist_x_pix / frame_w) * (ROOM_MAX_X - ROOM_MIN_X)
        # Y range (inverting so top is maxY)
        rocket_y = ROOM_MAX_Y - (wrist_y_pix / frame_h) * (ROOM_MAX_Y - ROOM_MIN_Y)

    return (rocket_x, rocket_y, rocket_z)
