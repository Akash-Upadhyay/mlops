"""
Model definition and training for cat vs dog classifier.
"""

import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import matplotlib.pyplot as plt
import numpy as np
import json
import config
from tensorflow.keras.preprocessing.image import ImageDataGenerator

def create_model():
    """
    Creates and returns a CNN model for image classification.
    
    Returns:
        model: A compiled Keras model
    """
    # Create directory for checkpoints
    os.makedirs(os.path.dirname(config.CHECKPOINT_PATH), exist_ok=True)
    
    # Define the model architecture
    model = Sequential([
        # First convolutional layer
        Conv2D(32, (3, 3), activation='relu', input_shape=(config.IMG_HEIGHT, config.IMG_WIDTH, config.CHANNELS)),
        MaxPooling2D(2, 2),
        
        # Second convolutional layer
        Conv2D(64, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        
        # Third convolutional layer
        Conv2D(128, (3, 3), activation='relu'),
        MaxPooling2D(2, 2),
        
        # Flatten and fully connected layers
        Flatten(),
        Dense(512, activation='relu'),
        Dropout(0.5),  # Dropout for regularization
        Dense(1, activation='sigmoid')  # Binary classification (cat or dog)
    ])
    
    # Compile the model
    model.compile(
        optimizer=tf.keras.optimizers.get(config.OPTIMIZER),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    # Print model summary
    model.summary()
    
    return model

def create_data_generators():
    """
    Creates and returns data generators for training, validation, and testing.
    
    Returns:
        tuple: (train_generator, validation_generator, test_generator)
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

def train_model(model, train_generator, validation_generator):
    """
    Trains the model using the provided data generators.
    
    Args:
        model: Compiled Keras model
        train_generator: Training data generator
        validation_generator: Validation data generator
    
    Returns:
        history: Training history
    """
    # Define callbacks
    callbacks = [
        EarlyStopping(
            monitor='val_loss',
            patience=config.EARLY_STOPPING_PATIENCE,
            restore_best_weights=True
        ),
        ModelCheckpoint(
            filepath=config.CHECKPOINT_PATH,
            monitor='val_accuracy',
            save_best_only=True,
            verbose=1
        )
    ]
    
    # Train the model
    history = model.fit(
        train_generator,
        epochs=config.EPOCHS,
        validation_data=validation_generator,
        callbacks=callbacks
    )
    
    return history

def evaluate_model(model, test_generator):
    """
    Evaluates the model on the test data.
    
    Args:
        model: Trained Keras model
        test_generator: Test data generator
    
    Returns:
        results: Evaluation results dictionary
    """
    # Evaluate the model
    test_loss, test_accuracy = model.evaluate(test_generator)
    
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
    
    # Return results as a dictionary
    return {
        "test_loss": float(test_loss),
        "test_accuracy": float(test_accuracy)
    }

def plot_training_history(history):
    """
    Plots the training and validation accuracy/loss.
    
    Args:
        history: Training history
    """
    # Create directory for plots
    os.makedirs("ml_part/plots", exist_ok=True)
    
    # Plot training & validation accuracy
    plt.figure(figsize=(12, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    
    # Plot training & validation loss
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    
    plt.tight_layout()
    plt.savefig('ml_part/plots/training_history.png')
    plt.close()
    
    # Save accuracy and loss history as separate plots for DVC
    # Accuracy plot
    plt.figure(figsize=(10, 6))
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Model Accuracy')
    plt.ylabel('Accuracy')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.grid(True)
    plt.savefig('ml_part/plots/accuracy.png')
    plt.close()
    
    # Loss plot
    plt.figure(figsize=(10, 6))
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model Loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Validation'], loc='upper left')
    plt.grid(True)
    plt.savefig('ml_part/plots/loss.png')
    plt.close()

def save_metrics(train_history, eval_results):
    """
    Save metrics in JSON format for DVC tracking.
    
    Args:
        train_history: Training history object
        eval_results: Evaluation results dictionary
    """
    # Extract final values from training history
    final_epoch = len(train_history.history['accuracy'])
    train_accuracy = float(train_history.history['accuracy'][-1])
    val_accuracy = float(train_history.history['val_accuracy'][-1])
    train_loss = float(train_history.history['loss'][-1])
    val_loss = float(train_history.history['val_loss'][-1])
    
    # Create metrics dictionary
    metrics = {
        "training": {
            "epochs_completed": final_epoch,
            "final_accuracy": train_accuracy,
            "final_loss": train_loss
        },
        "validation": {
            "final_accuracy": val_accuracy,
            "final_loss": val_loss
        },
        "testing": {
            "accuracy": eval_results["test_accuracy"],
            "loss": eval_results["test_loss"]
        },
        "parameters": {
            "img_height": config.IMG_HEIGHT,
            "img_width": config.IMG_WIDTH,
            "batch_size": config.BATCH_SIZE,
            "learning_rate": config.LEARNING_RATE,
            "max_epochs": config.EPOCHS
        }
    }
    
    # Save metrics to JSON file
    with open('ml_part/metrics.json', 'w') as f:
        json.dump(metrics, f, indent=4)
        
    print(f"Metrics saved to ml_part/metrics.json")

def main():
    """
    Main function to run the training pipeline.
    """
    # Set random seeds for reproducibility
    tf.random.set_seed(config.RANDOM_SEED)
    np.random.seed(config.RANDOM_SEED)
    
    # Create the model
    print("Creating model...")
    model = create_model()
    
    # Create data generators (assumes data_preprocessing.py has already been run)
    print("Creating data generators...")
    train_generator, validation_generator, test_generator = create_data_generators()
    
    # Train the model
    print("Training model...")
    history = train_model(model, train_generator, validation_generator)
    
    # Evaluate the model
    print("Evaluating model...")
    eval_results = evaluate_model(model, test_generator)
    
    # Plot training history
    plot_training_history(history)
    
    # Save metrics for DVC
    save_metrics(history, eval_results)
    
    print(f"Model saved to {config.CHECKPOINT_PATH}")
    print("Training complete!")

if __name__ == "__main__":
    main() 