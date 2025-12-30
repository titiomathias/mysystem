from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from core.config import settings

if settings.mysql_configured:
    DATABASE_URL = (
        f"mysql+pymysql://{settings.DB_USER}:"
        f"{settings.DB_PASSWORD}@"
        f"{settings.DB_HOST}:"
        f"{settings.DB_PORT}/"
        f"{settings.DB_NAME}"
    )
    print("[+] Using MySQL/MariaDB database [+]")


else:
    DATABASE_URL = "sqlite:///./dev_temp.db"
    print("[!] Using SQLite fallback database [!]")

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}
    if DATABASE_URL.startswith("sqlite")
    else {}
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
