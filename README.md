### ⭐PocketPrep Quiz Bot – LLM + Selenium Agent

### 📌Overview  
This project is a personal exploration into **how large language models (LLMs) can be fine-tuned for accuracy** and integrated with **automation tools like Selenium** to create intelligent, agentic systems.

The script automates the process of completing PocketPrep quizzes by combining:
- **Selenium** for browser-based interaction  
- A **locally hosted LLM** (via [Ollama](https://github.com/jmorganca/ollama)) for question analysis and answer selection  

The primary goal is to experiment with LLM-driven decision-making in specialized domains, evaluate prompt engineering strategies, and observe how AI agents can be adapted for real-world tasks.

### 📌What This Project Demonstrates  
- How prompt engineering affects LLM accuracy on niche question sets  
- How to combine LLMs with UI automation tools for agent-like behavior  
- How iterative refinement can reduce errors and improve task performance

### 📌Key Features  
- Automated login and quiz setup on PocketPrep  
- Dynamic quiz configuration (filters, question sliders, etc.)  
- LLM-generated answer selection using local models (e.g., Mistral, LLaMA)  
- Human-like delays and detailed logging for transparency and debugging  

### 📌Setup Instructions

#### Requirements  
- Python 3.8+  
- Google Chrome (latest version)  
- ChromeDriver (matching your browser version)  
- A `.env` file with:
  ```
  LOGIN_URL="https://pocketprep.com/login"
  START_URL="https://pocketprep.com/study"
  EMAIL="your_email@example.com"
  PASSWORD="YourSecurePassword"
  CHROMEDRIVER_PATH="/absolute/path/to/chromedriver"
  ```

#### Installation  
1. Clone this repository  
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Download the correct [ChromeDriver](https://chromedriver.chromium.org/downloads) and update the path in your `.env` file

### 📌Running the Bot  
Run the script directly:
```bash
python PocketPrepQuizBot.py
```
It will:
- Launch Chrome in incognito mode  
- Log in and configure a custom quiz  
- Use your specified LLM to select answers  
- Simulate human interaction via randomized delays

### 📌Customization  
- `AI_model`: Use any locally hosted model (e.g., `mistral`, `llama2`)  
- `test_questions`: Number of quiz questions per session  
- Prompt template: Modify the system prompt inside the script to experiment with answer format, reasoning depth, etc.  
- Delay settings: Customize `questiondelay_lower` and `questiondelay_upper` to control pacing  

### 📌Logging  
Logs all key actions for debugging and transparency:
```python
logging.basicConfig(level=logging.INFO, format='%(message)s')
```
Adjust log levels (`DEBUG`, `INFO`, etc.) as needed.

### 📌Future Directions  
- Adaptive prompt tuning based on model performance  
- Confidence-based retries or self-reflection  
- Study analytics: capture right/wrong answers and categorize feedback  
- Expansion into broader personal assistant functionality

---
