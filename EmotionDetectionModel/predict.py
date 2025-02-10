from transformers import DistilBertTokenizer
import tensorflow as tf

# Define the model path
model_path = "C:/Users/mrpre/OneDrive/Desktop/WEYA/EmotionDetectionModel/models/distilbert-emotion-tf"

# Load tokenizer
tokenizer = DistilBertTokenizer.from_pretrained(model_path)

# Load the model correctly
model = tf.saved_model.load(model_path)

# Define emotion labels (Ensure this matches your training labels!)
emotions = ["Sadness", "Joy", "Love", "Anger", "Fear", "Surprise"]

def predict_emotion(text):
    # Tokenize the input text
    inputs = tokenizer(
        text,
        padding=True,
        truncation=True,
        max_length=128,
        return_tensors="tf"
    )

    # Make predictions
    logits = model(inputs, training=False)  # Ensure inference mode
    predicted_class = tf.argmax(logits['logits'], axis=1).numpy()[0]  # ✅ Extract logits correctly

    return emotions[predicted_class]

if __name__ == "__main__":
    while True:
        user_input = input("\n🔹 Enter a sentence (or type 'exit' to quit): ")
        
        if user_input.lower() == "exit":
            print("👋 Exiting program. Have a great day!")
            break
        
        predicted_emotion = predict_emotion(user_input)
        print(f"📝 Text: {user_input}")
        print(f"🎭 Predicted Emotion: {predicted_emotion}")
