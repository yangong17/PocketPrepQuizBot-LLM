import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Load environment variables from .env file
load_dotenv()

# Get environment variables
login_url = os.getenv("LOGIN_URL")
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")
driver_path = os.getenv("CHROMEDRIVER_PATH")
start_url = os.getenv("START_URL")  # Load START_URL from .env file, the "Build Your Own" page

# Debug prints to verify environment variables
logging.info(f"Login URL: {login_url}")
logging.info(f"Driver Path: {driver_path}")

# Selenium setup
def setup_driver(driver_path):
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    return driver

# Function to log into PocketPrep
def login(driver, login_url, email, password):
    logging.info("Logging in...")
    driver.get(login_url)
    time.sleep(5)
    
    # Enter login credentials
    driver.find_element(By.XPATH, '//*[@id="input-email"]').send_keys(email)
    driver.find_element(By.XPATH, '//*[@id="study"]/div/div[2]/div[2]/div/div[3]/div/input').send_keys(password)
    driver.find_element(By.XPATH, '//*[@id="study"]/div/div[2]/div[2]/div/div[4]/button').click()
    time.sleep(4)  # Wait for login to complete

# Function to go to the "Build Your Own" page
def navigate_to_quiz_builder(driver, start_url):
    logging.info("Navigating to quiz builder...")
    driver.get(start_url)  # Use the start_url loaded from .env (Main study page)
    time.sleep(3)  # Ensure the page is fully loaded

    # Click on "Build Your Own"
    driver.find_element(By.XPATH, '//*[@id="study__container"]/div[2]/div[2]/div[2]/div[7]').click() # (Build your own page)
    time.sleep(2)


def configure_quiz_settings(driver, slider_value=50): #IMPORTANT! Slider value determines # of questions to run in quiz. (E.g: "slider_value=10" = 10 questions)
    # Ensure "New Questions" remains checked
    new_questions_checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@aria-labelledby="byoq__include-item-new" and contains(@class, "uikit-checkbox")]'))
    )
    if new_questions_checkbox.get_attribute("aria-checked") == "false": #Basically sets it to the opposite of whatever is listed here. 
        new_questions_checkbox.click()

    # Uncheck the "Answered Questions" checkbox
    answered_questions_checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@aria-labelledby="byoq__include-item-answered" and contains(@class, "uikit-checkbox")]'))
    )
    if answered_questions_checkbox.get_attribute("aria-checked") == "true":
        answered_questions_checkbox.click()

    # Uncheck the "Flagged Questions" checkbox
    flagged_questions_checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@aria-labelledby="byoq__include-item-flagged" and contains(@class, "uikit-checkbox")]'))
    )
    if flagged_questions_checkbox.get_attribute("aria-checked") == "true":
        flagged_questions_checkbox.click()

    # Uncheck the "Incorrect Questions" checkbox
    incorrect_questions_checkbox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//div[@aria-labelledby="byoq__include-item-incorrect" and contains(@class, "uikit-checkbox")]'))
    )
    if incorrect_questions_checkbox.get_attribute("aria-checked") == "true":
        incorrect_questions_checkbox.click()

    # Set the Question Number Slider to the desired value (Modify it above)
    try:
        slider = WebDriverWait(driver, 10).until( 
            EC.presence_of_element_located((By.XPATH, '//*[@id="questions-slider"]'))
        )
        if slider_value is None:
            slider_value = slider.get_attribute("max")  # Set to max if no value is provided

        driver.execute_script("arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('input'));", slider, slider_value)
        logging.info(f"Slider set to value: {slider_value}")
    except TimeoutException:
        logging.error("Slider element not found or took too long to load.")


def start_quiz(driver):
    logging.info("Starting quiz setup...")

    # Determine the number of remaining questions
    remaining_questions = int(driver.find_element(By.XPATH, '//*[@id="study"]/div/div/div/div[1]/div/div[5]/div[2]/div/div[1]').text)
    logging.info(f"Detected {remaining_questions} remaining questions.")
    loops_needed = (remaining_questions + 249) // 250  # Ceiling division

    # If no questions remaining, exit
    if loops_needed == 0:
        logging.info("No remaining questions. Exiting.")
        return False

    logging.info("Continuing with quiz processing...")

    time.sleep(2) # Buffer for user to confirm settings are correct

    # Press the button to start the quiz
    confirm_button_xpath = '//*[@id="study"]/div/div/div/div[2]/button[2]'
    confirm_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, confirm_button_xpath))
    )
    confirm_button.click()
    time.sleep(2)  # Wait to ensure the action is completed before proceeding

    return loops_needed


