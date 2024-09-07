from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import csv
import os
from dotenv import load_dotenv

load_dotenv()
TWITTER_USERNAME = os.getenv('TWITTER_USERNAME')
TWITTER_PASSWORD = os.getenv('TWITTER_PASSWORD')

def setup_driver():
    options = webdriver.ChromeOptions()
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver

def login_to_twitter(driver):
    driver.get('https://twitter.com/login')
    wait = WebDriverWait(driver, 10)
    
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "text")))
    username_field.send_keys(TWITTER_USERNAME)
    username_field.send_keys(Keys.RETURN)
    time.sleep(2)
    
    try:
        phone_or_username_field = wait.until(EC.presence_of_element_located((By.NAME, "text")))
        phone_or_username_field.clear()
        phone_or_username_field.send_keys(os.getenv('PHONE_NUMBER'))
        phone_or_username_field.send_keys(Keys.RETURN)
        time.sleep(2)
    except Exception as e:
        print("No se mostró la ventana de verificación de inicio de sesión:", e)

    try:
        password_field = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        password_field.send_keys(TWITTER_PASSWORD)
        password_field.send_keys(Keys.RETURN)
        time.sleep(3)
    except Exception as e:
        print("No se pudo encontrar el campo de contraseña:", e)

def scroll_and_load_tweets(driver, num_tweets=20):
    tweets_data = []
    tweet_count = 0
    scroll_attempts = 0

    while tweet_count < num_tweets and scroll_attempts < 10:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        tweets = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
        print(f"Total de tweets encontrados: {len(tweets)}")

        if len(tweets) <= tweet_count:
            print("No se cargaron más tweets.")
            break
        
        for tweet in tweets[tweet_count:]:
            if tweet_count >= num_tweets:
                break
            try:
                try:
                    text_element = tweet.find_element(By.XPATH, './/div[@data-testid="tweetText"]//span')
                    text = text_element.text if text_element else "Imagen o Retweet"
                except Exception:
                    text = "Imagen o Retweet"

                try:
                    date_element = tweet.find_element(By.XPATH, './/time')
                    date = date_element.get_attribute('datetime') if date_element else 'Fecha no disponible'
                except Exception:
                    date = 'Fecha no disponible'

                try:
                    retweets_element = tweet.find_element(By.XPATH, './/button[@data-testid="retweet"]//span[contains(@class, "css-1jxf684")]')
                    retweets_count = retweets_element.text if retweets_element else '0'
                except Exception:
                    retweets_count = '0'

                try:
                    likes_element = tweet.find_element(By.XPATH, './/button[@data-testid="like"]//span[contains(@class, "css-1jxf684")]')
                    likes_count = likes_element.text if likes_element else '0'
                except Exception:
                    likes_count = '0'

                tweet_url = tweet.find_element(By.XPATH, './/a[@href]').get_attribute('href')

                tweets_data.append([text, date, retweets_count, likes_count, tweet_url])
                tweet_count += 1
                
                # Imprimir el tweet de forma legible
                print(f"\nTweet {tweet_count}:")
                print(f"  Texto: {text}")
                print(f"  Fecha: {date}")
                print(f"  Retweets: {retweets_count}")
                print(f"  Likes: {likes_count}")
                print(f"  URL: {tweet_url}\n")
                
            except Exception as e:
                print(f"Error extracting tweet: {e}. Tweet número: {tweet_count + 1}.")
        
        scroll_attempts += 1

    return tweets_data

def save_to_csv(tweets_data, filename='tweets.csv'):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Texto', 'Fecha', 'Retweets', 'Likes', 'URL'])
        writer.writerows(tweets_data)

def close_driver(driver):
    driver.quit()

if __name__ == "__main__":
    driver = setup_driver()
    
    try:
        login_to_twitter(driver)
        tweets = scroll_and_load_tweets(driver, num_tweets=20)
        save_to_csv(tweets)
    finally:
        close_driver(driver)
