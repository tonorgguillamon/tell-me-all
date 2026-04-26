from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

import uuid

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from storage.db_engine import Base

class SourceEventCreate(BaseModel):
    source_id: uuid.UUID
    event_type: str = Field(min_length=1, max_length=50)
    summary_text: str = Field(min_length=1, max_length=1000)
    payload_json: dict[str, Any] = Field(default_factory=dict)

class SourceEventRead(BaseModel):
    id: uuid.UUID
    source_id: uuid.UUID
    event_type: str
    summary_text: str
    payload_json: dict[str, Any]
    occurred_at: datetime

    model_config = {"from_attributes": True}

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8) # it ONLY lives in memory -> never written anywhere

class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    model_config = {"from_attributes": True}

class DashboardCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)

class DashboardRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    name: str
    model_config = {"from_attributes": True}


class CardCreate(BaseModel):
    dashboard_id: uuid.UUID
    title: str = Field(min_length=1, max_length=120)
    topic: str = Field(min_length=1, max_length=120)
    role: str = Field(
        default="You are a careful research analyst focused on verified facts, clear summaries, and useful insights.",
        min_length=1,
        max_length=4000,
    )
    creativity: int = Field(default=20, ge=0, le=100)


class CardUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=120)
    topic: str | None = Field(None, min_length=1, max_length=120)
    role: str | None = Field(None, min_length=1, max_length=4000)
    creativity: int | None = Field(None, ge=0, le=100)


class CardRead(BaseModel):
    id: uuid.UUID
    dashboard_id: uuid.UUID
    title: str
    topic: str
    role: str
    creativity: int
    model_config = {"from_attributes": True}


class SourceCreate(BaseModel):
    source_type: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=120)
    config_json: dict[str, Any] = Field(default_factory=dict)


class SourceUpdate(BaseModel):
    source_type: str | None = Field(None, min_length=1, max_length=50)
    name: str | None = Field(None, min_length=1, max_length=120)
    config_json: dict[str, Any] | None = None


class SourceRead(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    source_type: str
    name: str
    config_json: dict[str, Any]
    model_config = {"from_attributes": True}


class User(Base):
    __tablename__ = "users"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255)) # bcrypt produces a ~60 character hash which is irreversible --> safe to store in DB
    dashboards: Mapped[list["Dashboard"]] = relationship(back_populates="user")
    sources: Mapped[list["Source"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Dashboard(Base):
    __tablename__ = "dashboards"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(120))
    user: Mapped["User"] = relationship(back_populates="dashboards")
    cards: Mapped[list["Card"]] = relationship(back_populates="dashboard", cascade="all, delete-orphan")


class Card(Base):
    __tablename__ = "cards"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dashboard_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("dashboards.id"), index=True)
    title: Mapped[str] = mapped_column(String(120))
    topic: Mapped[str] = mapped_column(String(120), index=True)
    role: Mapped[str] = mapped_column(
        Text,
        default="You are a careful research analyst focused on verified facts, clear summaries, and useful insights.",
    )
    creativity: Mapped[int] = mapped_column(Integer, default=20)
    dashboard: Mapped["Dashboard"] = relationship(back_populates="cards")
    card_sources: Mapped[list["CardSource"]] = relationship(back_populates="card", cascade="all, delete-orphan")


class Source(Base):
    __tablename__ = "sources"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    source_type: Mapped[str] = mapped_column(String(50), index=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    config_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)

    user: Mapped["User"] = relationship(back_populates="sources")
    card_sources: Mapped[list["CardSource"]] = relationship(back_populates="source", cascade="all, delete-orphan")
    events: Mapped[list["SourceEvent"]] = relationship(back_populates="source", cascade="all, delete-orphan")


class CardSource(Base):
    __tablename__ = "card_sources"

    card_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("cards.id"), primary_key=True)
    source_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sources.id"), primary_key=True)

    card: Mapped["Card"] = relationship(back_populates="card_sources")
    source: Mapped["Source"] = relationship(back_populates="card_sources")


class SourceEvent(Base):
    __tablename__ = "source_events"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("sources.id"), index=True)
    event_type: Mapped[str] = mapped_column(String(50), index=True)
    summary_text: Mapped[str] = mapped_column(String(1000))
    payload_json: Mapped[dict[str, Any]] = mapped_column(JSON, default=dict)
    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )
    source: Mapped["Source"] = relationship(back_populates="events")

