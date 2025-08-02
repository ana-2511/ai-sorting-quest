import streamlit as st
import os
import numpy as np
import random
from keras.layers import TFSMLayer
import streamlit.components.v1 as components
import shutil
import base64
import pandas as pd
from PIL import Image
from datetime import datetime


# Initialize session state
if 'mode_selected' not in st.session_state:
    st.session_state.mode_selected = False
if 'supervised_stage' not in st.session_state:
    st.session_state.supervised_stage = 0
if 'test_image' not in st.session_state:
    st.session_state.test_image = None
if 'correct_class' not in st.session_state:
    st.session_state.correct_class = None
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0
if 'score_saved' not in st.session_state:
    st.session_state.score_saved = False


# Title
st.set_page_config(page_title="AI Sorting Quest", layout="wide")
st.markdown("<h1 style='text-align:center;'>🎮 AI Sorting Quest</h1>", unsafe_allow_html=True)

# Session state
for key in ['mode_selected', 'supervised_stage', 'test_image', 'correct_class',
            'attempts', 'score_saved', 'name']:
    if key not in st.session_state:
        st.session_state[key] = 0 if key == 'attempts' else None if key == 'test_image' else False if key == 'score_saved' else ""


# Store name in session
if "name" not in st.session_state:
    st.session_state.name = ""

if not st.session_state.name:
    name_input = st.text_input("Enter your name to start the game:")
    if name_input.strip():
        st.session_state.name = name_input.strip()
        st.rerun()
    st.stop()  # Prevent rest of the app (like buttons, game) from showing
else:
    st.success(f"👋 Welcome, {st.session_state.name}!")
    st.button("⬅️ Back to Home", on_click=lambda: st.session_state.clear())
# Load model (Keras 3 compatible)
model = TFSMLayer("converted_savedmodel/model.savedmodel", call_endpoint="serving_default")

# Class names must match your model's order
class_names = ["Apple", "Banana", "Carrot", "Potato", "Cucumber", "Red Cabbage", "Pear", "Orange", "Ginger", "Blackberry"]
IMAGE_DIR = "images"
GUIDE_DIR = "guides"
LEADERBOARD_FILE = "scores.csv"

# Create leaderboard if it doesn't exist
#if not os.path.exists(LEADERBOARD_FILE):
    #pd.DataFrame(columns=["Name", "Game", "Score", "Attempts", "Date"]).to_csv(LEADERBOARD_FILE, index=False)






# Step 1: Choose mode
if not st.session_state.mode_selected:
    mode = st.radio("Choose your learning mode:", ["Supervised Learning", "Unsupervised Learning"])
    if st.button("Start Learning"):
        st.session_state.mode = mode
        st.session_state.mode_selected = True
        st.rerun()
