import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.database.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.building import Building
from app.models.complaint import Complaint, ComplaintHistory
from app.models.enums import ComplaintStatus, Priority, WasteType, ComplaintCategory
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def seed_db():
    db: Session = SessionLocal()
    
    # Check if we already seeded
    if db.query(User).first():
        print("Database already seeded. Skipping.")
        db.close()
        return

    # Create Users
    admin = User(
        full_name="Admin User",
        email="admin@ecotrack.edu",
        hashed_password=get_password_hash("password123"),
        role=UserRole.ADMIN
    )
    
    staff = [
        User(full_name=f"Staff {i}", email=f"staff{i}@ecotrack.edu", hashed_password=get_password_hash("123456"), role=UserRole.STAFF)
        for i in range(1, 4)
    ]
    
    students = [
        User(full_name=f"Student {i}", email=f"student{i}@ecotrack.edu", hashed_password=get_password_hash("password123"), role=UserRole.STUDENT)
        for i in range(1, 6)
    ]

    db.add(admin)
    db.add_all(staff)
    db.add_all(students)
    db.commit()

    # Create Buildings
    buildings = [
        Building(name="Main Library", code="MLIB", latitude=40.7128, longitude=-74.0060, description="Central campus library"),
        Building(name="Science Block A", code="SCIA", latitude=40.7130, longitude=-74.0065, description="Physics and Chemistry labs"),
        Building(name="Engineering Wing", code="ENGW", latitude=40.7125, longitude=-74.0050, description="Mechanical and CS dept"),
        Building(name="Student Center", code="STUC", latitude=40.7140, longitude=-74.0070, description="Food court and recreation"),
        Building(name="Hostel Block 1", code="HST1", latitude=40.7115, longitude=-74.0040, description="Boys hostel")
    ]
    db.add_all(buildings)
    db.commit()
    
    # Re-fetch users and buildings to use their IDs
    staff_users = db.query(User).filter(User.role == UserRole.STAFF).all()
    student_users = db.query(User).filter(User.role == UserRole.STUDENT).all()
    all_buildings = db.query(Building).all()

    # Create Complaints
    import random
    complaints = []
    
    categories = list(ComplaintCategory)
    waste_types = list(WasteType)
    
    for i in range(1, 11):
        reporter = random.choice(student_users)
        building = random.choice(all_buildings)
        
        c = Complaint(
            title=f"Sample Complaint {i}",
            description=f"This is a sample description for complaint {i}. It needs to be resolved quickly.",
            category=random.choice(categories),
            waste_type=random.choice(waste_types),
            priority=random.choice(list(Priority)),
            status=ComplaintStatus.PENDING,
            building_id=building.id,
            reported_by=reporter.id,
            floor=f"{random.randint(1, 5)}",
            room=f"Room {random.randint(100, 500)}"
        )
        complaints.append(c)

    db.add_all(complaints)
    db.commit()
    
    # Add History and assign some complaints
    for idx, c in enumerate(complaints):
        if idx % 2 == 0:
            assignee = random.choice(staff_users)
            c.status = ComplaintStatus.ASSIGNED
            c.assigned_to = assignee.id
            
            history = ComplaintHistory(
                complaint_id=c.id,
                old_status=ComplaintStatus.PENDING,
                new_status=ComplaintStatus.ASSIGNED,
                remarks="Assigned by admin",
                updated_by=admin.id
            )
            db.add(history)
            
        if idx % 4 == 0:
            c.status = ComplaintStatus.IN_PROGRESS
            history2 = ComplaintHistory(
                complaint_id=c.id,
                old_status=ComplaintStatus.ASSIGNED,
                new_status=ComplaintStatus.IN_PROGRESS,
                remarks="Staff started working",
                updated_by=c.assigned_to
            )
            db.add(history2)
            
    db.commit()
    print("Database seeded successfully with buildings, users, and complaints.")
    db.close()

if __name__ == "__main__":
    seed_db()
