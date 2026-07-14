import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy import String, Text, ForeignKey, DateTime, Boolean, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from app.database.database import Base
from app.models.enums import ComplaintStatus, Priority, WasteType, ComplaintCategory

class Complaint(Base):
    """
    Complaint model tracking reported waste management issues.
    """
    __tablename__ = "complaints"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    category: Mapped[ComplaintCategory] = mapped_column(Enum(ComplaintCategory, name="complaintcategory_enum", create_type=False), index=True, nullable=False)
    waste_type: Mapped[WasteType] = mapped_column(Enum(WasteType, name="wastetype_enum", create_type=False), nullable=False)
    priority: Mapped[Priority] = mapped_column(Enum(Priority, name="priority_enum", create_type=False), default=Priority.MEDIUM, index=True, nullable=False)
    status: Mapped[ComplaintStatus] = mapped_column(Enum(ComplaintStatus, name="complaintstatus_enum", create_type=False), default=ComplaintStatus.PENDING, index=True, nullable=False)
    
    # Location tracking
    building_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("buildings.id"), index=True, nullable=False)
    floor: Mapped[str | None] = mapped_column(String(50), nullable=True)
    room: Mapped[str | None] = mapped_column(String(50), nullable=True)
    landmark: Mapped[str | None] = mapped_column(String(100), nullable=True)
    location_description: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Images (Relative Paths)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    completion_image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    
    # Relationships
    reported_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    assigned_to: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("users.id"), index=True, nullable=True)
    
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, index=True, nullable=False)
    
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )
    
    # Navigation properties
    reporter = relationship("User", foreign_keys=[reported_by], back_populates="complaints_reported", lazy="selectin")
    assignee = relationship("User", foreign_keys=[assigned_to], back_populates="complaints_assigned", lazy="selectin")
    building = relationship("Building", lazy="selectin")
    history: Mapped[List["ComplaintHistory"]] = relationship(
        "ComplaintHistory", 
        back_populates="complaint", 
        cascade="all, delete-orphan"
    )

class ComplaintHistory(Base):
    """
    Immutable audit trail for complaint status transitions.
    """
    __tablename__ = "complaint_history"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    complaint_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("complaints.id", ondelete="CASCADE"), index=True, nullable=False)
    
    old_status: Mapped[ComplaintStatus | None] = mapped_column(Enum(ComplaintStatus, name="complaintstatus_enum", create_type=False), nullable=True)
    new_status: Mapped[ComplaintStatus] = mapped_column(Enum(ComplaintStatus, name="complaintstatus_enum", create_type=False), nullable=False)
    
    remarks: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True, nullable=False)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    complaint = relationship("Complaint", back_populates="history")
    updater = relationship("User", foreign_keys=[updated_by])
