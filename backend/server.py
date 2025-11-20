from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from supabase import create_client, Client
import os
import logging
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
import uuid
from datetime import datetime, timezone
from passlib.context import CryptContext

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Supabase connection
# Read Supabase credentials
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Supabase URL or Key missing! Check your .env file.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# FastAPI app
app = FastAPI()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Create the main app
app = FastAPI()
api_router = APIRouter(prefix="/api")
authorized_users = [
    'j06haniel@gmail.com',
    'snrathnadevi@gmail.com',
    'snrrohit7034@gmail.com',
    'suryarm.06@gmail.com',
    'shadeddak69@gmail.com',
    'meswaramuthu28@gmail.com',
    'jayaprasad133@gmail.com',
    'm.karthikeyan8124@gmail.com',
    'kirthika244@gmail.com',
    'prithiviraj.t.eee26@psvpec.in',
    'mohammedmuzzammil2004@gmail.com'
]

# Create a function to add users
def create_users():
    for email in authorized_users:
        try:
            user = supabase_admin.auth.admin.create_user(
                email=email,
                password="TempPass123!",  # temporary password
                email_confirm=True
            )
            print(f"Created user: {email}")
        except Exception as e:
            print(f"Error creating {email}: {e}")




# ========== MODELS ==========

class User(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    password: str
    name: str
    role: str
    email: Optional[str] = None
    contact: Optional[str] = None
    skillset: Optional[List[str]] = []
    current_tasks: Optional[List[str]] = []
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class UserResponse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str
    username: str
    name: str
    role: str
    email: Optional[str] = None
    contact: Optional[str] = None
    skillset: Optional[List[str]] = []
    current_tasks: Optional[List[str]] = []
    created_at: str

class UserCreate(BaseModel):
    username: str
    password: str
    name: str
    role: str
    email: Optional[str] = None
    contact: Optional[str] = None
    skillset: Optional[List[str]] = []

class UserUpdate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    email: Optional[str] = None
    contact: Optional[str] = None
    skillset: Optional[List[str]] = None
    current_tasks: Optional[List[str]] = None

class LoginRequest(BaseModel):
    email: str
    password: str

class Project(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    type: str
    assigned_members: List[str] = []
    deadline: Optional[str] = None
    status: str = "todo"
    progress: int = 0
    files: Optional[List[str]] = []
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    type: str
    assigned_members: List[str] = []
    deadline: Optional[str] = None

class Task(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    project_id: str
    title: str
    description: Optional[str] = None
    assigned_to: str
    status: str = "todo"
    priority: str = "medium"
    due_date: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class TaskCreate(BaseModel):
    project_id: str
    title: str
    description: Optional[str] = None
    assigned_to: str
    priority: str = "medium"
    due_date: Optional[str] = None

class CalendarEvent(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: Optional[str] = None
    start_time: str
    end_time: str
    participants: List[str] = []
    event_type: str = "meeting"
    google_event_id: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class CalendarEventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: str
    end_time: str
    participants: List[str] = []
    event_type: str = "meeting"

class LeaveRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    user_name: str
    type: str
    start_date: str
    end_date: str
    reason: str
    status: str = "pending"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class LeaveRequestCreate(BaseModel):
    user_id: str
    user_name: str
    type: str
    start_date: str
    end_date: str
    reason: str

class ContentItem(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    platform: str
    title: str
    caption: Optional[str] = None
    status: str = "draft"
    scheduled_date: Optional[str] = None
    creator: str
    content_url: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ContentItemCreate(BaseModel):
    platform: str
    title: str
    caption: Optional[str] = None
    scheduled_date: Optional[str] = None
    creator: str
    content_url: Optional[str] = None

class AIProject(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    dataset: Optional[str] = None
    model_version: Optional[str] = None
    accuracy: Optional[float] = None
    status: str = "in_progress"
    assigned_to: List[str] = []
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class AIProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    dataset: Optional[str] = None
    assigned_to: List[str] = []

class ResearchNote(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    content: str
    tags: List[str] = []
    author: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class ResearchNoteCreate(BaseModel):
    title: str
    content: str
    tags: List[str] = []
    author: str

class AcademyCourse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: Optional[str] = None
    instructor: Optional[str] = None
    students_count: int = 0
    status: str = "draft"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class AcademyCourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    instructor: Optional[str] = None

class PersonalTask(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: str
    category: str
    status: str = "todo"
    due_date: Optional[str] = None
    is_private: bool = True
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class PersonalTaskCreate(BaseModel):
    user_id: str
    title: str
    category: str
    due_date: Optional[str] = None
    is_private: bool = True

class CloudService(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    status: str
    uptime: Optional[str] = None
    environment: str
    last_deployment: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class CloudServiceCreate(BaseModel):
    name: str
    environment: str

class FinanceTransaction(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: str
    category: str
    amount: float
    description: str
    date: str
    payment_method: Optional[str] = None
    receipt_url: Optional[str] = None
    paid_to: Optional[str] = None
    status: str = "completed"
    created_by: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class FinanceTransactionCreate(BaseModel):
    type: str
    category: str
    amount: float
    description: str
    date: str
    payment_method: Optional[str] = None
    receipt_url: Optional[str] = None
    paid_to: Optional[str] = None
    status: str = "completed"
    created_by: str

class SalaryRecord(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    user_name: str
    month: str
    base_salary: float
    deductions: float = 0.0
    bonuses: float = 0.0
    net_salary: float
    status: str = "pending"
    payment_date: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class SalaryRecordCreate(BaseModel):
    user_id: str
    user_name: str
    month: str
    base_salary: float
    deductions: float = 0.0
    bonuses: float = 0.0

class AttendanceRecord(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    user_name: str
    date: str
    check_in: Optional[str] = None
    check_out: Optional[str] = None
    total_hours: Optional[float] = None
    status: str = "present"
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class AttendanceCheckIn(BaseModel):
    user_id: str
    user_name: str

class AttendanceCheckOut(BaseModel):
    user_id: str
    date: str

class KudosTransaction(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    user_name: str
    amount: int
    reason: str
    category: str
    given_by: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class KudosTransactionCreate(BaseModel):
    user_id: str
    user_name: str
    amount: int
    reason: str
    category: str
    given_by: str

class TrainingCourse(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: Optional[str] = None
    instructor: Optional[str] = None
    video_url: Optional[str] = None
    files: List[str] = []
    homework_tasks: List[str] = []
    kudos_reward: int = 0
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class TrainingCourseCreate(BaseModel):
    title: str
    description: Optional[str] = None
    instructor: Optional[str] = None
    video_url: Optional[str] = None
    homework_tasks: List[str] = []
    kudos_reward: int = 0

class TrainingProgress(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    course_id: str
    user_id: str
    user_name: str
    progress: int = 0
    completed: bool = False
    homework_submitted: bool = False
    homework_url: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class TrainingProgressUpdate(BaseModel):
    progress: int
    homework_submitted: Optional[bool] = None
    homework_url: Optional[str] = None

class Meeting(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    agenda: str
    start_time: str
    end_time: str
    organizer: str
    attendees: List[str] = []
    meeting_type: str = "team"
    attendance_tracked: bool = False
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class MeetingCreate(BaseModel):
    title: str
    agenda: str
    start_time: str
    end_time: str
    organizer: str
    attendees: List[str] = []
    meeting_type: str = "team"

class MeetingAttendance(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    meeting_id: str
    user_id: str
    user_name: str
    status: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class MeetingAttendanceCreate(BaseModel):
    meeting_id: str
    attendees_present: List[str]

class Subscription(BaseModel):
    model_config = ConfigDict(extra="ignore")
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    platform: str
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: bool = True
    renewal_date: Optional[str] = None
    notes: Optional[str] = None
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

class SubscriptionCreate(BaseModel):
    platform: str
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: bool = True
    renewal_date: Optional[str] = None
    notes: Optional[str] = None

# ========== AUTH ENDPOINTS ==========

# ========== AUTH ENDPOINTS (Revised) ==========

    @api_router.post("/auth/login")
    async def login(request: LoginRequest):
        try:
            # 1. Use Supabase Auth to securely verify credentials
            # This checks email/password against the protected 'auth.users' table
            auth_response = supabase.auth.sign_in_with_password(
                {
                    "email": request.email,
                    "password": request.password,
                }
            )

            if not auth_response.session:
                # If the sign-in failed (e.g., wrong password/email)
                raise HTTPException(status_code=401, detail="Invalid credentials - email or password incorrect.")
            
            user_id = auth_response.user.id
            access_token = auth_response.session.access_token
            
            # 2. Fetch the user's custom profile data from your 'users' table
            # The 'id' in your custom table should be the same as the 'auth.users' ID.
            # This fetches the rest of the profile data (name, role, skillset, etc.)
            response = supabase.table("users").select("*").eq("id", user_id).execute()
            
            if not response.data:
                raise HTTPException(status_code=404, detail="Authentication successful, but user profile not found.")

            user_profile = response.data[0]
            
            # 3. Return the profile and the secure token
            return {
                "user": user_profile, 
                "token": access_token
            }
            
        except Exception as e:
            # Catch common Supabase Auth errors and provide a generic 401 response for security
            error_detail = str(e)
            if "AuthApiError" in type(e).__name__ or "Invalid login credentials" in error_detail:
                raise HTTPException(status_code=401, detail="Invalid credentials - email or password incorrect.")
            
            logging.error(f"Login error: {error_detail}")
            raise HTTPException(status_code=500, detail="An unexpected server error occurred during login.")
        

    @api_router.post("/auth/register", response_model=UserResponse)
    async def register(user_data: UserCreate):
        try:
            # Check if username exists
            existing = supabase.table("users").select("*").eq("username", user_data.username).execute()
            if existing.data and len(existing.data) > 0:
                raise HTTPException(status_code=400, detail="Username already exists")
            
            # Hash password
            hashed_password = pwd_context.hash(user_data.password)
            user_dict = user_data.model_dump()
            user_dict["password"] = hashed_password
            
            user_obj = User(**user_dict)
            doc = user_obj.model_dump()
            
            response = supabase.table("users").insert(doc).execute()
            
            # Return without password
            response_dict = {k: v for k, v in response.data[0].items() if k != 'password'}
            return UserResponse(**response_dict)
        except Exception as e:
            logging.error(f"Register error: {e}")
            raise HTTPException(status_code=500, detail=str(e))

# ========== USER/TEAM MANAGEMENT ==========

@api_router.get("/users", response_model=List[UserResponse])
async def get_users():
    try:
        response = supabase.table("users").select("id, username, name, role, email, contact, skillset, current_tasks, created_at").execute()
        return response.data
    except Exception as e:
        logging.error(f"Get users error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    try:
        response = supabase.table("users").select("id, username, name, role, email, contact, skillset, current_tasks, created_at").eq("id", user_id).execute()
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return response.data[0]
    except Exception as e:
        logging.error(f"Get user error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/users/{user_id}")
async def update_user(user_id: str, user_data: UserUpdate):
    try:
        update_dict = {k: v for k, v in user_data.model_dump().items() if v is not None}
        if not update_dict:
            raise HTTPException(status_code=400, detail="No data to update")
        
        response = supabase.table("users").update(update_dict).eq("id", user_id).execute()
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        return {"message": "User updated successfully"}
    except Exception as e:
        logging.error(f"Update user error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.delete("/users/{user_id}")
async def delete_user(user_id: str):
    try:
        response = supabase.table("users").delete().eq("id", user_id).execute()
        if not response.data or len(response.data) == 0:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}
    except Exception as e:
        logging.error(f"Delete user error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== PROJECT MANAGEMENT ==========

@api_router.get("/projects")
async def get_projects():
    try:
        response = supabase.table("projects").select("*").execute()
        return response.data or []
    except Exception as e:
        logging.error(f"Get projects error: {e}")
        return []

@api_router.post("/projects")
async def create_project(project_data: ProjectCreate):
    try:
        project_obj = Project(**project_data.model_dump())
        doc = project_obj.model_dump()
        response = supabase.table("projects").insert(doc).execute()
        return response.data[0]
    except Exception as e:
        logging.error(f"Create project error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/projects/{project_id}")
async def update_project(project_id: str, update_data: dict):
    try:
        response = supabase.table("projects").update(update_data).eq("id", project_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Project not found")
        return {"message": "Project updated successfully"}
    except Exception as e:
        logging.error(f"Update project error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.delete("/projects/{project_id}")
async def delete_project(project_id: str):
    try:
        response = supabase.table("projects").delete().eq("id", project_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Project not found")
        return {"message": "Project deleted successfully"}
    except Exception as e:
        logging.error(f"Delete project error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== TASK MANAGEMENT ==========

@api_router.get("/tasks")
async def get_tasks(project_id: Optional[str] = None, user_id: Optional[str] = None):
    try:
        query = supabase.table("tasks").select("*")
        if project_id:
            query = query.eq("project_id", project_id)
        if user_id:
            query = query.eq("assigned_to", user_id)
        response = query.execute()
        return response.data or []
    except Exception as e:
        logging.error(f"Get tasks error: {e}")
        return []

@api_router.post("/tasks")
async def create_task(task_data: TaskCreate):
    try:
        task_obj = Task(**task_data.model_dump())
        doc = task_obj.model_dump()
        response = supabase.table("tasks").insert(doc).execute()
        return response.data[0]
    except Exception as e:
        logging.error(f"Create task error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/tasks/{task_id}")
async def update_task(task_id: str, update_data: dict):
    try:
        response = supabase.table("tasks").update(update_data).eq("id", task_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task updated successfully"}
    except Exception as e:
        logging.error(f"Update task error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.delete("/tasks/{task_id}")
async def delete_task(task_id: str):
    try:
        response = supabase.table("tasks").delete().eq("id", task_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task deleted successfully"}
    except Exception as e:
        logging.error(f"Delete task error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== CALENDAR MANAGEMENT ==========

@api_router.get("/calendar/events")
async def get_calendar_events():
    try:
        response = supabase.table("calendar_events").select("*").execute()
        return response.data or []
    except Exception as e:
        logging.error(f"Get calendar events error: {e}")
        return []

@api_router.post("/calendar/events")
async def create_calendar_event(event_data: CalendarEventCreate):
    try:
        event_obj = CalendarEvent(**event_data.model_dump())
        doc = event_obj.model_dump()
        response = supabase.table("calendar_events").insert(doc).execute()
        return response.data[0]
    except Exception as e:
        logging.error(f"Create calendar event error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/calendar/events/{event_id}")
async def update_calendar_event(event_id: str, update_data: dict):
    try:
        response = supabase.table("calendar_events").update(update_data).eq("id", event_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Event not found")
        return {"message": "Event updated successfully"}
    except Exception as e:
        logging.error(f"Update calendar event error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.delete("/calendar/events/{event_id}")
async def delete_calendar_event(event_id: str):
    try:
        response = supabase.table("calendar_events").delete().eq("id", event_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Event not found")
        return {"message": "Event deleted successfully"}
    except Exception as e:
        logging.error(f"Delete calendar event error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== LEAVE MANAGEMENT ==========

@api_router.get("/leave-requests")
async def get_leave_requests():
    try:
        response = supabase.table("leave_requests").select("*").execute()
        return response.data or []
    except Exception as e:
        logging.error(f"Get leave requests error: {e}")
        return []

@api_router.post("/leave-requests")
async def create_leave_request(request_data: LeaveRequestCreate):
    try:
        leave_obj = LeaveRequest(**request_data.model_dump())
        doc = leave_obj.model_dump()
        response = supabase.table("leave_requests").insert(doc).execute()
        return response.data[0]
    except Exception as e:
        logging.error(f"Create leave request error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/leave-requests/{request_id}")
async def update_leave_request(request_id: str, status: str):
    try:
        response = supabase.table("leave_requests").update({"status": status}).eq("id", request_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Leave request not found")
        return {"message": "Leave request updated successfully"}
    except Exception as e:
        logging.error(f"Update leave request error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== CONTENT STUDIO ==========

@api_router.get("/content")
async def get_content_items():
    try:
        response = supabase.table("content_items").select("*").execute()
        return response.data or []
    except Exception as e:
        logging.error(f"Get content items error: {e}")
        return []

@api_router.post("/content")
async def create_content_item(item_data: ContentItemCreate):
    try:
        content_obj = ContentItem(**item_data.model_dump())
        doc = content_obj.model_dump()
        response = supabase.table("content_items").insert(doc).execute()
        return response.data[0]
    except Exception as e:
        logging.error(f"Create content item error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/content/{item_id}")
async def update_content_item(item_id: str, update_data: dict):
    try:
        response = supabase.table("content_items").update(update_data).eq("id", item_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Content item not found")
        return {"message": "Content item updated successfully"}
    except Exception as e:
        logging.error(f"Update content item error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== AI DEVELOPMENT LAB ==========

@api_router.get("/ai-projects")
async def get_ai_projects():
    try:
        response = supabase.table("ai_projects").select("*").execute()
        return response.data or []
    except Exception as e:
        logging.error(f"Get AI projects error: {e}")
        return []

@api_router.post("/ai-projects")
async def create_ai_project(project_data: AIProjectCreate):
    try:
        ai_project_obj = AIProject(**project_data.model_dump())
        doc = ai_project_obj.model_dump()
        response = supabase.table("ai_projects").insert(doc).execute()
        return response.data[0]
    except Exception as e:
        logging.error(f"Create AI project error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/ai-projects/{project_id}")
async def update_ai_project(project_id: str, update_data: dict):
    try:
        response = supabase.table("ai_projects").update(update_data).eq("id", project_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="AI project not found")
        return {"message": "AI project updated successfully"}
    except Exception as e:
        logging.error(f"Update AI project error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== RESEARCH HUB ==========

@api_router.get("/research-notes")
async def get_research_notes():
    try:
        response = supabase.table("research_notes").select("*").execute()
        return response.data or []
    except Exception as e:
        logging.error(f"Get research notes error: {e}")
        return []

@api_router.post("/research-notes")
async def create_research_note(note_data: ResearchNoteCreate):
    try:
        note_obj = ResearchNote(**note_data.model_dump())
        doc = note_obj.model_dump()
        response = supabase.table("research_notes").insert(doc).execute()
        return response.data[0]
    except Exception as e:
        logging.error(f"Create research note error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.delete("/research-notes/{note_id}")
async def delete_research_note(note_id: str):
    try:
        response = supabase.table("research_notes").delete().eq("id", note_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Research note not found")
        return {"message": "Research note deleted successfully"}
    except Exception as e:
        logging.error(f"Delete research note error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== ACADEMY ZONE ==========

@api_router.get("/academy/courses")
async def get_academy_courses():
    try:
        response = supabase.table("academy_courses").select("*").execute()
        return response.data or []
    except Exception as e:
        logging.error(f"Get academy courses error: {e}")
        return []

@api_router.post("/academy/courses")
async def create_academy_course(course_data: AcademyCourseCreate):
    try:
        course_obj = AcademyCourse(**course_data.model_dump())
        doc = course_obj.model_dump()
        response = supabase.table("academy_courses").insert(doc).execute()
        return response.data[0]
    except Exception as e:
        logging.error(f"Create academy course error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/academy/courses/{course_id}")
async def update_academy_course(course_id: str, update_data: dict):
    try:
        response = supabase.table("academy_courses").update(update_data).eq("id", course_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Course not found")
        return {"message": "Course updated successfully"}
    except Exception as e:
        logging.error(f"Update academy course error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== PERSONAL PLANNER ==========

@api_router.get("/personal-tasks")
async def get_personal_tasks(user_id: str):
    try:
        response = supabase.table("personal_tasks").select("*").eq("user_id", user_id).execute()
        return response.data or []
    except Exception as e:
        logging.error(f"Get personal tasks error: {e}")
        return []

@api_router.post("/personal-tasks")
async def create_personal_task(task_data: PersonalTaskCreate):
    try:
        task_obj = PersonalTask(**task_data.model_dump())
        doc = task_obj.model_dump()
        response = supabase.table("personal_tasks").insert(doc).execute()
        return response.data[0]
    except Exception as e:
        logging.error(f"Create personal task error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/personal-tasks/{task_id}")
async def update_personal_task(task_id: str, update_data: dict):
    try:
        response = supabase.table("personal_tasks").update(update_data).eq("id", task_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Personal task not found")
        return {"message": "Personal task updated successfully"}
    except Exception as e:
        logging.error(f"Update personal task error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.delete("/personal-tasks/{task_id}")
async def delete_personal_task(task_id: str):
    try:
        response = supabase.table("personal_tasks").delete().eq("id", task_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Personal task not found")
        return {"message": "Personal task deleted successfully"}
    except Exception as e:
        logging.error(f"Delete personal task error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== CLOUD PANEL ==========

@api_router.get("/cloud-services")
async def get_cloud_services():
    try:
        response = supabase.table("cloud_services").select("*").execute()
        return response.data or []
    except Exception as e:
        logging.error(f"Get cloud services error: {e}")
        return []

@api_router.post("/cloud-services")
async def create_cloud_service(service_data: CloudServiceCreate):
    try:
        service_obj = CloudService(**service_data.model_dump())
        doc = service_obj.model_dump()
        response = supabase.table("cloud_services").insert(doc).execute()
        return response.data[0]
    except Exception as e:
        logging.error(f"Create cloud service error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/cloud-services/{service_id}")
async def update_cloud_service(service_id: str, update_data: dict):
    try:
        response = supabase.table("cloud_services").update(update_data).eq("id", service_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Cloud service not found")
        return {"message": "Cloud service updated successfully"}
    except Exception as e:
        logging.error(f"Update cloud service error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== DASHBOARD STATS ==========

@api_router.get("/dashboard/stats")
async def get_dashboard_stats(user_id: Optional[str] = None):
    try:
        stats = {}
        
        # Total counts
        stats["total_projects"] = len(supabase.table("projects").select("id", count="exact").execute().data)
        stats["total_tasks"] = len(supabase.table("tasks").select("id", count="exact").execute().data)
        stats["total_members"] = len(supabase.table("users").select("id", count="exact").execute().data)
        stats["pending_leaves"] = len(supabase.table("leave_requests").select("id").eq("status", "pending").execute().data)
        
        # User-specific stats
        if user_id:
            my_tasks_response = supabase.table("tasks").select("*").eq("assigned_to", user_id).neq("status", "done").execute()
            stats["my_tasks"] = len(my_tasks_response.data)
            
            my_tasks_completed_response = supabase.table("tasks").select("id").eq("assigned_to", user_id).eq("status", "done").execute()
            stats["my_tasks_completed"] = len(my_tasks_completed_response.data)
            
            my_projects_response = supabase.table("projects").select("*").contains("assigned_members", [user_id]).execute()
            stats["my_projects"] = len(my_projects_response.data)
            
            stats["assigned_tasks"] = my_tasks_response.data[:10]
            
            # Get kudos balance
            kudos_response = supabase.table("kudos_transactions").select("amount").eq("user_id", user_id).execute()
            total_kudos = sum(t["amount"] for t in kudos_response.data)
            stats["kudos_balance"] = total_kudos
            
            # Get upcoming meetings
            now = datetime.now(timezone.utc).isoformat()
            upcoming_meetings_response = supabase.table("meetings").select("*").gte("start_time", now).execute()
            # Filter meetings where user is organizer or attendee
            user_meetings = [m for m in upcoming_meetings_response.data if m.get("organizer") == user_id or user_id in m.get("attendees", [])]
            stats["upcoming_meetings"] = sorted(user_meetings, key=lambda x: x["start_time"])[:5]
        
        # Recent activity
        recent_projects = supabase.table("projects").select("*").order("created_at", desc=True).limit(5).execute().data
        recent_tasks = supabase.table("tasks").select("*").order("created_at", desc=True).limit(5).execute().data
        
        stats["recent_projects"] = recent_projects
        stats["recent_tasks"] = recent_tasks
        
        return stats
    except Exception as e:
        logging.error(f"Get dashboard stats error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== FINANCE MODULE ==========

@api_router.get("/finance/transactions")
async def get_finance_transactions():
    try:
        response = supabase.table("finance_transactions").select("*").order("created_at", desc=True).execute()
        return response.data or []
    except Exception as e:
        logging.error(f"Get finance transactions error: {e}")
        return []

@api_router.post("/finance/transactions")
async def create_finance_transaction(transaction_data: FinanceTransactionCreate):
    try:
        transaction_obj = FinanceTransaction(**transaction_data.model_dump())
        doc = transaction_obj.model_dump()
        response = supabase.table("finance_transactions").insert(doc).execute()
        return response.data[0]
    except Exception as e:
        logging.error(f"Create finance transaction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/finance/summary")
async def get_finance_summary():
    try:
        response = supabase.table("finance_transactions").select("*").execute()
        transactions = response.data or []
        
        total_income = sum(t["amount"] for t in transactions if t["type"] == "income")
        total_expenses = sum(t["amount"] for t in transactions if t["type"] == "expense")
        total_salary = sum(t["amount"] for t in transactions if t["type"] == "salary")
        
        categories = {}
        for t in transactions:
            if t["type"] == "expense":
                category = t["category"]
                categories[category] = categories.get(category, 0) + t["amount"]
        
        recent = sorted(transactions, key=lambda x: x.get("created_at", ""), reverse=True)[:10]
        
        pending_salaries_response = supabase.table("salary_records").select("id", count="exact").eq("status", "pending").execute()
        pending_salary_payments = len(pending_salaries_response.data or [])
        
        return {
            "total_income": total_income,
            "total_expenses": total_expenses,
            "total_salary": total_salary,
            "net_balance": total_income - total_expenses - total_salary,
            "expense_by_category": categories,
            "recent_transactions": recent,
            "pending_salary_payments": pending_salary_payments
        }
    except Exception as e:
        logging.error(f"Get finance summary error: {e}")
        return {
            "total_income": 0,
            "total_expenses": 0,
            "total_salary": 0,
            "net_balance": 0,
            "expense_by_category": {},
            "recent_transactions": [],
            "pending_salary_payments": 0
        }

@api_router.delete("/finance/transactions/{transaction_id}")
async def delete_transaction(transaction_id: str):
    try:
        response = supabase.table("finance_transactions").delete().eq("id", transaction_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return {"message": "Transaction deleted successfully"}
    except Exception as e:
        logging.error(f"Delete transaction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/finance/salaries")
async def get_salary_records():
    try:
        response = supabase.table("salary_records").select("*").order("created_at", desc=True).execute()
        return response.data or []
    except Exception as e:
        logging.error(f"Get salary records error: {e}")
        return []

@api_router.post("/finance/salaries")
async def create_salary_record(salary_data: SalaryRecordCreate):
    try:
        net_salary = salary_data.base_salary - salary_data.deductions + salary_data.bonuses
        salary_dict = salary_data.model_dump()
        salary_dict["net_salary"] = net_salary
        salary_obj = SalaryRecord(**salary_dict)
        doc = salary_obj.model_dump()
        response = supabase.table("salary_records").insert(doc).execute()
        return response.data[0]
    except Exception as e:
        logging.error(f"Create salary record error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/finance/salaries/{salary_id}")
async def update_salary_status(salary_id: str, status: str, payment_date: Optional[str] = None):
    try:
        update_data = {"status": status}
        if payment_date:
            update_data["payment_date"] = payment_date
        response = supabase.table("salary_records").update(update_data).eq("id", salary_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Salary record not found")
        return {"message": "Salary status updated successfully"}
    except Exception as e:
        logging.error(f"Update salary status error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== ATTENDANCE MODULE ==========

@api_router.post("/attendance/check-in")
async def check_in(data: AttendanceCheckIn):
    try:
        today = datetime.now(timezone.utc).date().isoformat()
        
        existing_response = supabase.table("attendance").select("*").eq("user_id", data.user_id).eq("date", today).execute()
        existing = existing_response.data[0] if existing_response.data else None
        
        if existing and existing.get("check_in"):
            raise HTTPException(status_code=400, detail="Already checked in today")
        
        check_in_time = datetime.now(timezone.utc).isoformat()
        
        if existing:
            supabase.table("attendance").update({"check_in": check_in_time}).eq("user_id", data.user_id).eq("date", today).execute()
        else:
            attendance_obj = AttendanceRecord(
                user_id=data.user_id,
                user_name=data.user_name,
                date=today,
                check_in=check_in_time,
                status="present"
            )
            doc = attendance_obj.model_dump()
            supabase.table("attendance").insert(doc).execute()
        
        return {"message": "Checked in successfully", "time": check_in_time}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Check-in error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/attendance/check-out")
async def check_out(data: AttendanceCheckOut):
    try:
        record_response = supabase.table("attendance").select("*").eq("user_id", data.user_id).eq("date", data.date).execute()
        if not record_response.data:
            raise HTTPException(status_code=404, detail="No check-in record found for today")
        
        record = record_response.data[0]
        if record.get("check_out"):
            raise HTTPException(status_code=400, detail="Already checked out")
        
        check_out_time = datetime.now(timezone.utc).isoformat()
        check_in_dt = datetime.fromisoformat(record["check_in"])
        check_out_dt = datetime.fromisoformat(check_out_time)
        total_hours = (check_out_dt - check_in_dt).total_seconds() / 3600
        
        supabase.table("attendance").update({
            "check_out": check_out_time,
            "total_hours": round(total_hours, 2)
        }).eq("user_id", data.user_id).eq("date", data.date).execute()
        
        return {"message": "Checked out successfully", "time": check_out_time, "total_hours": round(total_hours, 2)}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Check-out error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/attendance/records")
async def get_attendance_records(user_id: Optional[str] = None, month: Optional[str] = None):
    try:
        query = supabase.table("attendance").select("*")
        if user_id:
            query = query.eq("user_id", user_id)
        if month:
            query = query.ilike("date", f"{month}%")
        response = query.order("date", desc=True).execute()
        return response.data or []
    except Exception as e:
        logging.error(f"Get attendance records error: {e}")
        return []

@api_router.get("/attendance/summary")
async def get_attendance_summary(user_id: Optional[str] = None):
    try:
        query = supabase.table("attendance").select("*")
        if user_id:
            query = query.eq("user_id", user_id)
        response = query.execute()
        records = response.data or []
        
        total_days = len(records)
        present_days = len([r for r in records if r["status"] == "present"])
        absent_days = len([r for r in records if r["status"] == "absent"])
        leave_days = len([r for r in records if r["status"] == "leave"])
        total_hours = sum(r.get("total_hours", 0) for r in records if r.get("total_hours"))
        
        return {
            "total_days": total_days,
            "present_days": present_days,
            "absent_days": absent_days,
            "leave_days": leave_days,
            "total_hours_worked": round(total_hours, 2),
            "average_hours_per_day": round(total_hours / present_days, 2) if present_days > 0 else 0
        }
    except Exception as e:
        logging.error(f"Get attendance summary error: {e}")
        return {
            "total_days": 0,
            "present_days": 0,
            "absent_days": 0,
            "leave_days": 0,
            "total_hours_worked": 0,
            "average_hours_per_day": 0
        }

# ========== KUDOS SYSTEM ==========

@api_router.get("/kudos/transactions")
async def get_kudos_transactions(user_id: Optional[str] = None):
    try:
        query = supabase.table("kudos_transactions").select("*")
        if user_id:
            query = query.eq("user_id", user_id)
        response = query.order("created_at", desc=True).execute()
        return response.data or []
    except Exception as e:
        logging.error(f"Get kudos transactions error: {e}")
        return []

@api_router.post("/kudos/transactions")
async def create_kudos_transaction(kudos_data: KudosTransactionCreate):
    try:
        kudos_obj = KudosTransaction(**kudos_data.model_dump())
        doc = kudos_obj.model_dump()
        response = supabase.table("kudos_transactions").insert(doc).execute()
        return response.data[0]
    except Exception as e:
        logging.error(f"Create kudos transaction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/kudos/balance/{user_id}")
async def get_kudos_balance(user_id: str):
    try:
        response = supabase.table("kudos_transactions").select("*").eq("user_id", user_id).execute()
        transactions = response.data or []
        total_kudos = sum(t["amount"] for t in transactions)
        return {"user_id": user_id, "total_kudos": total_kudos, "transactions_count": len(transactions)}
    except Exception as e:
        logging.error(f"Get kudos balance error: {e}")
        return {"user_id": user_id, "total_kudos": 0, "transactions_count": 0}

# ========== TRAINING SECTION ==========

@api_router.get("/training/courses")
async def get_training_courses():
    try:
        response = supabase.table("training_courses").select("*").order("created_at", desc=True).execute()
        return response.data or []
    except Exception as e:
        logging.error(f"Get training courses error: {e}")
        return []

@api_router.post("/training/courses")
async def create_training_course(course_data: TrainingCourseCreate):
    try:
        course_obj = TrainingCourse(**course_data.model_dump())
        doc = course_obj.model_dump()
        response = supabase.table("training_courses").insert(doc).execute()
        return response.data[0]
    except Exception as e:
        logging.error(f"Create training course error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/training/courses/{course_id}")
async def update_training_course(course_id: str, update_data: dict):
    try:
        response = supabase.table("training_courses").update(update_data).eq("id", course_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Course not found")
        return {"message": "Course updated successfully"}
    except Exception as e:
        logging.error(f"Update training course error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/training/progress")
async def get_training_progress(user_id: Optional[str] = None, course_id: Optional[str] = None):
    try:
        query = supabase.table("training_progress").select("*")
        if user_id:
            query = query.eq("user_id", user_id)
        if course_id:
            query = query.eq("course_id", course_id)
        response = query.execute()
        return response.data or []
    except Exception as e:
        logging.error(f"Get training progress error: {e}")
        return []

@api_router.post("/training/progress")
async def enroll_training(user_id: str, user_name: str, course_id: str):
    try:
        existing_response = supabase.table("training_progress").select("*").eq("user_id", user_id).eq("course_id", course_id).execute()
        if existing_response.data:
            raise HTTPException(status_code=400, detail="Already enrolled in this course")
        
        progress_obj = TrainingProgress(user_id=user_id, user_name=user_name, course_id=course_id)
        doc = progress_obj.model_dump()
        response = supabase.table("training_progress").insert(doc).execute()
        return response.data[0]
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Enroll training error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/training/progress/{progress_id}")
async def update_training_progress(progress_id: str, update_data: TrainingProgressUpdate):
    try:
        update_dict = update_data.model_dump(exclude_none=True)
        
        if update_dict.get("homework_submitted"):
            progress_response = supabase.table("training_progress").select("*").eq("id", progress_id).execute()
            if progress_response.data:
                progress = progress_response.data[0]
                if not progress.get("completed"):
                    course_response = supabase.table("training_courses").select("*").eq("id", progress["course_id"]).execute()
                    if course_response.data:
                        course = course_response.data[0]
                        if course.get("kudos_reward", 0) > 0:
                            kudos_obj = KudosTransaction(
                                user_id=progress["user_id"],
                                user_name=progress["user_name"],
                                amount=course["kudos_reward"],
                                reason=f"Completed training: {course['title']}",
                                category="training_completion",
                                given_by="system"
                            )
                            supabase.table("kudos_transactions").insert(kudos_obj.model_dump()).execute()
                    update_dict["completed"] = True
        
        response = supabase.table("training_progress").update(update_dict).eq("id", progress_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Progress record not found")
        return {"message": "Progress updated successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Update training progress error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# ========== MEETINGS ==========

@api_router.get("/meetings")
async def get_meetings(user_id: Optional[str] = None, meeting_type: Optional[str] = None):
    try:
        response = supabase.table("meetings").select("*").order("start_time", desc=True).execute()
        meetings = response.data or []
        
        if user_id:
            meetings = [m for m in meetings if m.get("organizer") == user_id or user_id in m.get("attendees", [])]
        if meeting_type:
            meetings = [m for m in meetings if m.get("meeting_type") == meeting_type]
        
        return meetings
    except Exception as e:
        logging.error(f"Get meetings error: {e}")
        return []

@api_router.post("/meetings")
async def create_meeting(meeting_data: MeetingCreate):
    try:
        meeting_obj = Meeting(**meeting_data.model_dump())
        doc = meeting_obj.model_dump()
        response = supabase.table("meetings").insert(doc).execute()
        return response.data[0]
    except Exception as e:
        logging.error(f"Create meeting error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/meetings/{meeting_id}")
async def update_meeting(meeting_id: str, update_data: dict):
    try:
        response = supabase.table("meetings").update(update_data).eq("id", meeting_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Meeting not found")
        return {"message": "Meeting updated successfully"}
    except Exception as e:
        logging.error(f"Update meeting error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.post("/meetings/{meeting_id}/attendance")
async def record_meeting_attendance(meeting_id: str, attendance_data: MeetingAttendanceCreate):
    try:
        meeting_response = supabase.table("meetings").select("*").eq("id", meeting_id).execute()
        if not meeting_response.data:
            raise HTTPException(status_code=404, detail="Meeting not found")
        
        meeting = meeting_response.data[0]
        
        for attendee_id in meeting["attendees"]:
            user_response = supabase.table("users").select("*").eq("id", attendee_id).execute()
            if not user_response.data:
                continue
            
            user = user_response.data[0]
            status = "present" if attendee_id in attendance_data.attendees_present else "absent"
            
            attendance_obj = MeetingAttendance(
                meeting_id=meeting_id,
                user_id=attendee_id,
                user_name=user["name"],
                status=status
            )
            supabase.table("meeting_attendance").insert(attendance_obj.model_dump()).execute()
            
            if status == "absent":
                kudos_obj = KudosTransaction(
                    user_id=attendee_id,
                    user_name=user["name"],
                    amount=-5,
                    reason=f"Missed meeting: {meeting['title']}",
                    category="meeting_attendance",
                    given_by=meeting["organizer"]
                )
                supabase.table("kudos_transactions").insert(kudos_obj.model_dump()).execute()
        
        supabase.table("meetings").update({"attendance_tracked": True}).eq("id", meeting_id).execute()
        return {"message": "Attendance recorded successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Record meeting attendance error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/meetings/{meeting_id}/attendance")
async def get_meeting_attendance(meeting_id: str):
    try:
        response = supabase.table("meeting_attendance").select("*").eq("meeting_id", meeting_id).execute()
        return response.data or []
    except Exception as e:
        logging.error(f"Get meeting attendance error: {e}")
        return []

# ========== SUBSCRIPTIONS ==========

@api_router.get("/subscriptions")
async def get_subscriptions():
    try:
        response = supabase.table("subscriptions").select("*").order("platform", desc=False).execute()
        return response.data or []
    except Exception as e:
        logging.error(f"Get subscriptions error: {e}")
        return []

@api_router.post("/subscriptions")
async def create_subscription(subscription_data: SubscriptionCreate):
    try:
        subscription_obj = Subscription(**subscription_data.model_dump())
        doc = subscription_obj.model_dump()
        response = supabase.table("subscriptions").insert(doc).execute()
        return response.data[0]
    except Exception as e:
        logging.error(f"Create subscription error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.put("/subscriptions/{subscription_id}")
async def update_subscription(subscription_id: str, update_data: dict):
    try:
        response = supabase.table("subscriptions").update(update_data).eq("id", subscription_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Subscription not found")
        return {"message": "Subscription updated successfully"}
    except Exception as e:
        logging.error(f"Update subscription error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@api_router.delete("/subscriptions/{subscription_id}")
async def delete_subscription(subscription_id: str):
    try:
        response = supabase.table("subscriptions").delete().eq("id", subscription_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Subscription not found")
        return {"message": "Subscription deleted successfully"}
    except Exception as e:
        logging.error(f"Delete subscription error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Include router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.get("/")
async def root():
    return {
        "message": "SNR Team Dashboard API", 
        "version": "2.0.0",
        "database": "Supabase PostgreSQL",
        "status": "online",
        "features": [
            "Authentication (Login/Register)",
            "User Management",
            "Project Management",
            "Task Management",
            "Calendar Events",
            "Leave Management",
            "Content Studio",
            "AI Development Lab",
            "Research Hub",
            "Academy Zone",
            "Personal Planner",
            "Cloud Panel",
            "Finance (Transactions & Salaries)",
            "Attendance (Check-in/Check-out)",
            "Kudos System",
            "Training Section",
            "Meetings & Attendance",
            "Subscriptions",
            "Dashboard Stats"
        ],
        "endpoints": "/docs"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "database": "supabase",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
if __name__ == "__main__":
    create_users()