from transformers import DistilBertConfig
import json

# Define the number of labels based on your training data
num_labels = 6  # Update this to match your dataset

# Create a DistilBert configuration
config = DistilBertConfig(
    num_labels=num_labels,
    id2label={str(i): label for i, label in enumerate(["Sadness", "Joy", "Love", "Anger", "Fear", "Surprise"])},  # Update labels
    label2id={label: str(i) for i, label in enumerate(["Sadness", "Joy", "Love", "Anger", "Fear", "Surprise"])}
)

# Save the config.json file
config_path = "C:/Users/mrpre/OneDrive/Desktop/WEYA/EmotionDetectionModel/models/distilbert-emotion-tf/config.json"

with open(config_path, "w") as f:
    json.dump(config.to_dict(), f, indent=4)

print(f"✅ config.json successfully created at {config_path}")
