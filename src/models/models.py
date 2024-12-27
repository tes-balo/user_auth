from datetime import datetime
# from uuid import UUID

# from email.policy import default
from sqlalchemy import (
    UUID,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    String,
    func,
)

from sqlalchemy.orm import relationship, mapped_column, Mapped
from uuid_extensions import uuid7  # type: ignore

from db.database import Base


class BaseTableModel(Base):
    __abstract__ = True

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def to_dict(self):
        obj_dict = self.__dict__.copy()  # convert the new instance to dictionary\
        if isinstance(self.created_at, datetime):
            obj_dict["created_at"] = self.created_at.isoformat()
            obj_dict["updated_at"] = self.created_at.isoformat()
        # delete sqlalchemy info
        return obj_dict


class UserOrganisation(BaseTableModel):
    __tablename__ = "user_organisation"

    # organisation_id = Column(Integer, primary_key=True)
    # organisation_id: Mapped[str] = mapped_column(
    #     UUID(as_uuid=True), primary_key=True, default=lambda: str(uuid7())
    # )

    organisation_id: Mapped[UUID[str]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("organisations.organisation_id"),
        primary_key=True,
        default=lambda: uuid7(),
    )
    user_id: Mapped[UUID[str]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id"),
        primary_key=True,
        default=lambda: uuid7(),
    )

    roles: Mapped[Enum] = mapped_column(
        Enum(
            "admin",
            "guest",
            "owner",
            "user",
            name="user_organisation_roles",
        ),
        nullable=False,
        default="user",
    )


class User(BaseTableModel):
    __tablename__ = "users"

    user_id: Mapped[UUID[str]] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=lambda: uuid7()
    )
    firstname = Column(String(30), nullable=False)
    lastname = Column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    phone = Column(String)  # move to profile model later

    # is_active: Mapped[bool] = mapped_column(default=True)

    organisations = relationship(
        "Organisation", secondary="user_organisation", back_populates="users"
    )
    cascade = ("all, delete",)


class Organisation(BaseTableModel):
    __tablename__ = "organisations"

    organisation_id: Mapped[UUID[str]] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=lambda: uuid7()
    )
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    description: Mapped[str] = mapped_column(nullable=True)
    # user_id = Column(Integer, ForeignKey("users.user_id"))

    users = relationship(
        "User", secondary="user_organisation", back_populates="organisations"
    )
