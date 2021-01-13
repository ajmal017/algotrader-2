import datetime

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

TRANDINGSTOCKS = ["AAPL", "FB", "ZG", "MSFT", "NVDA", "TSLA", "BEP", "GOOGL"]


def get_tiprank_ratings_to_Stocks(stocks, path, existing_data, notification_callback=None):
    """

    :param stocks: list of stocks to track
    :param path: path to webDriver
    :return: stock-rank dictionary
    """
    # chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.binary_location = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Chrome(path, options=options)
    # driver = webdriver.Chrome(path)

    stocksRanks = {}
    for s in stocks:
        notification_callback.emit("Getting TipRank Rating for : " + s.ticker)
        found = False
        for m, n in existing_data.items():
            date = n['LastUpdate']
            date_tm_dt = datetime.datetime.strptime(date, '%Y-%m-%d')
            date_dt = date_tm_dt.date()
            today_dt = datetime.date.today()
            if n['Stock'] == s.ticker and date_dt == today_dt:
                stocksRanks[s.ticker] = n['tipranksRank']
                notification_callback.emit("Existing  rating from today found: " + stocksRanks[s.ticker])
                found = True
                break
        if not found:
            url = "https://www.tipranks.com/stocks/" + s.ticker + "/stock-analysis"
            driver.get(url)
            selector = "#app > div > div > main > div > div > article > div.client-components-stock-research-tabbed-style__contentArea > div > main > div:nth-child(1) > div.client-components-stock-research-smart-score-style__SmartScore > section.client-components-stock-research-smart-score-style__topSection > div.client-components-stock-research-smart-score-style__rank.client-components-stock-research-smart-score-style__rankSmartScoreTab > div.client-components-stock-research-smart-score-style__OctagonContainer > div > svg > text > tspan"
            xp = '//*[@id="app"]/div/div/main/div/div/article/div[2]/div/main/div[1]/div[2]/section[1]/div[1]/div[1]/div/svg/text/tspan'
            try:
                # element=driver.find_element_by_tag_name('svg')
                element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.TAG_NAME, 'svg'))
                )
                rating = element.text
                stocksRanks[s.ticker] = rating
                notification_callback.emit("Rating found on TipRanks : " + rating)
            except Exception as e:
                notification_callback.emit("Could not find  TipRank Rating for : " + s.ticker)
                continue

    driver.quit()
    return stocksRanks


if __name__ == '__main__':
    r = get_tiprank_ratings_to_Stocks(TRANDINGSTOCKS, "/Users/colakamornik/Desktop/algotrader/Research/chromedriverM")
    r = 3
