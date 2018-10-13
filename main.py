import crawler
import mongodb


def main():
    stock_id, year_start, year_end = 600519, 2016, 2017
    data = crawler.fetch_stock_data(stock_id, year_start, year_end)
    db = mongodb.MongoDb()
    db.put_one(data)


if __name__ == '__main__':
    main()
