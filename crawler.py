from selenium import webdriver
from urllib import parse
import datetime

__url_pattern__ = "http://money.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/{0}.phtml?{1}"

__xpath_name__ = "//div[@class='centerImgBlk']/div[@id='toolbar']/div[@class='tbtb01']/h1/a"
__xpath_table__ = "//*[@id='FundHoldSharesTable']/tbody/tr"


def create_driver():
    return webdriver.Chrome()


def fetch_stock_data(stock_id, year_start, year_end=datetime.datetime.now().year):
    year_start = int(year_start)
    year_end = int(year_end)
    driver = create_driver()
    data = dict(
        _id=int(stock_id),
        name=fetch_stock_name(driver, stock_id),
        data=[]
    )

    for year in range(year_end, year_start - 1, -1):
        data_year = fetch_stock_data_annually(driver, stock_id, year)
        data["data"].extend(data_year)

    driver.close()
    return data


def fetch_stock_data_annually(driver, stock_id, year):
    data = []
    for q in range(4, -1, -1):
        driver.get(generate_url(stock_id, year, q))
        table = driver.find_elements_by_xpath(__xpath_table__)[1:]
        for row in table:
            row_data = row.text.split('\n')
            row_dict = dict(
                date=row_data[0],               # 日期
                price_open=float(row_data[1]),  # 开盘价
                price_high=float(row_data[2]),  # 最高价
                price_end=float(row_data[3]),   # 收盘价
                price_low=float(row_data[4]),   # 最低价
                count_deal=int(row_data[5]),    # 交易量（股）
                amount_tx=float(row_data[6])    # 交易额
            )
            data.append(row_dict)

    return data


def fetch_stock_name(driver, stock_id):
    driver.get(__url_pattern__.format(stock_id, "l"))
    return driver.find_element_by_xpath(__xpath_name__).text


def generate_url(stock_id, year, quarter):
    get_params = parse.urlencode({"year": year, "jidu": quarter})
    return __url_pattern__.format(stock_id, get_params)