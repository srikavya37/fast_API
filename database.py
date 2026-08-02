#database
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
load_dotenv()

#DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/mobiles_db"
DATABASE_URL = "mysql+pymysql://avnadmin:AVNS_haq_unkwgk-4nB_Wa5U@mysql-1502a305-vetchasrikavya77-984c.k.aivencloud.com:24214/defaultdb"
DATABASE_URL=os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
