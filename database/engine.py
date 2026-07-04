"""
═══════════════════════════════════════════════════════════════════════
CryptoPulse AI Enterprise
Database Engine

Responsibilities:
- Database connection management
- Async session handling
- Support SQLite (dev) & PostgreSQL (prod)
═══════════════════════════════════════════════════════════════════════
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError

from core.logger import Logger
from config.settings import Settings


# ==========================================================
# LOGGER
# ==========================================================

logger = Logger("Database")


# ==========================================================
# BASE MODEL
# ==========================================================

Base = declarative_base()


# ==========================================================
# DATABASE ENGINE
# ==========================================================

class DatabaseEngine:
    """
    Central database connection manager
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self.engine = None
        self.SessionLocal = None

    # ======================================================
    # INIT ENGINE
    # ======================================================

    def connect(self):
        """
        Create database connection
        """

        try:
            logger.info("🗄️ Initializing database connection...")

            self.engine = create_engine(
                self.settings.DATABASE_URL,
                pool_size=20,
                max_overflow=30,
                pool_pre_ping=True,
                echo=self.settings.DEBUG,
            )

            self.SessionLocal = sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self.engine
            )

            logger.info("✅ Database connected successfully")

        except SQLAlchemyError as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise

    # ======================================================
    # GET SESSION
    # ======================================================

    def get_session(self):
        """
        Create new database session
        """
        if not self.SessionLocal:
            raise RuntimeError("Database not initialized")

        return self.SessionLocal()

    # ======================================================
    # CLOSE ENGINE
    # ======================================================

    def close(self):
        """
        Close database connection
        """
        if self.engine:
            self.engine.dispose()
            logger.warning("🛑 Database connection closed")
