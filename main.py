import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time

GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSd_XfH0a8BV2HpzNl8_zS0lN_zYWiYQfFVtpMz9cWYDRYiZ9w/viewform" \
              "?usp=sf_link "

ZILLOW_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C" \
             "%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A" \
             "-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C" \
             "%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A" \
             "%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse" \
             "%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B" \
             "%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D" \
             "%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min" \
             "%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D "

header = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/92.0.4515.131 YaBrowser/21.8.0.1716 Yowser/2.5 Safari/537.36",
    "Accept-Language": "ru,fr;q=0.9"
}

response = requests.get(url=ZILLOW_URL, headers=header)
soup = BeautifulSoup(response.content, "html.parser")

property_links = [link['href'] for link in soup.find_all(name="a", class_="list-card-link")][::2]
new_links = []

for link in property_links:
    if 'https' not in link:
        link = f"https://www.zillow.com{link}"
    new_links.append(link)

list_prices = [price.get_text() for price in soup.select(".list-card-price")]
new_prices = []

for price in list_prices:
    if "1 bd" in price:
        price = price.split('+')[0]
    if "/mo" in price:
        price = price.split('/')[0]
    new_prices.append(price)


list_addresses = [address.get_text() for address in soup.find_all(name="address", class_="list-card-addr")]
new_addresses = []

for address in list_addresses:
    if "|" in address:
        address = address.split("|")[-1]
    new_addresses.append(address)

for i in range(len(new_addresses)):
    chrome_driver_path = "/Users/anastasia/DevLab/chromedriver"
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get(GOOGLE_FORM)

    time.sleep(2)

    address_input = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_input = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link_input = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    send_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span/span')

    address_input.send_keys(new_addresses[i])
    price_input.send_keys(new_prices[i])
    link_input.send_keys(new_links[i])

    send_button.click()

    driver.close()

