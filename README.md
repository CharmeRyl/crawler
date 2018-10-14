** attention: this is only used for feasibility analysis and codes are not optimized for production. **

## PyCrawler ##

This is a crawler implemented with Python 3 and Selenium webdriver to fetch the stock data from Sina Finance website. For research and study only!

### Usages ###

For standalone use, modify `config-standalone.json` and run:

```
python standalone.py
```

For distributed use, modify the master and slave sections of `config-distributed.json` with your own configurations.

Run master node:

```
python distributed.py --master
```

Run slave node:

```
python distributed.py --slave
```