from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# Base de datos SQLite local almacenada en la raíz del proyecto
DATABASE_URL = "sqlite:///./sensorhub.db"

# engine para SQLite con soporte multihilo
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# Fabrica de sesiones tipadas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base declarativa (SQLAlchemy 2.0)
class Base(DeclarativeBase):
    pass

# Inyección de dependencia para obtener la sesión de BD por request
def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()