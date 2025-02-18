### ⭐Overview
This program automates the process of completing PocketPrep quizzes by using Selenium for browser interaction and a locally hosted Large Language Model (LLM) for selecting the correct answer. The primary goal of this project is to experiment with different language models on specialized, niche topics and to evaluate how prompt engineering can influence the accuracy of responses without changing the underlying model itself.

Through this process, the framework demonstrates how you can:
- Fine-tune prompts for increased accuracy.
- Learn from model mistakes by iterating on prompt structure.
- Gain a deeper understanding of how AI agents can be customized and improved for personal assistant applications.

### ⭐Features
- 📌 **Automated quiz navigation:** Logs in to PocketPrep, navigates to the “Build Your Own” quiz section, and sets up quiz parameters.
- 📌 **LLM-driven answer selection:** Uses the [Ollama LLM integration](https://github.com/jmorganca/ollama) to process the quiz question/answer pairs and automatically select an answer.
- 📌 **Human-like delay simulation:** Random sleep intervals mimic human behavior between questions.
- 📌 **Logging and debugging:** Logs essential steps and decisions for transparency.

### ⭐Setup

#### 📌 Requirements
1. **Python 3.8+** (Tested on newer versions).
2. **Google Chrome** (Latest version recommended).
3. **ChromeDriver** (Matching your Chrome version).
4. **Environment file (.env)** with the following variables:
   - `LOGIN_URL`: PocketPrep login page URL.
   - `START_URL`: The main study page or "Build Your Own" start page.
   - `EMAIL`: Your PocketPrep account email.
   - `PASSWORD`: Your PocketPrep account password.
   - `CHROMEDRIVER_PATH`: Absolute path to your ChromeDriver.

#### 📌 Installation
1. **Clone this repository** or download the code files.
2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Linux/Mac
   venv\Scripts\activate      # On Windows
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   Make sure your `requirements.txt` includes libraries like:
   - `selenium`
   - `python-dotenv`
   - `langchain_ollama` (or any custom integration for Ollama)
   - `logging` (commonly part of the standard library, but ensure no separate dependencies are needed)

4. **Set up ChromeDriver**:
   - Download [ChromeDriver](https://chromedriver.chromium.org/downloads) that matches your Google Chrome version.
   - Place it somewhere on your system.
   - Update the path in your `.env` file to point to where ChromeDriver is located.

5. **Create your `.env` file**:
   ```
   LOGIN_URL="https://pocketprep.com/login"
   START_URL="https://pocketprep.com/study"
   EMAIL="your_email@example.com"
   PASSWORD="YourSecurePassword"
   CHROMEDRIVER_PATH="/absolute/path/to/chromedriver"
   ```

### ⭐Usage

#### 📌 Running the Program
Run the script directly from your command line:
```bash
python your_script_name.py
```
The bot will:
1. Launch Google Chrome in incognito mode.
2. Navigate to the `LOGIN_URL` and log in with your `EMAIL` and `PASSWORD`.
3. Navigate to the `START_URL` and configure quiz settings:
   - Sets the quiz to only new questions.
   - Unchecks answered/flagged/incorrect questions.
   - Adjusts the question slider (default is `test_questions = 100`).
4. Starts the quiz and uses your specified LLM model (`AI_model = 'mistral'` by default) to answer each question.

#### 📌 Customizing
- **`AI_model`**: Change the model name to match any model you have installed with Ollama (e.g., `'llama2'`, `'mistral'`, etc.).
- **`test_questions`**: Adjust the number of questions you want the bot to attempt in a single quiz session.
- **`questiondelay_lower` and `questiondelay_upper`**: Control the range for the random sleep interval between questions.
- **Prompt template**: Modify the instructions for the LLM under the `template = """ ... """` variable if you want different answer formats or additional logic.

#### 📌 Logging
All key events (login, question navigation, answer prediction, etc.) are logged to the console with varying detail. You can modify the logging level by updating:
```python
logging.basicConfig(level=logging.INFO, format='%(message)s')
```
Possible levels are `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.

### ⭐Future Enhancements
- 📌 **Adaptive Prompt Engineering**: Dynamically adjust prompts based on the model’s confidence or previous mistakes.
- 📌 **Error Handling & Retries**: More robust handling when the site changes layout or if the LLM returns unexpected answers.
- 📌 **Analytics & Reporting**: Track correct/incorrect answers, identify patterns, and provide feedback on question categories for better studying.
- 📌 **Personal Assistant Framework**: Evolve this into a broader personal assistant to handle other tasks and queries using similar or advanced LLM architectures.

---
