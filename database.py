from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

#DATABASE_URL = "mysql+pymysql://root:root@localhost:3306/mobiles_db"
DATABASE_URL="mysql+pymysql://mysql-1502a305-vetchasrikavya77-984c.k.aivencloud.com:24214/defaultdb"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
