"""
Task management endpoints
"""
from typing import Any, Dict, List
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from app.celery_app import celery_app
from app.tasks.example_tasks import (
    example_long_task,
    simple_add_task,
    simple_multiply_task,
    send_email_task,
    process_data_task,
    health_check_task
)

router = APIRouter()


class TaskCreate(BaseModel):
    """Task creation model"""
    name: str
    description: str = ""
    priority: int = 1


class TaskResponse(BaseModel):
    """Task response model"""
    task_id: str
    task_name: str
    status: str
    result: Any = None


class MathOperation(BaseModel):
    """Math operation model"""
    x: int
    y: int


class EmailTask(BaseModel):
    """Email task model"""
    to: str
    subject: str
    body: str


class DataProcessing(BaseModel):
    """Data processing model"""
    data: List[Any]


@router.get("/")
async def list_tasks():
    """List all active tasks"""
    try:
        # Get active tasks from Celery
        inspect = celery_app.control.inspect()
        active_tasks = inspect.active()
        scheduled_tasks = inspect.scheduled()
        
        return {
            "active_tasks": active_tasks or {},
            "scheduled_tasks": scheduled_tasks or {},
            "message": "Task listing retrieved successfully"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve tasks: {str(e)}")


@router.get("/health")
async def task_health_check():
    """Run a health check task"""
    try:
        task = health_check_task.delay()
        return {
            "task_id": task.id,
            "task_name": "health_check_task",
            "status": "submitted",
            "message": "Health check task submitted"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to submit health check: {str(e)}")


@router.post("/math/add", response_model=TaskResponse)
async def create_add_task(operation: MathOperation):
    """Create an addition task"""
    try:
        task = simple_add_task.delay(operation.x, operation.y)
        return TaskResponse(
            task_id=task.id,
            task_name="simple_add_task",
            status="submitted"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create add task: {str(e)}")


@router.post("/math/multiply", response_model=TaskResponse)
async def create_multiply_task(operation: MathOperation):
    """Create a multiplication task"""
    try:
        task = simple_multiply_task.delay(operation.x, operation.y)
        return TaskResponse(
            task_id=task.id,
            task_name="simple_multiply_task", 
            status="submitted"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create multiply task: {str(e)}")


@router.post("/long-task", response_model=TaskResponse)
async def create_long_task(duration: int = 10):
    """Create a long-running task"""
    try:
        if duration > 300:  # Limit to 5 minutes
            raise HTTPException(status_code=400, detail="Duration cannot exceed 300 seconds")
        
        task = example_long_task.delay(duration)
        return TaskResponse(
            task_id=task.id,
            task_name="example_long_task",
            status="submitted"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create long task: {str(e)}")


@router.post("/email", response_model=TaskResponse)
async def create_email_task(email_data: EmailTask):
    """Create an email sending task"""
    try:
        task = send_email_task.delay(email_data.to, email_data.subject, email_data.body)
        return TaskResponse(
            task_id=task.id,
            task_name="send_email_task",
            status="submitted"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create email task: {str(e)}")


@router.post("/process-data", response_model=TaskResponse)
async def create_data_processing_task(data: DataProcessing):
    """Create a data processing task"""
    try:
        if len(data.data) > 100:  # Limit data size
            raise HTTPException(status_code=400, detail="Data list cannot exceed 100 items")
        
        task = process_data_task.delay(data.data)
        return TaskResponse(
            task_id=task.id,
            task_name="process_data_task",
            status="submitted"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create data processing task: {str(e)}")


@router.get("/{task_id}")
async def get_task_status(task_id: str):
    """Get task status and result"""
    try:
        task_result = celery_app.AsyncResult(task_id)
        
        if task_result.state == "PENDING":
            response = {
                "task_id": task_id,
                "status": "pending",
                "message": "Task is waiting to be processed"
            }
        elif task_result.state == "PROGRESS":
            response = {
                "task_id": task_id,
                "status": "in_progress",
                "progress": task_result.info
            }
        elif task_result.state == "SUCCESS":
            response = {
                "task_id": task_id,
                "status": "completed",
                "result": task_result.result
            }
        else:  # FAILURE
            response = {
                "task_id": task_id,
                "status": "failed",
                "error": str(task_result.info)
            }
        
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get task status: {str(e)}")


@router.delete("/{task_id}")
async def cancel_task(task_id: str):
    """Cancel a task"""
    try:
        celery_app.control.revoke(task_id, terminate=True)
        return {
            "task_id": task_id,
            "status": "cancelled",
            "message": "Task cancellation requested"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to cancel task: {str(e)}")
