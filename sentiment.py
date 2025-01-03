import tkinter as tk
from tkinter import messagebox
from nltk.sentiment import SentimentIntensityAnalyzer
import re
import nltk
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, classification_report

# Download necessary VADER lexicon from NLTK
nltk.download('vader_lexicon')

# Initialize the VADER sentiment analyzer
sia = SentimentIntensityAnalyzer()

# Function to calculate sentiment for a given text
def get_sentiment(text):
    score = sia.polarity_scores(text)
    if score['compound'] >= 0.05:
        return 'positive'
    elif score['compound'] <= -0.05:
        return 'negative'
    else:
        return 'neutral'

# Function to analyze sentiment for an entire conversation and track emotional flow
def analyze_sentiment():
    # Get input from the text box
    conversation_text = conversation_entry.get("1.0", "end-1c")
    
    # Check if the conversation is empty
    if not conversation_text.strip():
        messagebox.showerror("Input Error", "Please enter the conversation text.")
        return

    # Split the conversation into turns based on speaker labels
    turns = split_conversation(conversation_text)

    # Initialize dialogue storage for Person A and Person B
    person_a_dialogue = []
    person_b_dialogue = []

    # Separate the dialogue for Person A and Person B
    for turn in turns:
        if turn.startswith("Person A:"):
            person_a_dialogue.append(turn[8:].strip())  # remove "Person A:" label
        elif turn.startswith("Person B:"):
            person_b_dialogue.append(turn[8:].strip())  # remove "Person B:" label

    # Perform sentiment analysis on the entire dialogue of Person A and Person B
    sentiment_a = get_sentiment(' '.join(person_a_dialogue))
    sentiment_b = get_sentiment(' '.join(person_b_dialogue))

    # Map sentiment to emoji
    sentiment_map = {
        'positive': '😊',
        'neutral': '😐',
        'negative': '😞'
    }

    # Display the results with emojis
    result_a.config(text=f"Person A's Sentiment: {sentiment_map[sentiment_a]}")
    result_b.config(text=f"Person B's Sentiment: {sentiment_map[sentiment_b]}")

    # Generate the summary of the sentiment analysis based on emotional flow
    summary_text = generate_summary(sentiment_a, sentiment_b, person_a_dialogue, person_b_dialogue)
    summary_label.config(state=tk.NORMAL)  # Allow editing
    summary_label.delete(1.0, tk.END)  # Clear any previous text
    summary_label.insert(tk.END, summary_text)  # Insert new text
    summary_label.config(state=tk.DISABLED)  # Disable editing

    # Evaluate the sentiment analysis
    evaluate_sentiment_analysis([conversation_text], [sentiment_a])  # Pass conversation text and predicted sentiment

# Function to split conversation into turns by speaker (Person A and Person B)
def split_conversation(conversation):
    # Normalize line breaks for consistency in input format
    conversation = re.sub(r'\n+', '\n', conversation.strip())  # Replace multiple newlines with single newline
    turns = re.split(r'(?=Person [A-B]:)', conversation)  # Split at "Person A:" or "Person B:" label
    return [turn.strip() for turn in turns if turn.strip()]  # Remove extra spaces and empty lines

