from sqlalchemy import create_engine

def connect():
    engine = create_engine("postgresql+psycopg2://username:password@localhost:5432/community")
    return engine
