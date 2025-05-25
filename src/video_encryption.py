import cv2
import numpy as np
import os
from src.utils import save_file, load_file, generate_key_file


def generate_chaotic_sequence(seed, size):
    x = seed
    sequence = np.empty(size, dtype=np.float32)
    for i in range(size):
        x = 3.999 * x * (1 - x)
        sequence[i] = x
    return (sequence * 255).astype(np.uint8)


def encrypt_video(input_file):
    cap = cv2.VideoCapture(input_file)
    if not cap.isOpened():
        raise RuntimeError("Unable to open video file.")

    
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    
    encrypted_file = "encrypted_data/video_encrypted.mp4"
    os.makedirs(os.path.dirname(encrypted_file), exist_ok=True)
    out = cv2.VideoWriter(encrypted_file, fourcc, fps, (frame_width, frame_height))

    
    seed = np.random.uniform(0.001, 0.999)
    chaotic_sequence = generate_chaotic_sequence(seed, frame_width * frame_height * 3)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

       
        flat_frame = frame.flatten()
        encrypted_flat_frame = np.bitwise_xor(flat_frame, chaotic_sequence[:flat_frame.size])

        
        encrypted_flat_frame = np.clip(encrypted_flat_frame, 0, 255).astype(np.uint8)

        
        encrypted_frame = encrypted_flat_frame.reshape(frame.shape)

        out.write(encrypted_frame)

    cap.release()
    out.release()

    
    key_file = generate_key_file("video")
    save_file(str(seed).encode('utf-8'), key_file)

    return encrypted_file, key_file


def decrypt_video(encrypted_file, key_file):
    cap = cv2.VideoCapture(encrypted_file)
    if not cap.isOpened():
        raise RuntimeError("Unable to open encrypted video file.")


    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    
    decrypted_file = "decrypted_data/video_decrypted.mp4"
    os.makedirs(os.path.dirname(decrypted_file), exist_ok=True)
    out = cv2.VideoWriter(decrypted_file, fourcc, fps, (frame_width, frame_height))

    
    seed = float(load_file(key_file).decode('utf-8'))
    chaotic_sequence = generate_chaotic_sequence(seed, frame_width * frame_height * 3)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        
        flat_frame = frame.flatten()
        decrypted_flat_frame = np.bitwise_xor(flat_frame, chaotic_sequence[:flat_frame.size])

        
        decrypted_flat_frame = np.clip(decrypted_flat_frame, 0, 255).astype(np.uint8)

        
        decrypted_frame = decrypted_flat_frame.reshape(frame.shape)

        out.write(decrypted_frame)

    cap.release()
    out.release()

    return decrypted_file
