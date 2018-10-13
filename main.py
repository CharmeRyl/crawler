from crawler import Crawler
from mongodb import MongoDb

stock_ids = [600519, 600520, 600521]
year_start, year_end = 2016, 2017


def main():
    crawler = Crawler()
    db = MongoDb()

    for stock_id in stock_ids:
        data = crawler.fetch_stock_data(stock_id, year_start, year_end)
        db.append_one(data)


if __name__ == '__main__':
    main()
