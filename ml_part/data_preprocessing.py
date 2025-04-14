"""
Data downloading and preprocessing for the cat vs dog classifier.
"""

import os
import zipfile
import requests
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import shutil
from pathlib import Path
import config
from PIL import Image

# def download_dataset():
#     """
#     Downloads the cats and dogs dataset from Kaggle.
#     You need to have a kaggle.json file in your ~/.kaggle directory.
#     """
#     # Create data directory if it doesn't exist
#     os.makedirs(config.DATA_DIR, exist_ok=True)
#     
#     # Dataset URL (Kaggle's "Dogs vs. Cats" dataset)
#     # We'll use the Microsoft's dataset which is publicly available
#     url = "https://download.microsoft.com/download/3/E/1/3E1C3F21-ECDB-4869-8368-6DEBA77B919F/kagglecatsanddogs_5340.zip"
#     
#     print("Downloading cats and dogs dataset...")
#     response = requests.get(url, stream=True)
#     zip_path = os.path.join(config.DATA_DIR, "cats_and_dogs.zip")
#     
#     with open(zip_path, "wb") as f:
#         for chunk in response.iter_content(chunk_size=1024):
#             if chunk:
#                 f.write(chunk)
#     
#     # Extract the dataset
#     print("Extracting dataset...")
#     with zipfile.ZipFile(zip_path, 'r') as zip_ref:
#         zip_ref.extractall(config.DATA_DIR)
#     
#     # Remove the zip file to save space
#     os.remove(zip_path)
#     print("Dataset downloaded and extracted.")

def is_valid_image(file_path):
    """
    Check if an image file is valid by attempting to open it with PIL.
    
    Args:
        file_path: Path to the image file
        
    Returns:
        bool: True if the image is valid, False otherwise
    """
    try:
        img = Image.open(file_path)
        img.verify()  # Verify that the image is not corrupted
        img.close()
        
        # Also try to load the image to catch additional errors
        img = Image.open(file_path)
        img.load()
        img.close()
        return True
    except Exception as e:
        print(f"Invalid image found: {file_path} - Error: {str(e)}")
        return False

def organize_dataset():
    """
    Organizes the dataset into train and test directories with class subdirectories.
    Filters out corrupt images.
    """
    # Create train and test directories
    os.makedirs(config.TRAIN_DIR, exist_ok=True)
    os.makedirs(config.TEST_DIR, exist_ok=True)
    
    # Create class directories
    for dir_name in ["cats", "dogs"]:
        os.makedirs(os.path.join(config.TRAIN_DIR, dir_name), exist_ok=True)
        os.makedirs(os.path.join(config.TEST_DIR, dir_name), exist_ok=True)
    
    # Path to the extracted dataset
    extracted_dir = os.path.join(config.DATA_DIR, "PetImages")
    
    # Count statistics
    total_files = 0
    valid_files = 0
    invalid_files = 0
    
    # Move files to train and test directories
    for class_name in ["Cat", "Dog"]:
        class_dir = os.path.join(extracted_dir, class_name)
        target_class_name = class_name.lower() + "s"
        
        # List all files in the class directory
        all_files = os.listdir(class_dir)
        total_files += len(all_files)
        
        # Filter out invalid images
        valid_files_list = []
        for file in all_files:
            file_path = os.path.join(class_dir, file)
            if is_valid_image(file_path):
                valid_files_list.append(file)
                valid_files += 1
            else:
                invalid_files += 1
        
        print(f"Found {len(valid_files_list)} valid {class_name} images out of {len(all_files)}")
        
        # Shuffle the valid files
        np.random.seed(config.RANDOM_SEED)
        np.random.shuffle(valid_files_list)
        
        # Split files into train and test
        split_idx = int(len(valid_files_list) * 0.8)  # 80% train, 20% test
        train_files = valid_files_list[:split_idx]
        test_files = valid_files_list[split_idx:]
        
        # Copy files to train directory
        for file in train_files:
            src = os.path.join(class_dir, file)
            dst = os.path.join(config.TRAIN_DIR, target_class_name, file)
            try:
                shutil.copy(src, dst)
            except:
                print(f"Error copying {src}")
        
        # Copy files to test directory
        for file in test_files:
            src = os.path.join(class_dir, file)
            dst = os.path.join(config.TEST_DIR, target_class_name, file)
            try:
                shutil.copy(src, dst)
            except:
                print(f"Error copying {src}")
    
    print(f"Dataset organized into train and test directories.")
    print(f"Total files: {total_files}, Valid: {valid_files}, Invalid: {invalid_files}")

def create_data_generators():
    """
    Creates and returns train and test data generators.
    
    Returns:
        tuple: (train_generator, test_generator)
    """
    # Data augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        validation_split=config.VALIDATION_SPLIT
    )
    
    # Only rescaling for testing
    test_datagen = ImageDataGenerator(rescale=1./255)
    
    # Training generator with validation split
    train_generator = train_datagen.flow_from_directory(
        config.TRAIN_DIR,
        target_size=(config.IMG_HEIGHT, config.IMG_WIDTH),
        batch_size=config.BATCH_SIZE,
        class_mode='binary',
        subset='training'
    )
    
    # Validation generator
    validation_generator = train_datagen.flow_from_directory(
        config.TRAIN_DIR,
        target_size=(config.IMG_HEIGHT, config.IMG_WIDTH),
        batch_size=config.BATCH_SIZE,
        class_mode='binary',
        subset='validation'
    )
    
    # Test generator
    test_generator = test_datagen.flow_from_directory(
        config.TEST_DIR,
        target_size=(config.IMG_HEIGHT, config.IMG_WIDTH),
        batch_size=config.BATCH_SIZE,
        class_mode='binary'
    )
    
    return train_generator, validation_generator, test_generator

def prepare_dataset():
    """
    Main function to prepare the dataset.
    """
    # Dataset is now pulled using DVC pull instead of downloading
    # Ensure data directories exist
    os.makedirs(config.TRAIN_DIR, exist_ok=True)
    os.makedirs(config.TEST_DIR, exist_ok=True)
    
    # If the dataset is not organized, organize it
    if not os.path.exists(os.path.join(config.TRAIN_DIR, "cats")) or not os.path.exists(os.path.join(config.TRAIN_DIR, "dogs")):
        print("Organizing dataset...")
        organize_dataset()
    else:
        print("Dataset already organized.")
    
    return create_data_generators()

if __name__ == "__main__":
    prepare_dataset() 