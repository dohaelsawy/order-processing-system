import os 
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