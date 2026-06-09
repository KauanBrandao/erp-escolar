import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()


_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL_NON_POOLING")

if not _url:
    raise ValueError("Nenhuma variavel de banco encontrada (DATABASE_URL ou POSTGRES_URL_NON_POOLING)!")

# Garante o dialeto psycopg2 para SQLAlchemy
if _url.startswith("postgres://"):
    _url = _url.replace("postgres://", "postgresql+psycopg2://", 1)
elif _url.startswith("postgresql://"):
    _url = _url.replace("postgresql://", "postgresql+psycopg2://", 1)

SQLALCHEMY_DATABASE_URL = _url

_is_supabase = "supabase" in SQLALCHEMY_DATABASE_URL
_connect_args = {}
if _is_supabase and "pooler.supabase" not in SQLALCHEMY_DATABASE_URL:
    _connect_args = {"sslmode": "require"}

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args=_connect_args,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()