-- SNR Team Dashboard - Supabase Database Schema
-- Run this script in your Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users Table
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    name TEXT NOT NULL,
    role TEXT NOT NULL,
    email TEXT,
    contact TEXT,
    skillset TEXT[] DEFAULT '{}',
    current_tasks TEXT[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Projects Table
CREATE TABLE IF NOT EXISTS projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    type TEXT NOT NULL,
    assigned_members TEXT[] DEFAULT '{}',
    deadline TEXT,
    status TEXT DEFAULT 'todo',
    progress INTEGER DEFAULT 0,
    files TEXT[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Tasks Table
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    assigned_to TEXT NOT NULL,
    status TEXT DEFAULT 'todo',
    priority TEXT DEFAULT 'medium',
    due_date TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Calendar Events Table
CREATE TABLE IF NOT EXISTS calendar_events (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    event_type TEXT NOT NULL,
    attendees TEXT[] DEFAULT '{}',
    google_event_id TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Leave Requests Table
CREATE TABLE IF NOT EXISTS leave_requests (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    user_name TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT NOT NULL,
    reason TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    delegate_to TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Content Items Table
CREATE TABLE IF NOT EXISTS content_items (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    platform TEXT NOT NULL,
    content_type TEXT NOT NULL,
    assigned_editor TEXT,
    scheduled_date TEXT,
    status TEXT DEFAULT 'draft',
    draft_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- AI Projects Table
CREATE TABLE IF NOT EXISTS ai_projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    dataset TEXT,
    model_version TEXT,
    accuracy FLOAT,
    status TEXT DEFAULT 'development',
    assigned_engineers TEXT[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Research Notes Table
CREATE TABLE IF NOT EXISTS research_notes (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    tags TEXT[] DEFAULT '{}',
    author TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Academy Courses Table
CREATE TABLE IF NOT EXISTS academy_courses (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    instructor TEXT,
    students_count INTEGER DEFAULT 0,
    status TEXT DEFAULT 'draft',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Personal Tasks Table
CREATE TABLE IF NOT EXISTS personal_tasks (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    category TEXT NOT NULL,
    status TEXT DEFAULT 'todo',
    due_date TEXT,
    is_private BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Cloud Services Table
CREATE TABLE IF NOT EXISTS cloud_services (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    status TEXT NOT NULL,
    uptime TEXT,
    environment TEXT NOT NULL,
    last_deployment TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Finance Transactions Table
CREATE TABLE IF NOT EXISTS finance_transactions (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,
    category TEXT NOT NULL,
    amount FLOAT NOT NULL,
    description TEXT NOT NULL,
    date TEXT NOT NULL,
    payment_method TEXT,
    receipt_url TEXT,
    paid_to TEXT,
    status TEXT DEFAULT 'completed',
    created_by TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Salary Records Table
CREATE TABLE IF NOT EXISTS salary_records (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    user_name TEXT NOT NULL,
    month TEXT NOT NULL,
    base_salary FLOAT NOT NULL,
    deductions FLOAT DEFAULT 0.0,
    bonuses FLOAT DEFAULT 0.0,
    net_salary FLOAT NOT NULL,
    status TEXT DEFAULT 'pending',
    payment_date TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Attendance Records Table
CREATE TABLE IF NOT EXISTS attendance (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    user_name TEXT NOT NULL,
    date TEXT NOT NULL,
    check_in TEXT,
    check_out TEXT,
    total_hours FLOAT,
    status TEXT DEFAULT 'present',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, date)
);

-- Kudos Transactions Table
CREATE TABLE IF NOT EXISTS kudos_transactions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    user_name TEXT NOT NULL,
    amount INTEGER NOT NULL,
    reason TEXT NOT NULL,
    category TEXT NOT NULL,
    given_by TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Training Courses Table
CREATE TABLE IF NOT EXISTS training_courses (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    instructor TEXT,
    video_url TEXT,
    files TEXT[] DEFAULT '{}',
    homework_tasks TEXT[] DEFAULT '{}',
    kudos_reward INTEGER DEFAULT 0,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Training Progress Table
CREATE TABLE IF NOT EXISTS training_progress (
    id TEXT PRIMARY KEY,
    course_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    user_name TEXT NOT NULL,
    progress INTEGER DEFAULT 0,
    completed BOOLEAN DEFAULT FALSE,
    homework_submitted BOOLEAN DEFAULT FALSE,
    homework_url TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(course_id, user_id)
);

-- Meetings Table
CREATE TABLE IF NOT EXISTS meetings (
    id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    agenda TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL,
    organizer TEXT NOT NULL,
    attendees TEXT[] DEFAULT '{}',
    meeting_type TEXT DEFAULT 'team',
    attendance_tracked BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Meeting Attendance Table
CREATE TABLE IF NOT EXISTS meeting_attendance (
    id TEXT PRIMARY KEY,
    meeting_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    user_name TEXT NOT NULL,
    status TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Subscriptions Table
CREATE TABLE IF NOT EXISTS subscriptions (
    id TEXT PRIMARY KEY,
    platform TEXT NOT NULL,
    username TEXT,
    password TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    renewal_date TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_tasks_assigned_to ON tasks(assigned_to);
CREATE INDEX IF NOT EXISTS idx_tasks_project_id ON tasks(project_id);
CREATE INDEX IF NOT EXISTS idx_leave_requests_user_id ON leave_requests(user_id);
CREATE INDEX IF NOT EXISTS idx_attendance_user_id ON attendance(user_id);
CREATE INDEX IF NOT EXISTS idx_kudos_user_id ON kudos_transactions(user_id);
CREATE INDEX IF NOT EXISTS idx_training_progress_user_id ON training_progress(user_id);
CREATE INDEX IF NOT EXISTS idx_meetings_organizer ON meetings(organizer);

-- Enable Row Level Security (RLS) - Optional but recommended
-- You can enable this later based on your security requirements
-- ALTER TABLE users ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
-- etc.

-- Success message
SELECT 'Database schema created successfully!' as message;
