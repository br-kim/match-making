from database import SessionLocal


def get_db():
    db = SessionLocal()
    db.begin()
    try:
        yield db
    finally:
        db.close()
