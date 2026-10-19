import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.models import Product
from tests.factories import seed_catalog


@pytest.fixture
def db():
    """테스트마다 새 인메모리 SQLite를 만들어 쓰고 버린다. 실제 orders.db 파일은 건드리지 않고, 테스트끼리 데이터가 섞이지 않는다."""
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    engine.dispose()


@pytest.fixture
def product(db):
    product = Product(id=1, name="키보드", price=30000, stock=10)
    db.add(product)
    db.commit()
    return product


@pytest.fixture
def seeded(db):
    """키보드·마우스·품절 헤드셋과 주문 두 건을 미리 넣어 둔 DB."""
    return seed_catalog(db)
