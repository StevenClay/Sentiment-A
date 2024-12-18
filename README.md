# Conversation Sentiment Analysis App

This application performs sentiment analysis on a conversation between two people (Person A and Person B). It uses **VADER (Valence Aware Dictionary and sEntiment Reasoner)** from the **NLTK** library to analyze the emotional tone of the text. The sentiment of each speaker is displayed using emojis (😊, 😐, 😞), and a detailed summary of the conversation's emotional flow is generated.

## Features

- **Sentiment Analysis**: Analyzes the sentiment of the entire conversation for both speakers (Person A and Person B).
- **Emoji-based Sentiment Display**: Shows the sentiment of each person with corresponding emojis (😊 for positive, 😐 for neutral, 😞 for negative).
- **Dynamic Summary**: Generates a dynamic summary that describes the emotional flow of both speakers in the conversation.
- **GUI-based Interface**: Built with **Tkinter** for easy user interaction.

## Requirements

To run this project, you'll need the following dependencies:

- Python 3.x
- **NLTK** library (for sentiment analysis)
- **Tkinter** (for the GUI interface)

### Installation Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/conversation-sentiment-analysis.git
   cd conversation-sentiment-analysis
