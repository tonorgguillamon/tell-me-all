from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage.db_engine import Base

class CardEventCreate(BaseModel):
    card_id: int | None = None
    event_type: str = Field(min_length=1, max_length=50)
    summary_text: str = Field(min_length=1, max_length=1000)
    payload_json: dict[str, Any] = Field(default_factory=dict)

class CardEventRead(BaseModel):
    id: int
    card_id: int | None
    event_type: str
    summary_text: str
    payload_json: dict[str, Any]
    occurred_at: datetime

    model_config = {"from_attributes": True}

class UserCreate(BaseModel):
    email: EmailStr

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


class SourceIngestRequest(BaseModel):
    card_id: int | None = None
    source_kind: str = Field(min_length=1, max_length=30)
    source_name: str = Field(min_length=1, max_length=120)
    event_type: str = Field(min_length=1, max_length=50)
    summary_text: str = Field(min_length=1, max_length=1000)
    payload_json: dict[str, Any] = Field(default_factory=dict)


class SourceIngestResponse(BaseModel):
    event_id: int
    card_id: int | None
    source_kind: str
    source_name: str
    event_type: str
    summary_text: str
    payload_json: dict[str, Any]
    occurred_at: datetime


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    dashboards: Mapped[list["Dashboard"]] = relationship(back_populates="user")


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
    events: Mapped[list["CardEvent"]] = relationship(back_populates="card")


class CardEvent(Base):
    __tablename__ = "card_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    card_id: Mapped[int | None] = mapped_column(ForeignKey("cards.id"), index=True, nullable=True)
    event_type: Mapped[str] = mapped_column(String(50), index=True)
    summary_text: Mapped[str] = mapped_column(String(1000))
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
    card: Mapped["Card | None"] = relationship(back_populates="events")
