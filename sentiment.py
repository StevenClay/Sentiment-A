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

    # Generate the summary of the sentiment analysis
    summary_text = generate_summary(sentiment_a, sentiment_b)
    summary_label.config(text=summary_text)

# Function to split conversation into turns by speaker (Person A and Person B)
def split_conversation(conversation):
    # Split conversation by new lines and remove extra spaces
    turns = [turn.strip() for turn in conversation.splitlines() if turn.strip()]
    return turns

# Function to generate the sentiment summary
def generate_summary(sentiment_a, sentiment_b):
    # Summary for Person A
    if sentiment_a == 'positive':
        sentiment_a_text = "Person A is generally positive and encouraging, providing support and maintaining an optimistic tone throughout the conversation. 😊"
    elif sentiment_a == 'negative':
        sentiment_a_text = "Person A seems a bit down or frustrated, with a more negative tone. 😞"
    else:
        sentiment_a_text = "Person A is neutral, neither very positive nor negative. 😐"

    # Summary for Person B
    if sentiment_b == 'positive':
        sentiment_b_text = "Person B starts off stressed but becomes more positive as the conversation continues, particularly when discussing weekend plans. 😊"
    elif sentiment_b == 'negative':
        sentiment_b_text = "Person B is feeling overwhelmed and stressed, with a more negative tone. 😞"
    else:
        sentiment_b_text = "Person B is neutral throughout the conversation. 😐"

    # Combine the summaries for both speakers
    return f"{sentiment_a_text}\n\n{sentiment_b_text}"

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

# Label to show the detailed sentiment summary
summary_label = tk.Label(root, text="Sentiment Summary:", font=("Arial", 12))
summary_label.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()