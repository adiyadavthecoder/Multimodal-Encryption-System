import cv2
import numpy as np
import os
from src.utils import save_file, load_file, generate_key_file


def logistic_map(seed, size):
    x = seed
    sequence = []
    for i in range(size):
        x = 3.999 * x * (1 - x)
        sequence.append(x)
    return np.array(sequence)


def encrypt_image(input_file):
    try:
        image = cv2.imread(input_file)
        if image is None:
            raise ValueError("Invalid image file or path.")

        
        height, width, channels = image.shape
        total_pixels = height * width * channels

        
        seed = np.random.uniform(0.001, 0.999)
        chaotic_sequence = logistic_map(seed, total_pixels)
        chaotic_sequence = (chaotic_sequence * 255).astype(np.uint8)

        
        chaotic_image = chaotic_sequence.reshape(height, width, channels)

        
        encrypted_image = cv2.bitwise_xor(image, chaotic_image)

        
        encrypted_file = "encrypted_data/image_encrypted.png"
        os.makedirs(os.path.dirname(encrypted_file), exist_ok=True)
        cv2.imwrite(encrypted_file, encrypted_image)

        
        key_file = generate_key_file("image")
        save_file(str(seed).encode('utf-8'), key_file)

        return encrypted_file, key_file

    except Exception as e:
        raise RuntimeError(f"Error during image encryption: {e}")


def decrypt_image(encrypted_file, key_file):
    try:
        encrypted_image = cv2.imread(encrypted_file)
        if encrypted_image is None:
            raise ValueError("Invalid encrypted image file or path.")

       
        seed = float(load_file(key_file).decode('utf-8'))

        
        height, width, channels = encrypted_image.shape
        total_pixels = height * width * channels

        
        chaotic_sequence = logistic_map(seed, total_pixels)
        chaotic_sequence = (chaotic_sequence * 255).astype(np.uint8)

        
        chaotic_image = chaotic_sequence.reshape(height, width, channels)

        
        decrypted_image = cv2.bitwise_xor(encrypted_image, chaotic_image)

        
        decrypted_file = "decrypted_data/image_decrypted.png"
        os.makedirs(os.path.dirname(decrypted_file), exist_ok=True)
        cv2.imwrite(decrypted_file, decrypted_image)

        return decrypted_file

    except Exception as e:
        raise RuntimeError(f"Error during image decryption: {e}")
