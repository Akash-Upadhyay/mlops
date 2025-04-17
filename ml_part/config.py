"""
Configuration parameters for the cat vs dog classifier.
"""

# Dataset parameters
DATA_DIR = "ml_part/data"
TRAIN_DIR = f"{DATA_DIR}/train"
TEST_DIR = f"{DATA_DIR}/test"
VALIDATION_SPLIT = 0.2
BATCH_SIZE = 32

# Image parameters
IMG_HEIGHT = 150
IMG_WIDTH = 150
CHANNELS = 3

# Model parameters
EPOCHS = 1
LEARNING_RATE = 0.001
OPTIMIZER = "adam"
NUM_CLASSES = 2  # Cat and Dog

# Training parameters
EARLY_STOPPING_PATIENCE = 3
CHECKPOINT_PATH = "ml_part/checkpoints/model.h5"

# Random seed for reproducibility
RANDOM_SEED = 42 