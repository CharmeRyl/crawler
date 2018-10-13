from crawler import Crawler
from mongodb import MongoDb

stock_id = 600519
year_start = 2016
year_end = 2017


def main():
    crawler = Crawler()
    db = MongoDb()

    data = crawler.fetch_stock_data(stock_id, year_start, year_end)
    db.append_one(data)


if __name__ == '__main__':
    main()
