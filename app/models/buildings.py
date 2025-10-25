from sqlalchemy import CheckConstraint, Float, String
from sqlalchemy.orm import mapped_column, relationship

from app.core.db import Base


class Building(Base):
    """Модель зданий."""

    __table_args__ = (
        CheckConstraint(
            "-90 <= latitude AND latitude <= 90",
            name="ck_building_lat_range",
        ),
        CheckConstraint(
            "-180 <= longitude AND longitude <= 180",
            name="ck_building_lon_range",
        ),
    )

    address = mapped_column(String(255), nullable=False, unique=True)
    latitude = mapped_column(Float, nullable=False)
    longitude = mapped_column(Float, nullable=False)

    corporations = relationship(
        "Corporation",
        back_populates="building",
        cascade="all, delete-orphan",
        passive_deletes=True,
        lazy="selectin",
    )
