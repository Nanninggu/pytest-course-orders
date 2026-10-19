"""직접 실행해 볼 때 쓰는 초기화: 테이블을 만들고 예제 상품을 넣는다(python -m app.init_db). 테스트는 이 파일을 쓰지 않는다."""
from app.database import Base, SessionLocal, engine
from app.models import Product

Base.metadata.create_all(engine)
with SessionLocal() as db:
    if db.query(Product).count() == 0:
        db.add_all([Product(name="키보드", price=30000, stock=10), Product(name="마우스", price=15000, stock=20)])
        db.commit()
print("초기화 완료")
