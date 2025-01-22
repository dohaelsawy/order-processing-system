import os 
from dotenv import load_dotenv

load_dotenv()


class Config():
    SECRET_KEY=os.getenv("SECRET_KEY")
    MONGO_URI=os.getenv("MONGO_URI")
    MAIL_SERVER=os.getenv("MAIL_SERVER")
    MAIL_PORT=os.getenv("MAIL_PORT","587")
    MAIL_USE_TLS=True
    MAIL_USERNAME=os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD")