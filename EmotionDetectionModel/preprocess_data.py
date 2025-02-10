import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Define the target labels for alignment
label_mapping = {
    "anger": "3",
    "fear": "4",
    "joy": "1",
    "love": "2",
    "sadness": "0",
    "surprise": "5"
}
TARGET_LABELS = list(label_mapping.keys())  # ["sadness", "joy", "love", "anger", "fear", "surprise"]

def load_and_prepare_data():
    # Load GoEmotions dataset
    print("Loading GoEmotions dataset...")
    go_emotions = pd.read_csv(
        "C:/Users/mrpre/OneDrive/Desktop/WEYA/EmotionDetectionModel/data/go_emotions_dataset.csv"
    )
    
    # Check available columns in GoEmotions
    print(f"GoEmotions Columns: {go_emotions.columns}")
    
    # Combine emotion columns into a single "label" column
    print("Processing GoEmotions dataset...")
    emotion_columns = ["sadness", "joy", "love", "anger", "fear", "surprise"]  # Only target emotions
    go_emotions = go_emotions[["text"] + emotion_columns]
    go_emotions["label"] = go_emotions[emotion_columns].idxmax(axis=1)
    
    # Keep only the "text" and "label" columns
    go_emotions = go_emotions[["text", "label"]].dropna()
    go_emotions.rename(columns={"text": "sentence"}, inplace=True)
    
    # Map labels to align with Emotions dataset
    go_emotions["label"] = go_emotions["label"].map(label_mapping)
    go_emotions = go_emotions.dropna()  # Drop rows where mapping failed
    print(f"Filtered and aligned GoEmotions dataset: {len(go_emotions)} rows.")
    
    # Load Emotions dataset
    print("Loading Emotions dataset...")
    emotions = pd.read_csv(
        "C:/Users/mrpre/OneDrive/Desktop/WEYA/EmotionDetectionModel/data/emotions.csv"
    )
    
    # Ensure columns are named consistently
    emotions.rename(columns={"text": "sentence"}, inplace=True)
    print(f"Processed Emotions dataset: {len(emotions)} rows.")
    
    # Combine datasets
    print("Combining datasets...")
    combined_data = pd.concat([go_emotions, emotions], ignore_index=True)
    print(f"Combined dataset has {len(combined_data)} rows.")
    
    # Ensure all labels are strings
    combined_data["label"] = combined_data["label"].astype(str)  # Convert all labels to strings
    
    # Encode labels as integers
    print("Encoding labels...")
    label_encoder = LabelEncoder()
    combined_data["label"] = label_encoder.fit_transform(combined_data["label"])
    print(f"Labels encoded as integers. Classes: {list(label_encoder.classes_)}")
    
    # Split data into train, validation, and test sets
    print("Splitting datasets...")
    train_data, temp_data = train_test_split(combined_data, test_size=0.2, random_state=42)
    val_data, test_data = train_test_split(temp_data, test_size=0.5, random_state=42)
    
    print(f"Training Set: {len(train_data)} samples")
    print(f"Validation Set: {len(val_data)} samples")
    print(f"Test Set: {len(test_data)} samples")
    
    return train_data, val_data, test_data, label_encoder

if __name__ == "__main__":
    train_data, val_data, test_data, label_encoder = load_and_prepare_data()
    
    # Save processed datasets
    print("Saving datasets...")
    train_data.to_csv("data/train_data.csv", index=False)
    val_data.to_csv("data/val_data.csv", index=False)
    test_data.to_csv("data/test_data.csv", index=False)

    # Save label encoder classes
    label_classes = pd.DataFrame({"label": label_encoder.classes_})
    label_classes.to_csv("data/label_classes.csv", index=False)

    print("Datasets and label classes saved successfully.")