else:
    mode = st.session_state.mode
    st.markdown(f"### Mode: {mode}")

    # --- SUPERVISED MODE ---
    if mode == "Supervised Learning":

        # Stage 0: Show 1 sample image from each class
        if st.session_state.supervised_stage == 0:
            st.subheader("👀 Step 1: Learn the Classes")
            cols = st.columns(5)
            for idx, cls in enumerate(class_names):
                sample_img = random.choice(os.listdir(os.path.join(IMAGE_DIR, cls)))
                #img_path = os.path.join(IMAGE_DIR, cls, random.choice(os.listdir(os.path.join(IMAGE_DIR, cls))))
                with cols[idx % 5]:
                    st.image(os.path.join(IMAGE_DIR, cls, sample_img), caption=cls, use_column_width=True)

            if st.button("Next → Let's Test AI!"):
                st.session_state.supervised_stage = 1
                st.session_state.test_image = None  # Reset test image
                st.session_state.attempts = 0
                st.session_state.score_saved = False
                st.rerun()

        # Stage 1: Random test image shown
        elif st.session_state.supervised_stage == 1:
            st.subheader("🤔 Step 2: Guess the Fruit!")

            if st.session_state.test_image is None:
               chosen_class = random.choice(class_names)
               image_file = random.choice(os.listdir(os.path.join(IMAGE_DIR, chosen_class)))
               st.session_state.test_image = os.path.join(IMAGE_DIR, chosen_class, image_file)
               st.session_state.correct_class = chosen_class
               st.session_state.attempts = 0  # reset attempts for new round
               st.session_state.score_saved = False
               st.rerun()


            img = Image.open(st.session_state.test_image).resize((224, 224))
            st.image(img, caption="What do you think this is?", width=300)

            guess = st.radio("Choose the correct class:", class_names)
            if st.button("Submit Answer"):
                  st.session_state.attempts += 1

                  if guess == st.session_state.correct_class:
                    st.success("🎉 Wohoo Correct! That's how supervised learning works!")

                    st.session_state.correct_guess = True
                    st.session_state.score = max(30 - 5 * (st.session_state.attempts - 1), 5)
                  else:
                    st.error(f"❌ Oops! That’s incorrect. It was: {st.session_state.correct_class}")
                    st.session_state.correct_guess = False
            
                    if st.button("🔁 Try Again"):
                        st.session_state.test_image = None
                        st.session_state.attempts = 0
                        st.session_state.correct_guess = None
                        st.rerun()

            # After answer is submitted and correct
            if st.session_state.get("correct_guess", False):
                score = st.session_state.score
                st.markdown(f"### 🎯 Your Score: {score} / 30")
                
                columns = ["Name", "Game", "Score", "Attempts" ,"Date"]

                    # Add 'Save Score' button
                if not st.session_state.score_saved:
                    if st.button("💾 Save My Score to Leaderboard"):
                        new_entry = pd.DataFrame([{
                            "Name": st.session_state.name,
                            "Game": "Supervised",
                            "Score": score,
                            "Attempts": st.session_state.attempts,
                            "Date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
                        }], columns=columns)
                        if os.path.exists("scores.csv"):
                            new_entry.to_csv("scores.csv", mode="a", header=False, index=False)
                        else:
                            new_entry.to_csv("scores.csv", index=False)
                        st.session_state.score_saved = True
                        st.success("✅ Your score was saved to the leaderboard!")


                    
                # Explanation
                st.markdown("""
                ### 🧠 What is Supervised Learning?
                - AI is trained with labeled data (e.g. "This is a Banana")
                - It learns patterns and relationships (color, shape, size).
                - Later, it predicts labels for new data
                - That's exactly what you did, you just acted like an AI classifier
                ### 🤖 What about Reinforcement Learning?
                Just like you tried different guesses and got a reward (score),
                AI agents in reinforcement learning explore actions and learn which give the best rewards over time!
                """)
                with open("guides/supervised_learning.docx", "rb") as doc_file:
                    st.download_button(
                        label="📘 Download Supervised Learning Guide",
                        data=doc_file,
                        file_name="supervised_learning.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )

                  #else:
                      #st.error(f"❌ Oops! That's incorrect. It was: {st.session_state.correct_class}")
                      #if st.button("🔁 Try Again"):
                          #st.session_state.test_image = None
                          #st.rerun()



    # --- UNSUPERVISED MODE --- (placeholder)
    else:
        st.subheader("🧠 Unsupervised Learning")
        st.info("In unsupervised learning, the AI doesn’t know labels but tries to group similar items together!")


        # when score received
        #st.session_state.unsupervised_attempts += 1

    
        st.markdown("""
        In this game, **you** will act like the AI!
    
        - You will see **random fruits** without names
        - Drag and drop them into **3 groups** based on how similar they look
        - After placing all items, you’ll see if your grouping is correct
    
        💡 Hint: Try grouping by **color**, **shape**, or **texture**
        """)

        
        # Define image source directory (3 folders with fruits)
        IMAGE_SOURCE = "images"  # <-- Folder must contain subfolders like Apple, Banana, Cucumber etc.
        
        # Randomly select 3 class folders
        selected_classes = random.sample(os.listdir(IMAGE_SOURCE), 3)
        #sample_paths = []           # [(img_id, base64_string)]
        bin_assignments = [[], [], []]  # bin1 → [f1, f4], bin2 → [f2, f5], bin3 → [f3, f6]
        html_blocks = []
        
        img_counter = 1
        def img_to_base64(path):
            with open(path, "rb") as f:
                return base64.b64encode(f.read()).decode()
            

        for bin_index, cls in enumerate(selected_classes):
            cls_path = os.path.join(IMAGE_SOURCE, cls)
            img_files = random.sample(os.listdir(cls_path), 2)  # 2 images per class
            for img_file in img_files:
                img_id = f"f{img_counter}"
                img_path = os.path.join(cls_path, img_file)
                base64_str = img_to_base64(img_path)
        
                # Generate HTML for draggable image
                html_blocks.append(
                    f'<img src="data:image/jpeg;base64,{base64_str}" class="fruit" id="{img_id}" draggable="true" ondragstart="drag(event)">'
                )
                bin_assignments[bin_index].append(img_id)
                img_counter += 1
        
        # Generate JS-correct answer map
        js_correct = '{' + ',\n'.join([f'"bin{i+1}": {bin_assignments[i]}' for i in range(3)]) + '}'
        
        html_game = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <title>Unsupervised Learning Game</title>
          <style>
            .fruit {{
              width: 100px;
              height: 100px;
              margin: 10px;
              cursor: move;
              border-radius: 12px;
              box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
            }}
            .bin {{
              width: 180px;
              height: 220px;
              border: 3px dashed #888;
              display: inline-block;
              margin: 20px;
              padding: 10px;
              border-radius: 10px;
              background: #f2f2f2;
              vertical-align: top;
            }}
            h2, h3 {{
              font-family: sans-serif;
            }}
            button {{
              margin-top: 20px;
              padding: 10px 20px;
              font-size: 16px;
              border-radius: 8px;
              background-color: #4CAF50;
              color: white;
              border: none;
              cursor: pointer;
            }}
            button:hover {{
              background-color: #45a049;
            }}
            #resultBox {{
              margin-top: 30px;
              padding: 15px;
              background-color: #fff8dc;
              border: 2px solid #ffcc00;
              border-radius: 8px;
              font-family: sans-serif;
              display: none;
            }}
          </style>
        </head>
        <body>
          <h2>🍍 Drag each fruit into one of 3 groups</h2>
          <div>{''.join(html_blocks)}</div>
        
          <h3>📁 Drop fruits here:</h3>
          <div style="display: flex; justify-content: center; gap: 30px;">
            <div id="bin1" class="bin" ondrop="drop(event)" ondragover="allowDrop(event)"></div>
            <div id="bin2" class="bin" ondrop="drop(event)" ondragover="allowDrop(event)"></div>
            <div id="bin3" class="bin" ondrop="drop(event)" ondragover="allowDrop(event)"></div>
          </div>

        
          <br><button onclick="checkResult()">✅ Submit</button>
          <div id="resultBox"></div>
        
          <script>
            function allowDrop(event) {{
              event.preventDefault();
            }}
            function drag(event) {{
              event.dataTransfer.setData("text", event.target.id);
            }}
            function drop(event) {{
              event.preventDefault();
              const data = event.dataTransfer.getData("text");
              event.target.appendChild(document.getElementById(data));
            }}
        
            function sameSet(a, b) {{
              return a.length === b.length && a.every(item => b.includes(item));
            }}
        
            function checkResult() {{
              const correct = Object.values({js_correct});
              const used = [false, false, false];
              const bins = ["bin1", "bin2", "bin3"];
              let matched = 0;
        
              const actualGroups = bins.map(bin =>
                Array.from(document.getElementById(bin).children).map(el => el.id)
              );
        
              for (let actual of actualGroups) {{
                for (let i = 0; i < correct.length; i++) {{
                  if (!used[i] && sameSet(actual, correct[i])) {{
                    used[i] = true;
                    matched++;
                    break;
                  }}
                }}
              }}
              
              let score = matched * 10;
              let resultBox = document.getElementById("resultBox");
              resultBox.style.display = "block";
              resultBox.innerHTML = `<input type="hidden" id="scoreInput" value="${{score}}">`;
              resultBox.innerHTML += `🎯 Your Score: ${{score}} / 30`;

                     
              if (matched === 3) {{
                resultBox.innerHTML += `<br><br>🎉 Excellent! You grouped everything perfectly, just like in Unsupervised Learning.<br><br>
                <b>🧠 What is Unsupervised Learning?</b><br>
                In unsupervised learning, AI models don’t get any labels or answers in advance. Instead, they learn to find patterns and group similar things together — just like you did by noticing colors, shapes, or textures. Great job acting like an AI!`;

              }} else {{
                resultBox.innerHTML += `<br><br><button onclick='location.reload()'>🔁 Try Again</button>`;
              }}
            }}
          </script>
        </body>
        </html>
        """
        # Display in Streamlit
        components.html(html_game, height=750)


        #score_str = st.text_input("", key="unsupervised_score", label_visibility="collapsed")
        #attempt_str = st.text_input("", key="unsupervised_attempts", label_visibility="collapsed")
        #
        ## Properly cast to integers with fallback
        #try:
        #    st.session_state.unsupervised_score = int(score_str) if score_str else 0
        #except ValueError:
        #    st.session_state.unsupervised_score = 0
        #
        #try:
        #    st.session_state.unsupervised_attempts = int(attempt_str) if attempt_str else 0
        #except ValueError:
        #    st.session_state.unsupervised_attempts = 0


        #score_placeholder = st.empty()

        # JavaScript → Streamlit communication via iframe messaging
        components.html("""
        <script>
          window.addEventListener("message", (event) => {
            if (event.data.score !== undefined) {
              const score = event.data.score;
              const attemptValue = event.data.attempt || 1;
              window.parent.postMessage({ type: "streamlit:setComponentValue", value: score }, "*");
              document.querySelector("input[name='unsupervised_score']").value = score;
              document.querySelector("input[name='unsupervised_attempts']").value = attemptValue;
              document.querySelector("form").dispatchEvent(new Event("submit", { bubbles: true }));
            }
          });
        </script>
        """, height=0)

        # Initialize once
        if "unsupervised_score" not in st.session_state:
            st.session_state.unsupervised_score = 0
        if "unsupervised_attempts" not in st.session_state:
            st.session_state.unsupervised_attempts = 0
        # Read score and attempts from hidden input using Streamlit-JS bridge
        score = st.query_params.get("score", [None])[0]
        attempt = st.query_params.get("attempt", [None])[0]
        
        # Store in session_state only if received
        if score is not None:
            st.session_state.unsupervised_score = int(score)
        if attempt is not None:
            st.session_state.unsupervised_attempts = int(attempt)

        submitted = st.button("💾 Save My Score to Leaderboard")

        if submitted:
            name = st.session_state.get("name", "Unknown")
            score = st.session_state.get("unsupervised_score", 0)
            st.session_state.unsupervised_attempts += 1
            attempts = st.session_state.unsupervised_attempts
            
        
            columns = ["Name", "Game", "Score", "Attempts", "Date"]
            leaderboard_path = "scores.csv"
        
            # Load existing leaderboard
            if os.path.exists(leaderboard_path):
                leaderboard_df = pd.read_csv(leaderboard_path)
            else:
                leaderboard_df = pd.DataFrame(columns=columns)
        
            existing_entry = leaderboard_df[
                (leaderboard_df["Name"] == st.session_state.name) &
                (leaderboard_df["Game"] == "Unsupervised")
            ]
        
            # Only update if score is higher
            if not existing_entry.empty:
                prev_score = existing_entry["Score"].values[0]
                if score > prev_score:
                    leaderboard_df.loc[existing_entry.index, "Score"] = score
                leaderboard_df.loc[existing_entry.index, "Attempts"] += 1
                leaderboard_df.loc[existing_entry.index, "Date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
            else:
                new_row = pd.DataFrame([{
                    "Name": st.session_state.name,
                    "Game": "Unsupervised",
                    "Score": score,
                    "Attempts": attempts,
                    "Date": datetime.now().strftime("%Y-%m-%d %H:%M")
                }])
                leaderboard_df = pd.concat([leaderboard_df, new_row], ignore_index=True)
        
            leaderboard_df.to_csv(leaderboard_path, index=False)
            st.success("✅ Your score has been saved to the leaderboard!")
                    
        
        # Add download link
        with open("guides/unsupervised_learning.docx", "rb") as doc_file:
            st.download_button(
                label="📘 Learn More: Download Unsupervised Learning Guide",
                data=doc_file,
                file_name="unsupervised_learning.docx",
                mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

# -------------------- LEADERBOARD --------------------
st.markdown("## 📊 Leaderboard Dashboard")

df_leader = pd.read_csv(LEADERBOARD_FILE)

# Filter tabs
tab1, tab2 = st.tabs(["🏷️ Supervised", "🧩 Unsupervised"])

with tab1:
    st.subheader("🏷️ Supervised Game Leaderboard")
    st.dataframe(df_leader[df_leader["Game"] == "Supervised"].sort_values(by="Score", ascending=False).reset_index(drop=True))

with tab2:
    st.subheader("🧩 Unsupervised Game Leaderboard")
    st.dataframe(df_leader[df_leader["Game"] == "Unsupervised"].sort_values(by="Score", ascending=False).reset_index(drop=True))

# Download Option
st.download_button(
    label="📥 Download Full Leaderboard",
    data=df_leader.to_csv(index=False).encode('utf-8'),
    file_name="AI_Game_Leaderboard.csv",
    mime="text/csv"
)
