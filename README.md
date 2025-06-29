# Rabbit-Celery-FastAPI Automation Workflow

A comprehensive CI/CD pipeline system designed for solopreneur development workflows, integrating RabbitMQ, Celery, and FastAPI for scalable task automation.

## Project Overview

This project implements a prompt-driven development methodology for building robust automation workflows. It combines message queuing (RabbitMQ), distributed task processing (Celery), and modern web APIs (FastAPI) to create a complete automation platform.

## Technology Stack

- **FastAPI**: Modern, fast web framework for building APIs
- **Celery**: Distributed task queue system
- **RabbitMQ**: Message broker for reliable communication
- **Docker**: Containerization for consistent development environments
- **Git**: Version control with structured commit workflow

## Development Workflow

This project follows a structured prompt-driven development approach:

1. **Setup Phase**: Initial project structure and environment configuration
2. **Discussion Phase**: Section-by-section implementation planning
3. **Implementation Phase**: Iterative development with testing
4. **Deployment Phase**: CI/CD pipeline automation

## Project Status

- [x] Initial project setup and documentation
- [ ] Core development environment (Docker, docker-compose)
- [ ] FastAPI application structure
- [ ] Celery worker configuration
- [ ] RabbitMQ integration
- [ ] CI/CD pipeline implementation
- [ ] Testing framework setup
- [ ] Production deployment configuration

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
# - RabbitMQ Management UI: http://localhost:15673
# - Celery Flower monitoring: http://localhost:5555
# - PostgreSQL: localhost:5432
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
