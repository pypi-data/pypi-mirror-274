# neural_network_predict/predict.py
import tensorflow as tf
import numpy as np
import os

DEFAULT_MODEL_PATH = os.path.join(os.path.dirname(__file__), 'modelv111.h5')
DEFAULT_DATA_FILE = os.path.join(os.path.dirname(__file__), 'new_data1.txt')

def load_new_data(file_path):
    with open(file_path, 'r') as f:
        content = f.readlines()
        e2_value = float(content[0].strip())
        array_data = np.array([list(map(float, row.split())) for row in content[1:]])
    return array_data, e2_value

def create_rgb_images(grayscale_data):
    return np.stack([grayscale_data] * 3, axis=-1)

def normalize_data(data):
    normalized_images = []
    for img in data:
        min_val = img.min()
        max_val = img.max()
        if max_val == min_val:  # Avoid division by zero
            normalized_img = np.zeros_like(img)
        else:
            normalized_img = (img - min_val) / (max_val - min_val)
        normalized_images.append(normalized_img)
    return np.array(normalized_images)

def integrate_e2_with_images(images, e2_values):
    e2_layers = e2_values[:, np.newaxis, np.newaxis, np.newaxis]
    e2_layers = np.repeat(e2_layers, images.shape[1], axis=1)
    e2_layers = np.repeat(e2_layers, images.shape[2], axis=2)
    return np.concatenate([images, e2_layers], axis=-1)

def predict_new_data(model_path=DEFAULT_MODEL_PATH, new_file=DEFAULT_DATA_FILE):
    array_data, e2_value = load_new_data(new_file)
    new_rgb_image = normalize_data(create_rgb_images(array_data))
    new_integrated_image = integrate_e2_with_images(np.array([new_rgb_image]), np.array([e2_value]))

    model = tf.keras.models.load_model(model_path)  # Load the model
    prediction = model.predict(new_integrated_image)
    return prediction.flatten()

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Predict v2 values for new data")
    parser.add_argument('--model_path', type=str, default=DEFAULT_MODEL_PATH, help="Path to the trained model file")
    parser.add_argument('--new_data_file', type=str, default=DEFAULT_DATA_FILE, help="Path to the new data file")

    args = parser.parse_args()

    predictions = predict_new_data(args.model_path, args.new_data_file)
    print("Predicted v2 values for new data:")
    print(predictions)

if __name__ == "__main__":
    main()
