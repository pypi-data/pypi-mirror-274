from datetime import datetime
from zoneinfo import ZoneInfo


class Config:
    api_key: str = ''
    BASE_URL = 'https://talkingequipment.com'
    VERSION = 'v1'
    TIME_ZONE = 'America/Edmonton'

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            print('Creating the object')
            cls._instance = super(Config, cls).__new__(cls)
            # Put any initialization here.
        return cls._instance

    def local_date(self):
        time_zone = ZoneInfo(self.TIME_ZONE)
        return datetime.now(time_zone).date()

    def local_date_str(self):
        time_zone = ZoneInfo(self.TIME_ZONE)
        return datetime.now(time_zone).strftime('%Y-%m-%d')

    def local_datetime(self):
        time_zone = ZoneInfo(self.TIME_ZONE)
        return datetime.now(time_zone)


config = Config()
