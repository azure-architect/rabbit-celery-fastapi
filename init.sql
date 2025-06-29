-- Initialize the database with basic setup
-- This file is automatically executed when the PostgreSQL container starts

-- Create database if it doesn't exist (handled by POSTGRES_DB env var)
-- CREATE DATABASE IF NOT EXISTS rabbit_celery_db;

-- Create application user if needed (optional, as main user is created via env vars)
-- CREATE USER app_user WITH PASSWORD 'app_password';
-- GRANT ALL PRIVILEGES ON DATABASE rabbit_celery_db TO app_user;

-- Enable extensions that might be useful
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create initial schema structure (basic example)
-- Note: In production, this would be handled by Alembic migrations

-- Example: Create a basic tasks table for demonstration
-- CREATE TABLE IF NOT EXISTS tasks (
--     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
--     name VARCHAR(255) NOT NULL,
--     status VARCHAR(50) DEFAULT 'pending',
--     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
--     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
-- );

-- Example: Create an index
-- CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);

-- Log initialization
SELECT 'Database initialized successfully' as status;
