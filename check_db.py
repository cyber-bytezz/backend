from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://root:Root%401234@localhost:3306/quitq_ecom"
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        print("Database connected successfully!")
except Exception as e:
    print(" Error connecting to the database:", e)
