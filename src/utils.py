import os

def save_file(data, path):
    f = open(path, 'wb')
    f.write(data)
    f.close()

def load_file(path):
    f = open(path, 'rb')
    data = f.read()
    f.close()
    return data

def generate_key_file(data_type):
    key_path = f"keys/{data_type}_key.bin"
    return key_path
