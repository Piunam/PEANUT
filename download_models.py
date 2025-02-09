# download_models.py
import urllib.request
import os

def download_models():
    # Define the models directory
    models_dir = 'static/models/'
    
    # Create directory if it doesn't exist
    os.makedirs(models_dir, exist_ok=True)
    
    # List of model files to download
    models = {
        'tiny_face_detector_model-weights_manifest.json': 'https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/tiny_face_detector_model-weights_manifest.json',
        'tiny_face_detector_model-shard1': 'https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/tiny_face_detector_model-shard1',
        'face_landmark_68_model-weights_manifest.json': 'https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_landmark_68_model-weights_manifest.json',
        'face_landmark_68_model-shard1': 'https://raw.githubusercontent.com/justadudewhohacks/face-api.js/master/weights/face_landmark_68_model-shard1'
    }
    
    # Download each model file
    for filename, url in models.items():
        filepath = os.path.join(models_dir, filename)
        if not os.path.exists(filepath):
            print(f'Downloading {filename}...')
            try:
                urllib.request.urlretrieve(url, filepath)
                print(f'Successfully downloaded {filename}')
            except Exception as e:
                print(f'Error downloading {filename}: {str(e)}')

if __name__ == '__main__':
    download_models()


