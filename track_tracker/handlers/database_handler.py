from sqlmodel import SQLModel, Session, create_engine, select
import os


class DatabaseHandler:
    def __init__(self):
        self.engine = create_engine(os.getenv("DATABASE_URL"))

    def create_tables(self):
        SQLModel.metadata.create_all(self.engine)

    # def get_session(self):
    #     with Session(self.engine) as session:
    #         yield session
