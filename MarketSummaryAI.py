import requests
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from PIL import Image
import urllib.request
from datetime import date
import calendar
import openai

start_time = time.time()

# GroupMe Bot ID and access token, OpenAI API Key
BOT_ID = 'YOUR_BOT_ID'
ACCESS_TOKEN = 'ACCESS_TOKEN'
OPEN_AI_API_KEY = "YOUR_OPEN_AI_API_KEY"

# API URLs for GroupMe
GROUPME_API_URL = 'https://api.groupme.com/v3/bots/post'
GROUPME_IMAGE_SERVICE_URL = 'https://image.groupme.com/pictures'


# Initialize webdriver instance
def get_driver_instance():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument('--disable-gpu')
    options.add_argument('--log-level=3')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36")

    driver = webdriver.Chrome(options=options, service_log_path="NUL")
    return driver


# Function to retrieve crypto heatmap screenshot
def Crypto_HeatMap(driver):
    driver.get('https://quantifycrypto.com/heatmaps')

    time.sleep(1.5)

    driver.set_window_size(1080,1080)
    driver.save_screenshot(r'C:\YOUR_FILE_PATH\crypto_heatmap.png')

    im = Image.open(r'C:\YOUR_FILE_PATH\crypto_heatmap.png').crop((left:=15, top:=170, right:=1065, bottom:=700))
    im.save(r'C:\YOUR_FILE_PATH\crypto_heatmap.png')


# Function to retrieve Fortune 500 heatmap 
def Fortune500_HeatMap(driver):
    driver.get("https://finviz.com/map.ashx")
    driver.set_window_size(1080,1080)
    
    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div[1]/div[3]/button[1]"))).click()

    WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='root']/div[1]/div[3]/button[2]"))).click()
    time.sleep(1)
    
    soup = BeautifulSoup(driver.page_source, "html.parser").text.strip()
    image_link = soup[soup.index("https://finviz.com/published_map.ashx?t=sec&st=d1&f"):soup.index("https://finviz.com/published_map.ashx?t=sec&st=d1&f") + 77]
    
    today = image_link[image_link.index("f=") + 2:image_link.index("f=") + 8]
    image_id = image_link[image_link.index("sec_d1_") + 7:]

    driver.get(f"https://finviz.com/publish/{today}/sec_d1_{image_id}.png")
    print(f"https://finviz.com/publish/{today}/sec_d1_{image_id}.png")
    heatmap = driver.find_element(By.XPATH, "/html/body/img")
    heatmap.screenshot("Fortune500_HeatMap.png")
    

# Function to upload an image to GroupMe Image Service and return its URL
def upload_image(image_path):
    time.sleep(1)
    headers = {'X-Access-Token': ACCESS_TOKEN, 'Content-Type': 'image/jpeg'}
    with open(image_path, 'rb') as image_file:
        response = requests.post(GROUPME_IMAGE_SERVICE_URL, headers=headers, data=image_file)

    if response.ok:
        return response.json()['payload']['url']

    return None


# Function to send an ima to a GroupMe chat with an optional image URL
def send_image(image_url=None):
    payload = {'bot_id': BOT_ID}

    if image_url:
        payload['attachments'] = [{'type': 'image', 'url': image_url}]

    response = requests.post(GROUPME_API_URL, json=payload)

    print(f'Error sending message: {response.status_code}') if response.status_code != 202 else None


# Function to summarize CNBC Five Things to Know
def AISummary(Article):
    openai.api_key = "OPEN_AI_API_KEY"
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": "You are given a 5 things to know before the stock market opens article, your job is to give each point a brief headline like summary for a tweet"},
                  {"role": "user", "content": f"Please provide a brief summary of each point from this article while keeping the response under 1,000 characters: {Article}"}])
    
    print("Characters:", len(completion['choices'][0]['message']['content']),"\nWord Count:", len(completion['choices'][0]['message']['content'].split()))

    if len(completion['choices'][0]['message']['content']) > 1000:
        print("ERROR: Summary Too long. Retrying...")
        AISummary(Article)
    else:
        return completion['choices'][0]['message']['content']


# Function that fetches CNBC's Five Things to Know
def FiveThingsToKnow():
    today = date.today()

    day_of_week = calendar.day_name[today.weekday()].lower()
    month_name = today.strftime('%B').lower()
    day = today.strftime('%d')
    formatted_date = today.strftime('%Y/%m/%d')

    article = ""

    if day_of_week != 5 and day_of_week != 6:
        response = requests.get(f'https://www.cnbc.com/{formatted_date}/5-things-to-know-before-the-stock-market-opens-{day_of_week}-{month_name}-{int(day)}.html')
        print(f'https://www.cnbc.com/{formatted_date}/5-things-to-know-before-the-stock-market-opens-{day_of_week}-{month_name}-{int(day)}.html')

        soup = BeautifulSoup(response.text, 'html.parser')

        subtitles = soup.find_all('h2', class_='ArticleBody-subtitle')
        bodies = soup.find_all('div', class_='group')

        for subtitle, body in zip(subtitles, bodies[2:]):
            article += subtitle.text + '\n' + body.text + '\n'
        
        return article
    
    else:
        return "The market it closed."


# Function that sends a plain text group me message
def send_groupme_message(Article):
    response = requests.post(url="https://api.groupme.com/v3/bots/post", json={"bot_id": BOT_ID, "text": Article}, headers={'X-Access-Token': ACCESS_TOKEN})
    print(response)
    
    if int(response.status_code) == 202:
        return None
    
    elif int(response.status_code) != 400:
        exit()

    # Retry safeguard
    else:
        print("ERROR: Failed to Send Market Summary. Retrying...")
        Article = FiveThingsToKnow()
        if Article != "The market it closed.":
            Summary = AISummary(Article)
            send_groupme_message(Summary)
        else:
            send_groupme_message("The market it closed, no market summary.")


if __name__ == '__main__':
    with get_driver_instance() as driver:
        Crypto_HeatMap(driver)
        crypto_heatmap_path = r'C:\YOUR_FILE_PATH\Crypto_HeatMap.png'
        crypto_image_url = upload_image(crypto_heatmap_path)
        print("Crypto HeatMap Complete")

        Fortune500_HeatMap(driver)
        Fortune500_HeatMap_path = r'C:\YOUR_FILE_PATH\Fortune500_HeatMap.png'
        stocks_image_url = upload_image(Fortune500_HeatMap_path)
        print("Stock Market HeatMap Complete")

        if crypto_image_url:
            send_image(crypto_image_url)
        
        if stocks_image_url:
            send_image(stocks_image_url)
        print("Images Sent")

        
    Article = FiveThingsToKnow()
    if Article != "The market it closed.":
        Summary = AISummary(Article)
        send_groupme_message(Summary)
    else:
        send_groupme_message("The market it closed, no market summary.")
    
    print("Script Complete")

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds")