# Function to generate the dynamic sentiment summary
def generate_summary(sentiment_a, sentiment_b, conversation_a, conversation_b):
    # Tracking emotional flow for Person A and Person B
    sentiment_a_flow = []
    sentiment_b_flow = []
    
    # Analyze sentence-by-sentence sentiment for Person A
    for line in conversation_a:
        sentiment_a_flow.append(get_sentiment(line))  # Track sentiment of each sentence
    
    # Analyze sentence-by-sentence sentiment for Person B
    for line in conversation_b:
        sentiment_b_flow.append(get_sentiment(line))  # Track sentiment of each sentence
    
    # Generating dynamic summaries based on flow
    # Summary for Person A
    sentiment_a_summary = []
    if 'positive' in sentiment_a_flow:
        sentiment_a_summary.append("Person A shows enthusiasm and support, encouraging Person B through most of the conversation.")
    if 'negative' in sentiment_a_flow:
        sentiment_a_summary.append("Person A also expresses concern at moments, trying to reassure Person B.")
    if 'neutral' in sentiment_a_flow:
        sentiment_a_summary.append("Person A remains neutral, helping to balance the conversation with calm responses.")
    
    sentiment_a_text = " ".join(sentiment_a_summary) or "Person A maintains a balanced tone throughout the conversation."
    
    # Summary for Person B
    sentiment_b_summary = []
    if 'positive' in sentiment_b_flow:
        sentiment_b_summary.append("Person B gradually warms up to the idea of the surprise, showing excitement as the conversation progresses.")
    if 'negative' in sentiment_b_flow:
        sentiment_b_summary.append("At the beginning, Person B expresses anxiety and reluctance about the surprise, but their mood improves.")
    if 'neutral' in sentiment_b_flow:
        sentiment_b_summary.append("Person B's emotions fluctuate, but they eventually begin to feel more relaxed and open to the idea.")
    
    sentiment_b_text = " ".join(sentiment_b_summary) or "Person B's feelings shift from hesitation to excitement."

    # Combining summaries for both
    return f"Person A: {sentiment_a_text}\n\nPerson B: {sentiment_b_text}"

# Function to evaluate sentiment analysis performance
def evaluate_sentiment_analysis(texts, ground_truth_labels):
    predicted_labels = []
    
    # Predict sentiment for each text using VADER
    for text in texts:
        sentiment = get_sentiment(text)  # Now we pass the text to get_sentiment
        predicted_labels.append(sentiment)
    
    # Print the predicted and actual labels
    print("Predicted Labels: ", predicted_labels)
    print("Ground Truth Labels: ", ground_truth_labels)

    # Calculate and print evaluation metrics
    accuracy = accuracy_score(ground_truth_labels, predicted_labels)
    precision, recall, f1, _ = precision_recall_fscore_support(ground_truth_labels, predicted_labels, average='weighted')
    
    print(f"\nAccuracy: {accuracy * 100:.2f}%")
    print(f"Precision: {precision:.2f}")
    print(f"Recall: {recall:.2f}")
    print(f"F1-Score: {f1:.2f}")

    # Confusion Matrix
    print("\nConfusion Matrix:")
    cm = confusion_matrix(ground_truth_labels, predicted_labels, labels=['positive', 'neutral', 'negative'])
    print(cm)

    # Classification report (includes precision, recall, f1-score per class)
    print("\nClassification Report:")
    print(classification_report(ground_truth_labels, predicted_labels))

# Create the main Tkinter window
root = tk.Tk()
root.title("Conversation Sentiment Analysis")

# Set the fixed window size
root.geometry("600x500")
root.resizable(False, False)  # Disable window resizing

# Create label and text box for entering the conversation
label_conversation = tk.Label(root, text="Enter the Conversation (with 'Person A:' and 'Person B:'):")
label_conversation.pack(pady=5)

conversation_entry = tk.Text(root, height=10, width=50)
conversation_entry.pack(pady=5)

# Create the Apply button to trigger sentiment analysis
apply_button = tk.Button(root, text="Apply", command=analyze_sentiment)
apply_button.pack(pady=10)

# Create labels to display the sentiment results with emojis
result_a = tk.Label(root, text="Person A's Sentiment: ", font=("Arial", 14))
result_a.pack(pady=5)

result_b = tk.Label(root, text="Person B's Sentiment: ", font=("Arial", 14))
result_b.pack(pady=5)

# Label to show the detailed sentiment summary
summary_label = tk.Text(root, height=8, width=60, wrap=tk.WORD, font=("Arial", 12))
summary_label.pack(pady=10)
summary_label.config(state=tk.DISABLED)  # Disable editing for the summary box

# Start the Tkinter event loop
root.mainloop()
