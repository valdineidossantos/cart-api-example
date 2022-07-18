from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

host="cart_api_example_db"
user="cart-api-example-user"
password="ultra-secret-password123"
db_name="cart-api-example-db"
engine = create_engine(f"postgresql://{user}:{password}@{host}/{db_name}", echo=True)
Base=declarative_base()
LocalSession = sessionmaker(bind=engine)
