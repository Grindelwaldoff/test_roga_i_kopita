from sqlalchemy import Column, ForeignKey, String, Table, UniqueConstraint
from sqlalchemy.orm import mapped_column, relationship

from app.core.db import Base


corporation_activity_link = Table(
    "corporation_activity_link",
    Base.metadata,
    Column(
        "corporation_id",
        ForeignKey("corporation.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "activity_id",
        ForeignKey("activity.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Corporation(Base):
    """Модель организаций."""

    name = mapped_column(String(255), nullable=False, index=True)
    building_id = mapped_column(
        ForeignKey("building.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )

    building = relationship(
        "Building",
        back_populates="corporations",
        lazy="joined",
    )
    phones = relationship(
        "CorporationPhone",
        back_populates="corporation",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    activities = relationship(
        "Activity",
        secondary="corporation_activity_link",
        back_populates="corporations",
        lazy="selectin",
    )


class CorporationPhone(Base):
    """Модель телефонов организаций."""

    __tablename__ = "corporation_phones"
    __table_args__ = (
        UniqueConstraint(
            "corporation_id",
            "phone_number",
            name="uq_phone_per_corporation",
        ),
    )

    corporation_id = mapped_column(
        ForeignKey("corporation.id", ondelete="CASCADE"),
        nullable=False,
    )
    phone_number = mapped_column(String(32), nullable=False)

    corporation = relationship(
        "Corporation",
        back_populates="phones",
        lazy="joined",
    )
