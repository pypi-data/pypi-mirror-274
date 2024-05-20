from .rsi import compute_rsi
from .stock_listing import StockListing
from .stock_data import StockDataDownloader

def download(ticker, start_date, end_date, interval='day'):
    downloader = StockDataDownloader(ticker, start_date, end_date, interval)
    return downloader.download()
