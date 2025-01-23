import os 
import logging
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv()


class Config():
    SECRET_KEY=os.getenv("SECRET_KEY")
    MONGO_URI=os.getenv("MONGO_URI")
    JWT_SECRET_KEY=os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(hours=int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES")))
    MAIL_SERVER=os.getenv("MAIL_SERVER")
    MAIL_PORT=os.getenv("MAIL_PORT","587")
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD")
    LOGGING_LEVEL = logging.DEBUG  
    LOGGING_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    LOGGING_FILE = 'app.log' 

    @staticmethod
    def init_app(app):
        logging.basicConfig(
            level=Config.LOGGING_LEVEL,
            format=Config.LOGGING_FORMAT,
            handlers=[
                logging.FileHandler(Config.LOGGING_FILE),
            ]
        )