from transformers import DistilBertTokenizer, TFDistilBertForSequenceClassification
from tensorflow.keras.optimizers.legacy import Adam
import tensorflow as tf
import pandas as pd
from preprocess_data import load_and_prepare_data

# GPU setup: Ensure TensorFlow uses GPU if available
gpus = tf.config.list_physical_devices('GPU')
if gpus:
    try:
        # Set memory growth to avoid consuming all GPU memory
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print("GPU is available and configured.")
    except RuntimeError as e:
        print(f"Error configuring GPU: {e}")
else:
    print("No GPU found. Training will use CPU.")

def train_model():
    # Load data
    train_data, val_data, _, label_encoder = load_and_prepare_data()

    # Load tokenizer and model
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")
    model = TFDistilBertForSequenceClassification.from_pretrained(
        "distilbert-base-uncased", num_labels=len(label_encoder.classes_)
    )

    # Tokenize data
    def tokenize_data(data):
        return tokenizer(
            list(data["sentence"]),
            padding=True,
            truncation=True,
            max_length=128,
            return_tensors="tf"
        )

    train_encodings = tokenize_data(train_data)
    val_encodings = tokenize_data(val_data)

    # Convert labels to tensors
    train_labels = tf.convert_to_tensor(train_data["label"].tolist())
    val_labels = tf.convert_to_tensor(val_data["label"].tolist())

    # Prepare TensorFlow datasets
    train_dataset = tf.data.Dataset.from_tensor_slices(({
        "input_ids": train_encodings["input_ids"],
        "attention_mask": train_encodings["attention_mask"]
    }, train_labels)).shuffle(len(train_data)).batch(16)

    val_dataset = tf.data.Dataset.from_tensor_slices(({
        "input_ids": val_encodings["input_ids"],
        "attention_mask": val_encodings["attention_mask"]
    }, val_labels)).batch(16)

    # Compile model
    model.compile(
        optimizer=Adam(learning_rate=5e-5),
        loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        metrics=["accuracy"]
    )

    # Train model
    model.fit(train_dataset, validation_data=val_dataset, epochs=3)

    # Save the model and tokenizer
    print("Saving the trained model...")
    model.save("../models/distilbert-emotion-tf")
    tokenizer.save_pretrained("../models/distilbert-emotion-tf")
    print("Model and tokenizer saved!")

if __name__ == "__main__":
    train_model()
