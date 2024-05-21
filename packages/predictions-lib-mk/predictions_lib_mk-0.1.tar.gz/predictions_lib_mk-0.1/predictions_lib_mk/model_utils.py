import os
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
from tensorflow.keras.applications import DenseNet121
from tensorflow.keras.layers import Dense, Input, concatenate
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint

def extract_and_process_data(input_directory, output_file, num_images=500):
    output_data = np.loadtxt(output_file, delimiter=' ')
    output_dict = {int(event): v2 for event, v2 in output_data}

    images = []
    e2_values = []
    v2_values = []

    print("Event Number | E2 Value | Array Data Shape | v2 Value")
    image_files = sorted(os.listdir(input_directory))[:num_images]
    for filename in image_files:
        with open(os.path.join(input_directory, filename), 'r') as f:
            content = f.readlines()
            e2 = float(content[4].split('=')[1].strip())
            event_number = int(filename.split('.')[0])
            array_data = np.array([list(map(float, row.split())) for row in content[11:132]])

            if event_number in output_dict:
                v2 = output_dict[event_number]
                print(f"{event_number:<13}| {e2:<9}| {array_data.shape} | {v2}")
                images.append(array_data)
                e2_values.append(e2)
                v2_values.append(v2)

    images = np.array(images)
    e2_values = np.array(e2_values)
    v2_values = np.array(v2_values)
    return images, e2_values, v2_values

def create_rgb_images(grayscale_data):
    rgb_images = np.stack([grayscale_data] * 3, axis=-1)
    return rgb_images

def normalize_data(data):
    normalized_images = np.array([(img - img.min()) / (img.max() - img.min()) for img in data])
    return normalized_images

def integrate_e2_with_images(images, e2_values):
    e2_layers = e2_values[:, np.newaxis, np.newaxis, np.newaxis]
    e2_layers = np.repeat(e2_layers, images.shape[1], axis=1)
    e2_layers = np.repeat(e2_layers, images.shape[2], axis=2)
    return np.concatenate([images, e2_layers], axis=-1)

def load_new_data(file_path):
    with open(file_path, 'r') as f:
        content = f.readlines()
        e2_value = float(content[0].strip())
        array_data = np.array([list(map(float, row.split())) for row in content[1:]])
    return array_data, e2_value

def predict_new_data(model_path, new_files):
    model = load_model(model_path)

    new_array_data_list = []
    new_e2_value_list = []
    for file_path in new_files:
        array_data, e2_value = load_new_data(file_path)
        new_array_data_list.append(array_data)
        new_e2_value_list.append(e2_value)

    new_array_data = np.array(new_array_data_list)
    new_e2_values = np.array(new_e2_value_list)

    new_rgb_images = normalize_data(np.array([create_rgb_images(img) for img in new_array_data]))
    new_integrated_images = integrate_e2_with_images(new_rgb_images, new_e2_values)

    predictions = model.predict([new_integrated_images, new_e2_values])
    return predictions.flatten()

def plot_comparison_graph(predicted_v2, actual_v2, title):
    mean_v2 = np.mean(actual_v2)
    delta_v2_squared = (actual_v2 - predicted_v2) ** 2
    average_delta_v2_squared = np.mean(delta_v2_squared)

    sorted_indices = np.argsort(predicted_v2)
    sorted_predicted_v2 = predicted_v2[sorted_indices]
    sorted_delta_v2_squared = delta_v2_squared[sorted_indices]

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel('v2 (Hydro)')
    ax1.set_ylabel('<Δv2>²', color=color)
    ax1.plot(sorted_predicted_v2, sorted_delta_v2_squared, 'k--')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()

    color = 'tab:blue'
    ax2.set_ylabel('<v2>', color=color)
    ax2.plot(sorted_predicted_v2, sorted_predicted_v2, 'k-')
    ax2.tick_params(axis='y', labelcolor=color)

    ax2.text(0.05, 0.95, f'<v2> = {mean_v2:.4f}', transform=ax2.transAxes, fontsize=14, verticalalignment='top')

    fig.tight_layout()
    plt.title(title)
    plt.show()

def plot_error_histogram(actual_v2, predicted_v2):
    errors = actual_v2 - predicted_v2
    plt.hist(errors, bins=50, edgecolor='black', alpha=0.75)
    plt.title('Histogram of Prediction Errors')
    plt.xlabel('Prediction Error')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

def save_results_to_file(actual_v2, predicted_v2, filename='resultsDense.txt'):
    with open(filename, 'w') as f:
        for real, pred in zip(actual_v2, predicted_v2):
            difference = real - pred
            f.write(f"Real: {real}, Predicted: {pred}, Difference: {difference}\n")
