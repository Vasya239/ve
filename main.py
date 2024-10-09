import requests
import fake_useragent
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pickle
import os
from aiogram.enums.parse_mode import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram import types, filters
import json
import logging
from selenium.webdriver.common.keys import Keys
from aiogram import Dispatcher, Bot
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio

bot = Bot(token = '7861578202:AAEDBo_5esnNDAUW7Q8iF4JUofnzfDiAGm0',
    default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher(storage=MemoryStorage())

@dp.message(filters.CommandStart())
async def parse(message: types.Message):
    await message.answer('Подождите немного...')
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")
    options.add_argument("--headless")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    service=Service(ChromeDriverManager().install())
    proxy_for_chrome = '168.196.238.196:9678'
    options.add_argument(f'--proxy-server={proxy_for_chrome}')
    
    browser = webdriver.Chrome(service=service, options = options)
    
    proxy = 'http://168.196.238.196:9678'
    
    proxies = {
        'http': proxy,
        'https': proxy
    }

    stealth(browser,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Elementary OS",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    
    domen = 'https://kwork.ru/'
    user = fake_useragent.UserAgent().random

    headers = {
        'User-Agent': user
    }
    
    session = requests.Session()
    
    response_get_cookie = session.get(domen, headers = headers, proxies = proxies)
    print('Получил куки')
    time.sleep(10)

    link_auth = 'https://kwork.ru/api/user/login'

    login = 'vasya239999@gmail.com'
    password = 'Vasya239'

    data = {
        'g-recaptcha-response':	"",
        'jlog': '1',
        'l_password': password,
        'l_remember_me': "1",
        'l_username': login,
        'recaptcha_pass_token': "",
        'track_client_id': 'false'
    }
    
    headers_auth = {
        'User-Agent': user,
        'Host': 'kwork.ru',
        'Origin': 'https://kwork.ru',
        'Referer': 'https://kwork.ru/'
    }

    response_auth = session.post(link_auth, data = data, headers = headers_auth)
    print('Авторизовался')
    time.sleep(10)

    link_for_referer = 'https://kwork.ru/seller'
    
    browser.get(link_for_referer)
    
    time.sleep(10)

    for key, value in session.cookies.get_dict().items():
        browser.add_cookie({'name': key, 'value': value, 'domain': 'kwork.ru'})
    
    await message.answer('Парсинг начат!')
    
    browser.implicitly_wait(30)

    while True:
        try:
            time1 = time.time()
            browser.refresh()
            link_orders = 'https://kwork.ru/projects?c=41&attr=211'
            browser.get(link_orders)
            links = []
            block = browser.find_element(By.XPATH, '/html/body/div[9]/div[3]/div/div[2]/div[2]/div[3]/div/div[1]')
            blocks = block.find_elements(By.CLASS_NAME, 'want-card.want-card--list.want-card--hover')
            for block in blocks:
                path = os.path.dirname(__file__)
                with open(f'{path}/data.json') as file:
                    data = json.load(file)
                link = block.find_element(By.TAG_NAME, 'a').get_attribute('href')
                if link not in list(data):
                    title = block.find_element(By.TAG_NAME, 'a').text
                    block.find_element(By.CLASS_NAME, 'kw-link-dashed').click()
                    text = block.find_element(By.CLASS_NAME, 'breakwords.first-letter.overflow-hidden').text
                    price = block.find_element(By.CLASS_NAME, 'wants-card__right').text
                    await message.answer(f'🔔Новый заказ🔔\nЗаголовок: {title}\n{price}\nСсылка: {link}\nКраткое описание: {text}')
                links.append(link)
            path = os.path.dirname(__file__)
            data = {link:'' for link in links}
            with open(f'{path}/data.json', 'w') as file:
                json.dump(data, file)
            time.sleep(12)
            time2 = time.time()
            print(time2 - time1)
        except:
            pass

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
