from sqlalchemy import create_engine

def connect():
    engine = create_engine("postgresql+psycopg2://postgres:Iyas.2020@localhost:5432/community")
    return engine
