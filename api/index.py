import os
import platform
import requests
import logging
from flask import Flask, request, jsonify
from zipfile import ZipFile
from io import BytesIO
from selenium import webdriver
import subprocess

DRIVER_PATH = "/tmp/chromedriver"

def download_chromedriver(force = False):

    system = platform.system()

    if system == 'Linux':
        arch = '64' if platform.architecture()[0] == '64bit' else '32'
        driver_version = 'chromedriver_linux' + arch
    elif system == 'Windows':
        driver_version = 'chromedriver_win32'
    elif system == 'Darwin':
        driver_version = 'chromedriver_mac64'
    else:
        raise ValueError(f"Unsupported OS: {system}")
    
    if force and os.path.exists(DRIVER_PATH):
        os.remove(DRIVER_PATH)

    if force and os.path.exists('/tmp/headless-chromium'):
        os.remove('/tmp/headless-chromium')
        
    # if os.path.exists(DRIVER_PATH) and not force:
    #     logging.info("ChromeDriver already exists. No need to download.")
    #     return

    logging.info("Attempting to download ChromeDriver...")
    version = requests.get("https://chromedriver.storage.googleapis.com/LATEST_RELEASE").text.strip()
    url = f"https://chromedriver.storage.googleapis.com/{version}/{driver_version}.zip"
    response = requests.get(url, stream=True)
    with ZipFile(BytesIO(response.content)) as z:
        z.extractall("/tmp")
    os.chmod(DRIVER_PATH, 0o755)
    
    url = f"https://github.com/adieuadieu/serverless-chrome/releases/download/v1.0.0-57/stable-headless-chromium-amazonlinux-2.zip"
    response = requests.get(url, stream=True)
    with ZipFile(BytesIO(response.content)) as z:
        z.extractall("/tmp")
        os.chmod("/tmp/headless-chromium", 0o755)

    logging.info("ChromeDriver downloaded and extracted successfully.")

def fetch_html_content(url):
    logging.info(f"Fetching content for URL: {url}")
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = '/tmp/headless-chromium'
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x1696')
    chrome_options.add_argument(f"--log-path=/tmp/chromedriver.log")

    result = subprocess.run(['ls', '-al', '/tmp'], stdout=subprocess.PIPE)
    # print(result.stdout.decode('utf-8'))
    # return os.path.exists(DRIVER_PATH)
    # return result.stdout.decode('utf-8')
    browser = webdriver.Chrome(executable_path=DRIVER_PATH, options=chrome_options)
    browser.get(url)
    html = browser.page_source
    browser.quit()
    logging.info(f"Successfully fetched content for URL: {url}")
    return html

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

download_chromedriver(True)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/scrape', methods=['POST'])
def scrape():
    try:
        data = request.json
        url = data['url']
        if not url:
            raise ValueError("URL is required")
        html_content = fetch_html_content(url)
        return jsonify({"html": html_content})
    except Exception as e:
        logging.error(f"Error during scraping: {str(e)}")
        return jsonify({"error": str(e)}), 400

