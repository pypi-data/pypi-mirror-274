
import datetime
import requests
import pandas as pd

class StockDataDownloader:
    base_url = "https://api.stock.naver.com/chart/domestic/item/"

    def __init__(self, ticker, start_date, end_date, interval='day'):
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval

    def download(self):
        start_datetime = datetime.datetime.strptime(self.start_date, '%Y-%m-%d')
        end_datetime = datetime.datetime.strptime(self.end_date, '%Y-%m-%d')
        start_str = start_datetime.strftime('%Y%m%d') + "0000"
        end_str = end_datetime.strftime('%Y%m%d') + "2359"

        url = f"{self.base_url}{self.ticker}/{self.interval}?startDateTime={start_str}&endDateTime={end_str}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return self.parse_data(data)
        else:
            raise Exception(f"Failed to fetch data: {response.status_code}")

    @staticmethod
    def parse_data(data):
        df = pd.DataFrame(data)
        df['localDate'] = pd.to_datetime(df['localDate'])
        df.set_index('localDate', inplace=True)
        df.rename(columns={
            'closePrice': 'Close',
            'openPrice': 'Open',
            'highPrice': 'High',
            'lowPrice': 'Low',
            'accumulatedTradingVolume': 'Volume',
            'foreignRetentionRate': 'ForeignHold'
        }, inplace=True)
        # Convert relevant columns to numeric
        df[['Close', 'Open', 'High', 'Low', 'Volume']] = df[['Close', 'Open', 'High', 'Low', 'Volume']].apply(pd.to_numeric)
        df['ForeignHold'] = df['ForeignHold'].astype(float)
        return df
