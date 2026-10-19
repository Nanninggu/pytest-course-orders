from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = "sqlite:///./orders.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    pass


def get_db():  # pragma: no cover (테스트가 바꿔 끼움)
    """요청마다 DB 세션을 하나 열고, 끝나면 닫는다(FastAPI 의존성)."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
