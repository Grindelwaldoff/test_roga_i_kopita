from typing import Optional, List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.core.db import Base
from app.models.corporations import Corporation


class Activity(Base):
    """Модель деятельностей."""

    name = mapped_column(String(255), unique=True, nullable=False)
    parent_id = mapped_column(
        ForeignKey("activity.id", ondelete="RESTRICT"),
        nullable=True,
    )

    parent: Mapped[Optional["Activity"]] = relationship(
        remote_side="Activity.id",
        back_populates="children",
        lazy="joined",
    )
    children: Mapped[List["Activity"]] = relationship(
        back_populates="parent",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    corporations: Mapped[List["Corporation"]] = relationship(
        "Corporation",
        secondary="corporation_activity_link",
        back_populates="activities",
        lazy="selectin",
    )

    @validates("parent")
    def validate_depth(
        self, _, parent: Optional["Activity"]
    ) -> Optional["Activity"]:
        if parent:
            depth = 2
            ancestor = parent.parent
            while ancestor is not None:
                depth += 1
                ancestor = ancestor.parent
            if depth > 3:
                raise ValueError("Максимальный уровень вложенности деятельности организаций - 3.")
        return parent
