import tkinter as tk
from tkinter import messagebox
from nltk.sentiment import SentimentIntensityAnalyzer
import re
import nltk
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

# Function to analyze the overall sentiment for Person A and Person B
def analyze_sentiment():
    # Get input from the text box
    conversation_text = conversation_entry.get("1.0", "end-1c")
    
    # Check if the conversation is empty
    if not conversation_text.strip():
        messagebox.showerror("Input Error", "Please enter the conversation text.")
        return

    # Split the conversation into turns based on speaker labels
    turns = split_conversation(conversation_text)

    # Initialize sentiment trackers for each person
    person_a_dialogue = ""
    person_b_dialogue = ""

    # Separate the dialogue for Person A and Person B
    for turn in turns:
        if turn.startswith("Person A:"):
            person_a_dialogue += " " + turn[8:].strip()  # remove "Person A:" label
        elif turn.startswith("Person B:"):
            person_b_dialogue += " " + turn[8:].strip()  # remove "Person B:" label

    # Perform sentiment analysis on the entire dialogue of Person A and Person B
    sentiment_a = get_sentiment(person_a_dialogue)
    sentiment_b = get_sentiment(person_b_dialogue)

    # Map sentiment to emoji
    sentiment_map = {
        'positive': '😊',
        'neutral': '😐',
        'negative': '😞'
    }

    # Display the results with emojis
    result_a.config(text=f"Person A's Sentiment: {sentiment_map[sentiment_a]}")
    result_b.config(text=f"Person B's Sentiment: {sentiment_map[sentiment_b]}")

# Function to split conversation into turns by speaker (Person A and Person B)
def split_conversation(conversation):
    # Split conversation by new lines and remove extra spaces
    turns = [turn.strip() for turn in conversation.splitlines() if turn.strip()]
    return turns

# Create the main Tkinter window
root = tk.Tk()
root.title("Conversation Sentiment Analysis")

# Create label and text box for entering the conversation
label_conversation = tk.Label(root, text="Enter the Conversation (with 'Person A:' and 'Person B:'):")
label_conversation.pack(pady=5)

conversation_entry = tk.Text(root, height=15, width=50)
conversation_entry.pack(pady=5)

# Create the Apply button to trigger sentiment analysis
apply_button = tk.Button(root, text="Apply", command=analyze_sentiment)
apply_button.pack(pady=10)

# Create labels to display the sentiment results with emojis
result_a = tk.Label(root, text="Person A's Sentiment: ", font=("Arial", 14))
result_a.pack(pady=5)

result_b = tk.Label(root, text="Person B's Sentiment: ", font=("Arial", 14))
result_b.pack(pady=5)

# Start the Tkinter event loop
root.mainloop()
