import librosa
import numpy as np
import os
import soundfile as sf
from src.utils import save_file, load_file, generate_key_file

def generate_chaotic_sequence(seed, size):
    x = seed
    sequence = []
    for i in range(size):
        x = 3.999 * x * (1 - x)
        sequence.append(x)
    return np.array(sequence)

def encrypt_audio(input_file):
    try:
        audio, sr = librosa.load(input_file, sr=None)

        seed = np.random.uniform(0.001, 0.999)
        chaotic_sequence = generate_chaotic_sequence(seed, len(audio))

        
        encrypted_time = audio + chaotic_sequence * 0.7 

        
        stft = librosa.stft(encrypted_time)
        chaotic_freq = generate_chaotic_sequence(seed, stft.shape[0] * stft.shape[1]).reshape(stft.shape)
        encrypted_stft = stft + chaotic_freq * 0.5 

        
        encrypted_audio = librosa.istft(encrypted_stft)

        
        encrypted_file = "encrypted_data/audio_encrypted.wav"
        os.makedirs(os.path.dirname(encrypted_file), exist_ok=True)
        sf.write(encrypted_file, encrypted_audio, sr)

        
        key_file = generate_key_file("audio")
        save_file(str(seed).encode('utf-8'), key_file)

        return encrypted_file, key_file

    except Exception as e:
        raise RuntimeError(f"Error during audio encryption: {e}")

def decrypt_audio(encrypted_file, key_file):
    try:
        encrypted_audio, sr = librosa.load(encrypted_file, sr=None)
        
        seed = float(load_file(key_file).decode('utf-8'))

        
        chaotic_sequence = generate_chaotic_sequence(seed, len(encrypted_audio))

        
        decrypted_time = encrypted_audio - chaotic_sequence * 0.7

        
        stft = librosa.stft(decrypted_time)
        chaotic_freq = generate_chaotic_sequence(seed, stft.shape[0] * stft.shape[1]).reshape(stft.shape)
        decrypted_stft = stft - chaotic_freq * 0.5

        
        decrypted_audio = librosa.istft(decrypted_stft)

        
        decrypted_file = "decrypted_data/audio_decrypted.wav"
        os.makedirs(os.path.dirname(decrypted_file), exist_ok=True)
        sf.write(decrypted_file, decrypted_audio, sr)

        return decrypted_file

    except Exception as e:
        raise RuntimeError(f"Error during audio decryption: {e}")