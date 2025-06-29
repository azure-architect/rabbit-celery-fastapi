# Rabbit-Celery-FastAPI Automation Workflow (PostgreSQL-Free)

A lightweight, containerized automation system designed for solopreneur development workflows, integrating RabbitMQ, Celery, and FastAPI for scalable task automation without database dependencies.

## Project Overview

This project implements a prompt-driven development methodology for building robust automation workflows. It combines message queuing (RabbitMQ), distributed task processing (Celery), and modern web APIs (FastAPI) to create a complete automation platform optimized for stateless operations.

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Celery**: Distributed task queue system
- **RabbitMQ**: Message broker for reliable communication
- **Redis**: Result backend for task status and caching
- **Docker**: Containerization for consistent development environments
- **Git**: Version control with structured commit workflow

## Perfect For

- **File processing automation** (CSV, JSON, XML parsing)
- **API integration workflows** (data sync, webhooks)
- **Report generation and delivery**
- **Scheduled maintenance tasks**
- **Microservice architectures** (where database is external)
- **Stateless automation workflows**
- **Data transformation pipelines**

## Development Workflow

This project follows a structured prompt-driven development approach:

1. **Setup Phase**: Initial project structure and environment configuration
2. **Discussion Phase**: Section-by-section implementation planning
3. **Implementation Phase**: Iterative development with testing
4. **Deployment Phase**: CI/CD pipeline automation

## Project Status

- [x] Initial project setup and documentation
- [x] Core development environment (Docker, docker-compose)
- [x] FastAPI application structure
- [x] Celery worker configuration
- [x] RabbitMQ integration
- [x] Redis result backend
- [x] Task management API endpoints
- [x] Monitoring with Flower
- [x] Production-ready containerization
- [x] Comprehensive error handling
- [ ] Custom task implementations (project-specific)

## Quick Start

```bash
# Clone the repository
git clone <repository-url>
cd rabbit-celery-fastapi

# Set up environment variables
cp .env.example .env

# Start the development environment
docker-compose up -d

# Access the services:
# - FastAPI application: http://localhost:8000
# - FastAPI docs: http://localhost:8000/docs
# - RabbitMQ Management UI: http://localhost:15673 (admin/devpassword123)
# - Celery Flower monitoring: http://localhost:5555
# - Redis: localhost:6379

# Run tests
pytest
```

## Documentation

- `prompt-workflow.md`: Developer prompt sequence guide
- `CD Pipeline for Solopreneur Development Workflow.md`: CI/CD pipeline specification
- `status.log`: Development progress tracking

## Contributing

This project follows a structured development workflow. Please refer to the prompt-workflow documentation for the proper development sequence.

## License

[License information to be added]
