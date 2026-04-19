from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage.db_engine import Base

class SourceEventCreate(BaseModel):
    source_id: int
    event_type: str = Field(min_length=1, max_length=50)
    summary_text: str = Field(min_length=1, max_length=1000)
    payload_json: dict[str, Any] = Field(default_factory=dict)

class SourceEventRead(BaseModel):
    id: int
    source_id: int
    event_type: str
    summary_text: str
    payload_json: dict[str, Any]
    occurred_at: datetime

    model_config = {"from_attributes": True}

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8) # it ONLY lives in memory -> never written anywhere

class UserRead(BaseModel):
    id: int
    email: EmailStr
    model_config = {"from_attributes": True}

class DashboardCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)

class DashboardRead(BaseModel):
    id: int
    user_id: int
    name: str
    model_config = {"from_attributes": True}


class CardCreate(BaseModel):
    dashboard_id: int
    title: str = Field(min_length=1, max_length=120)
    topic: str = Field(min_length=1, max_length=120)


class CardRead(BaseModel):
    id: int
    dashboard_id: int
    title: str
    topic: str
    model_config = {"from_attributes": True}


class SourceCreate(BaseModel):
    source_type: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=120)
    config_json: dict[str, Any] = Field(default_factory=dict)


class SourceRead(BaseModel):
    id: int
    user_id: int
    source_type: str
    name: str
    config_json: dict[str, Any]
    model_config = {"from_attributes": True}


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255)) # bcrypt produces a ~60 character hash which is irreversible --> safe to store in DB
    dashboards: Mapped[list["Dashboard"]] = relationship(back_populates="user")
    sources: Mapped[list["Source"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Dashboard(Base):
    __tablename__ = "dashboards"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    user: Mapped["User"] = relationship(back_populates="dashboards")
    cards: Mapped[list["Card"]] = relationship(back_populates="dashboard", cascade="all, delete-orphan")


class Card(Base):
    __tablename__ = "cards"
    id: Mapped[int] = mapped_column(primary_key=True)
    dashboard_id: Mapped[int] = mapped_column(ForeignKey("dashboards.id"), index=True)
    title: Mapped[str] = mapped_column(String(120))
    topic: Mapped[str] = mapped_column(String(120), index=True)
    dashboard: Mapped["Dashboard"] = relationship(back_populates="cards")
    card_sources: Mapped[list["CardSource"]] = relationship(back_populates="card", cascade="all, delete-orphan")


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    source_type: Mapped[str] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    config_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

    user: Mapped["User"] = relationship(back_populates="sources")
    card_sources: Mapped[list["CardSource"]] = relationship(back_populates="source", cascade="all, delete-orphan")
    events: Mapped[list["SourceEvent"]] = relationship(back_populates="source", cascade="all, delete-orphan")


class CardSource(Base):
    __tablename__ = "card_sources"

    card_id: Mapped[int] = mapped_column(ForeignKey("cards.id"), primary_key=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"), primary_key=True)

    card: Mapped["Card"] = relationship(back_populates="card_sources")
    source: Mapped["Source"] = relationship(back_populates="card_sources")


class SourceEvent(Base):
    __tablename__ = "source_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    source_id: Mapped[int] = mapped_column(ForeignKey("sources.id"), index=True)
    event_type: Mapped[str] = mapped_column(String(50), index=True)
    summary_text: Mapped[str] = mapped_column(String(1000))
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
    source: Mapped["Source"] = relationship(back_populates="events")

