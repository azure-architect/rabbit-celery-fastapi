# PostgreSQL-Free Version

This branch does not include PostgreSQL database support.

If you need database functionality:
1. Switch to the main branch: `git checkout main`
2. Or add your preferred database service to docker-compose.yml

## Adding Database Support

To add database support to this template:

1. Add database service to docker-compose.yml
2. Add database dependencies to requirements.txt
3. Update environment variables in .env
4. Add database configuration to app/core/config.py

Example databases you can add:
- PostgreSQL
- MySQL  
- MongoDB
- SQLite (file-based)
