🧠 AI Sorting Quest – Learn AI Through Games! 🎮
AI Sorting Quest is an educational game app built using Streamlit that introduces kids and beginners to Artificial Intelligence through fun, interactive modules like sorting, training bots, image classification, and chatbot creation.

🌐 Live Demo (Streamlit Cloud)
https://ai-sorting-quest-jayadhi.streamlit.app/

📌 Features

Drag-and-drop games, quizzes, puzzles

Live image classification with an AI model 🧠

Leaderboards with score tracking

Downloadable learning guides (PDF/DOCX)

Deployed via Streamlit Cloud 🔥

🧭 How to Navigate the App
👋 Enter Your Name

On the home page, you're prompted to type your name.

This will start your session and record your scores.

🎮 Choose a Game Mode

Select either:

Supervised Learning

Unsupervised Learning

📘 Supervised Learning Mode

Step 1: Learn by viewing labeled fruit images.

Step 2: Guess the fruit shown by AI – acts like image classification.

Score is based on correct guesses and number of attempts.

Save your score to the leaderboard with a click.

🧠 Unsupervised Learning Mode

Drag-and-drop fruit images into 3 groups based on shape/color.

The AI checks your grouping.

You get a score out of 30, based on grouping accuracy.

Save score after each game; leaderboard only updates if new score is better.

📊 Leaderboard Dashboard

Shows top scores for both Supervised and Unsupervised games.

Includes attempts, timestamps, and downloadable CSVs.

📥 Download Learning Guides

Each module has a downloadable DOCX explaining key concepts like:

Supervised vs Unsupervised Learning

ChatGPT said:
Here’s a detailed and polished README.md file for your AI Sorting Quest app. This includes instructions on how to navigate the app, an overview of how each module works, and information for users and developers.

🧠 AI Sorting Quest – Learn AI Through Games! 🎮
AI Sorting Quest is an educational game app built using Streamlit that introduces kids and beginners to Artificial Intelligence through fun, interactive modules like sorting, training bots, image classification, and chatbot creation.

🌐 Live Demo (Streamlit Cloud)
(replace with your actual deployed link)

📌 Features
9 AI learning modules 🎓

Drag-and-drop games, quizzes, puzzles

Live image classification with an AI model 🧠

Leaderboards with score tracking

Downloadable learning guides (PDF/DOCX)

Deployed via Streamlit Cloud 🔥

🧭 How to Navigate the App
👋 Enter Your Name

On the home page, you're prompted to type your name.

This will start your session and record your scores.

🎮 Choose a Game Mode

Select either:

Supervised Learning

Unsupervised Learning

📘 Supervised Learning Mode

Step 1: Learn by viewing labeled fruit images.

Step 2: Guess the fruit shown by AI – acts like image classification.

Score is based on correct guesses and number of attempts.

Save your score to the leaderboard with a click.

🧠 Unsupervised Learning Mode

Drag-and-drop fruit images into 3 groups based on shape/color.

The AI checks your grouping.

You get a score out of 30, based on grouping accuracy.

Save score after each game; leaderboard only updates if new score is better.

📊 Leaderboard Dashboard

Shows top scores for both Supervised and Unsupervised games.

Includes attempts, timestamps, and downloadable CSVs.

📥 Download Learning Guides

Each module has a downloadable DOCX explaining key concepts like:

Supervised vs Unsupervised Learning

Reinforcement Learning

Neural Networks and more

🧩 Modules Overview
No.	Module Name	Description
1	What is AI?	Basic quizzes and games to introduce AI history and usage.
2	Machine Learning 101	Fruit sorting by visual features (color/shape).
3	Data Detective	Label, clean, and fix datasets to solve mysteries.
4	Train Your Bot	Drag-and-drop interface to train an AI bot.
5	Neural Network Maze	Learn neural layers by navigating a fun maze.
6	Image Recognition	Upload images and test AI’s ability to classify them.
7	Chatbot Creator	Build your own chatbot using predefined logic.
8	AI in Nature	See how AI helps in wildlife, agriculture, weather.
9	AI Ethics Adventure	Solve ethical dilemmas in AI through choices.

🛠 Developer Setup
🔧 Requirements
bash
Copy code
pip install -r requirements.txt
📁 Folder Structure
Copy code
.
├── app.py
├── images/
│   ├── Apple/
│   ├── Banana/
│   └── ...
├── guides/
│   ├── supervised_learning.docx
│   └── unsupervised_learning.docx
├── scores.csv
├── requirements.txt                                             


🚀 Deployment (Render / Streamlit Cloud)
This app is already configured for deployment:

requirements.txt handles Python dependencies

Procfile (for Render) or just streamlit run app.py (for Streamlit Cloud)

Leaderboard CSV saved locally or to persistent storage if using a database

