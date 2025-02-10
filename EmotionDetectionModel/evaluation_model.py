import tensorflow as tf
from transformers import DistilBertTokenizer
from preprocess_data import load_and_prepare_data
from sklearn.metrics import classification_report, accuracy_score

def evaluate_model():
    # Load test data
    _, _, test_data, label_encoder = load_and_prepare_data()

    # Define model path
    model_path = "C:/Users/mrpre/OneDrive/Desktop/WEYA/EmotionDetectionModel/models/distilbert-emotion-tf"

    # Load tokenizer
    tokenizer = DistilBertTokenizer.from_pretrained(model_path)

    # Load the model using TensorFlow's SavedModel format
    model = tf.keras.models.load_model(model_path)

    # Tokenize test data
    test_encodings = tokenizer(
        list(test_data["sentence"]),
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors="tf"
    )

    # Convert labels to tensors
    test_labels = test_data["label"].tolist()

    # Prepare TensorFlow dataset
    test_dataset = tf.data.Dataset.from_tensor_slices((
        {"input_ids": test_encodings["input_ids"], "attention_mask": test_encodings["attention_mask"]},
        tf.convert_to_tensor(test_labels)
    )).batch(32)

    # Evaluate model and collect predictions
    all_preds = []
    all_labels = []

    for batch in test_dataset:
        inputs, labels = batch
        logits = model(inputs, training=False)['logits']  # Extract logits properly
        predictions = tf.argmax(logits, axis=1).numpy()

        all_preds.extend(predictions)
        all_labels.extend(labels.numpy())

    # Compute Accuracy
    accuracy = accuracy_score(all_labels, all_preds)
    print(f"Model Accuracy: {accuracy:.4f}")

    # Generate classification report using actual label names
    emotions = list(label_encoder.classes_)  # Get actual class names from label encoder
    report = classification_report(all_labels, all_preds, target_names=emotions)

    print("\nClassification Report:\n")
    print(report)

if __name__ == "__main__":
    evaluate_model()
