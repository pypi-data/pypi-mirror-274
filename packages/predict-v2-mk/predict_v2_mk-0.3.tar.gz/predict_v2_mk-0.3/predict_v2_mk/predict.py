import tensorflow as tf
import numpy as np
import argparse
import os

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

def predict_new_data(model_path, new_file):
    array_data, e2_value = load_new_data(new_file)
    new_rgb_image = normalize_data(create_rgb_images(array_data))
    new_integrated_image = integrate_e2_with_images(np.array([new_rgb_image]), np.array([e2_value]))

    model = tf.keras.models.load_model(model_path, compile=False)  # Load the model without compiling
    prediction = model.predict([new_integrated_image, np.array([e2_value])])
    return prediction.flatten()

def main():
    parser = argparse.ArgumentParser(description='Predict new data using a pre-trained model.')
    parser.add_argument('new_data_file', type=str, nargs='?', default='new_data1.txt', help='Path to the new data file')
    parser.add_argument('--model_path', type=str, default='modelv111.h5', help='Path to the model file')
    args = parser.parse_args()

    predictions = predict_new_data(args.model_path, args.new_data_file)
    print("Predicted v2 values for new data:")
    print(predictions)

if __name__ == '__main__':
    main()
