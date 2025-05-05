from sqlalchemy import BigInteger, DateTime, String, Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine


engine = create_async_engine(url="sqlite+aiosqlite:///db_todo.sqlite3", echo=True)

async_session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column()
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(32))
    full_name: Mapped[str] = mapped_column(String(64))
    created_at: Mapped[DateTime] = mapped_column(DateTime)
    updated_at: Mapped[DateTime] = mapped_column(DateTime)
    
    
class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(512))
    competed: Mapped[bool] = mapped_column(default=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"), ondelete="CASCADE")
    
    
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
