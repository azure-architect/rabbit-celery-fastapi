"""
Example Celery tasks
"""
from celery import current_task
from app.celery_app import celery_app
import time
import logging

logger = logging.getLogger(__name__)


@celery_app.task(bind=True)
def example_long_task(self, duration: int = 10):
    """
    Example long-running task with progress updates
    """
    logger.info(f"Starting long task with duration: {duration} seconds")
    
    for i in range(duration):
        time.sleep(1)
        current_task.update_state(
            state="PROGRESS",
            meta={
                "current": i + 1, 
                "total": duration,
                "status": f"Processing step {i + 1} of {duration}"
            }
        )
        logger.info(f"Task progress: {i + 1}/{duration}")
    
    result = {"status": "completed", "result": f"Task completed in {duration} seconds"}
    logger.info(f"Task completed: {result}")
    return result


@celery_app.task
def simple_add_task(x: int, y: int):
    """Simple addition task for testing"""
    logger.info(f"Adding {x} + {y}")
    result = x + y
    logger.info(f"Addition result: {result}")
    return {"operation": "addition", "inputs": [x, y], "result": result}


@celery_app.task
def simple_multiply_task(x: int, y: int):
    """Simple multiplication task for testing"""
    logger.info(f"Multiplying {x} * {y}")
    result = x * y
    logger.info(f"Multiplication result: {result}")
    return {"operation": "multiplication", "inputs": [x, y], "result": result}


@celery_app.task(bind=True)
def send_email_task(self, to: str, subject: str, body: str):
    """Example email sending task"""
    logger.info(f"Sending email to: {to}")
    
    # Simulate email sending process
    self.update_state(
        state="PROGRESS",
        meta={"status": "Connecting to email server..."}
    )
    time.sleep(1)
    
    self.update_state(
        state="PROGRESS", 
        meta={"status": "Composing email..."}
    )
    time.sleep(1)
    
    self.update_state(
        state="PROGRESS",
        meta={"status": "Sending email..."}
    )
    time.sleep(1)
    
    result = {
        "status": "sent", 
        "to": to, 
        "subject": subject,
        "timestamp": time.time()
    }
    logger.info(f"Email sent successfully: {result}")
    return result


@celery_app.task(bind=True)
def process_data_task(self, data_list: list):
    """Example data processing task"""
    logger.info(f"Processing {len(data_list)} items")
    
    processed_items = []
    total_items = len(data_list)
    
    for i, item in enumerate(data_list):
        # Simulate processing time
        time.sleep(0.5)
        
        # Process the item (example: uppercase if string, square if number)
        if isinstance(item, str):
            processed_item = item.upper()
        elif isinstance(item, (int, float)):
            processed_item = item ** 2
        else:
            processed_item = str(item)
        
        processed_items.append(processed_item)
        
        # Update progress
        self.update_state(
            state="PROGRESS",
            meta={
                "current": i + 1,
                "total": total_items,
                "processed_items": processed_items,
                "status": f"Processed {i + 1} of {total_items} items"
            }
        )
    
    result = {
        "status": "completed",
        "original_count": total_items,
        "processed_items": processed_items
    }
    logger.info(f"Data processing completed: {result}")
    return result


@celery_app.task
def health_check_task():
    """Simple health check task"""
    logger.info("Running health check task")
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "worker_id": celery_app.control.inspect().active()
    }