# Function to log the question and answers, and wait for user confirmation
def log_question_and_answers(driver, question_number):
    current_question_xpath = '//*[@id="study"]/div/div[2]/div/div/div[2]/div/div/div[2]/div[2]'
    answer_options_xpath_template = '//*[@id="study"]/div/div[2]/div/div/div[2]/div/div/div[2]/div[3]/div[{}]/div/div[2]'

    # Log the question
    question = driver.find_element(By.XPATH, current_question_xpath).text
    logging.info(f"Question {question_number}: {question}")  # Changed to include question_number

    # Log all answer options in a list
    answer_options = []
    all_answers = []
    i = 1
    while True:
        try:
            answer_option_xpath = answer_options_xpath_template.format(i)
            answer_option = driver.find_element(By.XPATH, answer_option_xpath).text
            answer_options.append(answer_option)
            letter = chr(64 + i)  # Convert index to letter
            logging.info(f"{letter}: {answer_option}")
            all_answers.append(f"{letter}: {answer_option}")
            i += 1
        except NoSuchElementException:
            break  # Exit loop if no more elements are found

    # Setup for using LangChain with Ollama
    template = """
    You are taking a PHR (professional in human resources) quiz.
    Answer the following question with ONLY the letter associated with the correct answer.
    There is only one correct answer, unless the question states otherwise. 
    If there are multiple correct answers, separate them with a ','.

    Question: {question}

    Answers:
    {all_answers}
    """

    model = OllamaLLM(model='llama3.1')
    prompt = ChatPromptTemplate.from_template(template)
    chain = prompt | model

    # Invoke the model to get the prediction
    formatted_answers = '\n'.join(all_answers)  # Format the answers for display
    result = chain.invoke({"question": question, "all_answers": formatted_answers})
    print("Bot predicted answer:", result)

    # Send the appropriate key press based on the model's prediction
    results = result.strip().split(',')
    for answer in results:
        answer = answer.strip().upper()  # Clean up any spaces and convert to uppercase
        driver.find_element(By.TAG_NAME, 'body').send_keys(answer)
        logging.info(f"Selected answer: {answer}")

    # Wait for user to press 'enter' to move to the next question - FOR TROUBLESHOOTING
    # input("Press 'Enter' when you are ready to proceed to the next question...")

# Replace the previous loop in the complete_quiz function with this one
def complete_quiz(driver):
    total_questions_xpath = '//*[@id="study"]/div/div[2]/div/div/div[2]/div/div/div[2]/div[1]/h2/div[2]'
    total_questions = int(driver.find_element(By.XPATH, total_questions_xpath).text.replace("/ ", ""))
    logging.info(f"Starting quiz with {total_questions} questions.")

    for question_number in range(1, total_questions + 1):
        logging.info(f"Processing Question {question_number}/{total_questions}")  # Log the current question number
        log_question_and_answers(driver, question_number)

        # Simulate pressing the "Right Arrow" to move to the next question
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ARROW_RIGHT)

        # Random sleep time between 5 and 15 seconds to mimic human behavior
        sleep_time = random.uniform(5, 15)
        logging.info(f"Sleeping for {sleep_time:.2f} seconds before next question.")
        time.sleep(sleep_time)

    # Quit quiz
    driver.find_element(By.XPATH, '//*[@id="study"]/div/div[2]/div/div/div[1]/button').click()
    time.sleep(1)

    # Submit quiz
    driver.find_element(By.XPATH, '//*[@id="study"]/div/div[2]/div[2]/div[2]/div[2]/button[1]').click()
    time.sleep(2)

    # Close results
    driver.find_element(By.XPATH, '//*[@id="study"]/div/div[2]/div[3]/button[2]').click()
    time.sleep(2)

# Main function
def main():
    driver = setup_driver(driver_path)

    try:
        login(driver, login_url, email, password)
        
        while True:
            navigate_to_quiz_builder(driver, start_url)
            # troubleshoot_checkboxes(driver)
            configure_quiz_settings(driver)  # Configure the quiz settings
            loops_needed = start_quiz(driver)

            if not loops_needed:
                logging.info("No remaining questions. Exiting.")
                break

            complete_quiz(driver)

    finally:
        driver.quit()
        logging.info("Bot operation complete.")

if __name__ == "__main__":
    main()