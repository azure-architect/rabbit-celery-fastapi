Project Plan: Automated Email Data Extraction and Ingestion System
1. Introduction
This document outlines the project plan for developing an automated system designed to extract financial data from incoming Gmail emails. The system will handle various email formats, including CSV attachments and HTML tables within the email body, and ingest this data into a PostgreSQL database. This plan prioritizes rapid, in-house deployment for a sole developer, while emphasizing robustness, dynamic configuration, and a clear path for future expansion into a broader personal automation hub.
2. Goals and Objectives
The primary goal of this project is to automate the process of extracting critical financial data from Gmail and storing it in a structured database for analysis and reporting. Beyond this, the architecture is designed to serve as a foundation for managing diverse personal automation tasks.
Key Objectives:
Automated Email Access: Programmatically open and maintain access to Gmail accounts using secure OAuth 2.0, with token management handled robustly in the database.
Dynamic Data Extraction: Extract data from emails based on their subject line, supporting both CSV attachments and HTML tables in the email body.
Structured Data Storage: Ingest extracted data into specific, dynamically created tables within a dedicated financial schema in a PostgreSQL database.
Robustness: Implement retry mechanisms for failures, respect API rate limits, and maintain processing state to prevent data loss or duplication.
Centralized Task Management: Provide a unified dashboard (Celery Flower) for monitoring all automated tasks, including email processing, web scraping, and other classification tasks.
Configurability: Allow easy addition, modification, or removal of data extraction/processing rules based on email subjects or other criteria via external configuration files, without modifying core code.
Scalable Foundation: Establish an architecture that can easily scale to handle increasing volumes of emails and diverse automation tasks (e.g., multiple email accounts, web scraping).
3. Scope
3.1. In-Scope
Gmail API integration for email fetching (metadata) and full message/attachment download.
OAuth 2.0 authentication with refresh token management for Gmail, with tokens stored securely in PostgreSQL.
Extraction of metadata (sender, recipient, subject, date) for all processed emails.
Parsing and ingestion of data from CSV attachments.
Parsing and ingestion of data from HTML tables embedded in email bodies.
Dynamic table creation in PostgreSQL based on extracted data schema.
PostgreSQL database interaction for data storage and state management.
Implementation of a subject-based rule engine for dynamic data processing.
Error handling, logging, and retry mechanisms for failed operations.
Rate limit adherence for Gmail API calls.
Containerization using Docker and orchestration with Docker Compose for local and initial production deployment.
Integration of RabbitMQ as a message broker and Celery for distributed task processing.
Deployment of Celery Flower for centralized task monitoring.
Integration of Celery Beat for scheduled task execution.
Guidance for deployment in a dedicated LXC container (running Docker).
Allocation strategy for data dumps and logs.
Design for extensibility to other email accounts (e.g., IMAP) and web scraping tasks via the Celery framework.
3.2. Out-of-Scope
User interface for system management or data visualization (beyond Celery Flower).
Advanced data validation beyond basic type inference.
Complex Natural Language Processing (NLP) for unstructured email body content (only HTML tables are targeted for extraction).
Direct IMAP client implementation (design for future integration is in scope).
Direct web scraping implementation (design for future integration is in scope).
Real-time data streaming (system operates on a scheduled basis).
Detailed reporting or analytics functionalities within the system itself.
Full Kubernetes deployment (considered a future enhancement).
n8n workflow development (mentioned as a potential integration point, but not core to this project's scope).
4. Key Features
Scheduled Email Fetching (Celery Beat): Automatically triggers email fetching and processing tasks on a defined schedule (e.g., every 45 minutes).
OAuth State Persistence (Database-backed): Securely manages and refreshes Gmail OAuth tokens by storing them in the PostgreSQL database.
Centralized Task Monitoring (Celery Flower): Provides a web dashboard to monitor the status, performance, and history of all automated tasks.
Intelligent Email Classification: Identifies email types (CSV attachment vs. HTML body table) based on configurable subject patterns.
CSV Attachment Processing: Downloads, parses, and imports data from CSV files into PostgreSQL.
HTML Table Extraction: Extracts and parses data from HTML tables within email bodies into PostgreSQL.
Dynamic Schema & Table Creation: Automatically creates new tables in the financial schema if a unique subject-based data structure is encountered.
Financial Schema Integration: All extracted financial data is routed to a dedicated financial schema in the database.
Idempotent Processing: Prevents reprocessing of already ingested emails/attachments.
Configurable Rules: External YAML/JSON file for defining subject-to-processing rules, including task names and parameters, enabling dynamic behavior without code changes.
Robust Error Handling: Implements exponential backoff for API errors and Celery task retries for failed data processing.
Status Tracking: Maintains a processed_status (0: unprocessed, 1: processed, 2: failed) for each email in the database.
Scalable Deployment: Utilizes a message queue and distributed workers for parallel processing, easily extensible to handle multiple email accounts and other automation tasks.
5. Architecture Design
The system is designed with a microservices-oriented approach, leveraging Docker for containerization and a message queue for decoupling, providing a robust and extensible foundation.
5.1. High-Level Architecture (Enhanced for Broader Automation)
graph TD
    A[Scheduler: Celery Beat] --> B(Producer - App Container);
    B -- Email ID Task --> C(Message Queue - RabbitMQ);
    C -- Task --> D[Data Processor/Consumer - Worker Container(s)];
    D -- Fetch Full Email & Ingest Data --> E[PostgreSQL Database - DB Container];
    E -- Stores State/Metadata & Rules --> B;
    F[Configuration File: rules.yaml] -- Loaded By --> B & D;
    D -- Dynamic Table Creation --> E;
    D -- Updates Processed Status --> E;
    C -- Monitoring --> G[Celery Flower Dashboard];


5.2. Component Breakdown
Producer (app container):
Purpose: Connects to Gmail, fetches only new email IDs and basic metadata, identifies unprocessed emails, and dispatches these email IDs as processing tasks to the message queue. This container also handles the OAuth state management.
Technologies: Python, google-api-python-client, psycopg2 / SQLAlchemy.
Logic:
Authenticates with Gmail and manages OAuth token state by loading/saving tokens from/to PostgreSQL.
Queries Gmail for new message IDs using historyId for incremental updates.
For each new email_id:
Checks the public.email_metadata table to see if the email_id exists and its processed_status (0: unprocessed, 1: processed, 2: failed).
If the email is unprocessed (status 0) or failed (status 2 from a previous attempt), it pushes the email_id to the message queue.
Inserts or updates the email_metadata table with processed_status = 0 (unprocessed) for newly discovered emails.
Updates public.system_state table with the latest historyId.
Handles Gmail API rate limits with exponential backoff.
Note: The schedule library is no longer needed here, as Celery Beat will trigger the main email fetching task.
Message Queue (broker container - RabbitMQ):
Purpose: Provides asynchronous communication between the producer and consumers. Decouples task dispatching from execution.
Technologies: RabbitMQ.
Data Processor/Consumer (worker container(s) - Celery):
Purpose: Consumes email IDs (and other task parameters) from the message queue. For email tasks, it fetches the full email content, performs data extraction (CSV parsing, HTML table parsing), dynamically creates database tables, and ingests data. These workers are generic and can be extended to handle other automation tasks (web scraping, IMAP processing) by defining new Celery tasks.
Technologies: Python, Celery, google-api-python-client, pandas, BeautifulSoup4, psycopg2 / SQLAlchemy, re, PyYAML (for config).
Logic:
Listens for tasks from the message queue.
Loads rules.yaml: Each worker instance will load the configuration file to interpret task parameters and processing rules.
Upon receiving an email_id task:
Fetches the full email content (including HTML body and attachment details) from Gmail API using the email_id.
Extracts email metadata (subject, sender, etc.).
Classifies Email (Worker-side): Uses the email subject and the loaded rules.yaml to determine the type of data and the rule_details for processing.
Data Extraction & Ingestion:
If type is csv_attachment: Downloads the CSV attachment, uses pandas.read_csv to parse.
If type is html_body_table: Extracts HTML body, uses BeautifulSoup4 and pandas.read_html to extract tables. Selects the correct table based on table_index from rule_details.
Dynamic Table Creation: Connects to PostgreSQL. Based on rule_details['target_table_prefix'] and potentially dynamic parts from the subject (e.g., date), constructs a table name (e.g., financial.monthly_report_2025_06_28). It then dynamically creates the table in the financial schema if it doesn't exist, inferring column types from the DataFrame.
Data Ingestion: Uses pandas.DataFrame.to_sql() for efficient bulk insertion into the newly created or existing table in the financial schema.
Updates public.email_metadata: Sets processed_status = 1 (processed) and processed_at timestamp. Also updates has_csv_attachment, has_html_table, extracted_table_name, and classification based on the processing outcome.
Error Handling: If any step fails (Gmail API call, parsing, DB insertion), the worker catches the exception, updates public.email_metadata to processed_status = 2 (failed), and triggers Celery's retry mechanism with exponential backoff.
Celery Beat (celery_beat container):
Purpose: The scheduler for Celery tasks. It reads scheduled tasks from the Celery configuration (which can be defined in Python code or loaded from a file) and periodically adds them to the message queue for workers to execute. This replaces the schedule library in the producer for scheduled tasks.
Technologies: Celery Beat.
Features: Handles periodic tasks (e.g., "run fetch_new_emails_task every 45 minutes"). Ensures tasks are reliably scheduled even if the producer container restarts.
Celery Flower (flower container):
Purpose: Provides a real-time web-based monitoring and administration tool for Celery tasks and workers.
Technologies: Celery Flower.
Features: View task progress, history, worker status, task details, and even revoke or terminate tasks.
PostgreSQL Database (db container):
Purpose: Persistent storage for email metadata, processing state, and all extracted financial data.
Technologies: PostgreSQL.
Schemas:
public: Default schema (used for system-level tables like email_metadata, system_state, and oauth_tokens).
financial: Dedicated schema for all extracted financial data tables.
Tables:
public.email_metadata: Stores message_id, thread_id, from_email, to_email, subject, date, has_csv_attachment, has_html_table, processed_status (0: unprocessed, 1: processed, 2: failed), processed_at, attachment_filename, extracted_table_name, classification.
public.system_state: Stores last_history_id for incremental Gmail API fetches.
public.oauth_tokens: Stores Gmail OAuth tokens securely.
CREATE TABLE public.oauth_tokens (
    account_id VARCHAR(255) PRIMARY KEY, -- Unique identifier for the Gmail account (e.g., email address)
    access_token TEXT NOT NULL,
    refresh_token TEXT, -- Crucial for long-term access
    token_uri TEXT,
    client_id TEXT,
    client_secret TEXT,
    scopes TEXT, -- Store scopes as a comma-separated string or JSON array
    token_expiry TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


financial.your_dynamic_table_name_1: For CSV data (e.g., financial.monthly_report_2025_06_28).
financial.your_dynamic_table_name_2: For HTML table data (e.g., financial.daily_sales_summary_2025_06_28).
6. Technology Stack
Programming Language: Python 3.x
Email API: Google Gmail API
OAuth Library: google-auth-oauthlib, google-api-python-client
Scheduler: Celery Beat
Message Queue: RabbitMQ
Task Queue: Celery
Task Monitoring: Celery Flower
HTML Parsing: BeautifulSoup4
Data Manipulation: pandas
Database: PostgreSQL
Database ORM/Client: psycopg2, SQLAlchemy
Configuration: YAML (PyYAML)
Containerization: Docker
Orchestration (Dev/Test/Initial Prod): Docker Compose
7. Data Models (PostgreSQL)
7.1. public.email_metadata Table
CREATE TABLE public.email_metadata (
    message_id VARCHAR(255) PRIMARY KEY,
    thread_id VARCHAR(255),
    from_email TEXT,
    to_email TEXT,
    subject TEXT,
    date TIMESTAMP WITH TIME ZONE,
    has_csv_attachment BOOLEAN DEFAULT FALSE,
    has_html_table BOOLEAN DEFAULT FALSE,
    processed_status SMALLINT DEFAULT 0, -- 0: unprocessed, 1: processed, 2: failed
    processed_at TIMESTAMP WITH TIME ZONE,
    attachment_filename TEXT, -- For CSVs
    extracted_table_name VARCHAR(255), -- Name of the financial table where data was inserted
    classification VARCHAR(100) -- e.g., 'Financial_Report', 'Sales_Data', 'Transaction_Data', 'Unclassified'
);


7.2. public.system_state Table
CREATE TABLE public.system_state (
    key VARCHAR(100) PRIMARY KEY,
    value TEXT
);
-- Example entry: INSERT INTO public.system_state (key, value) VALUES ('last_history_id', '1234567890');


7.3. public.oauth_tokens Table
CREATE TABLE public.oauth_tokens (
    account_id VARCHAR(255) PRIMARY KEY, -- Unique identifier for the Gmail account (e.g., email address)
    access_token TEXT NOT NULL,
    refresh_token TEXT, -- Crucial for long-term access
    token_uri TEXT,
    client_id TEXT,
    client_secret TEXT,
    scopes TEXT, -- Store scopes as a comma-separated string or JSON array
    token_expiry TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


7.4. financial Schema and Dynamic Tables
All extracted financial data will reside in the financial schema. Tables within this schema will be created dynamically based on the email subject and the configured rules.
Example Dynamic Table (e.g., financial.monthly_report_2025_06_28):
-- Columns will be inferred from the CSV/HTML table headers and data types
CREATE TABLE financial.monthly_report_2025_06_28 (
    id SERIAL PRIMARY KEY, -- Auto-incrementing ID
    column_name_from_csv_1 TEXT,
    column_name_from_csv_2 NUMERIC,
    ...
    email_message_id VARCHAR(255) REFERENCES public.email_metadata(message_id), -- Link back to source email
    ingestion_timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);


8. Configuration Management
A rules.yaml file will define how different email subjects are processed, including which Celery task to invoke and what parameters to pass.
# rules.yaml
rules:
  - subject_pattern: "^Monthly Financial Report - (\\d{4}-\\d{2}-\\d{2})$" # Regex to capture date
    task_name: "email_tasks.process_csv_email" # Specific Celery task for CSV
    task_params:
      type: "csv_attachment"
      target_table_prefix: "monthly_report_"
      date_group_index: 1 # Index of the regex group containing the date for table naming
      classification: "Financial_Report"
    notes: "Processes monthly financial reports with CSV attachments. Creates a table like 'monthly_report_YYYY_MM_DD'."

  - subject_pattern: "^Daily Sales Summary for (.+)$" # Regex to capture region/date
    task_name: "email_tasks.process_html_table_email" # Specific Celery task for HTML
    task_params:
      type: "html_body_table"
      target_table_prefix: "daily_sales_summary_"
      table_index: 0 # Index of the HTML table to extract (0-indexed)
      classification: "Sales_Data"
    notes: "Extracts data from the first HTML table in daily sales summary emails. Table name based on subject."

  - subject_pattern: "^Transaction Data from (.+) - (\\d{4}-\\d{2}-\\d{2})$"
    task_name: "email_tasks.process_html_table_email"
    task_params:
      type: "html_body_table"
      target_table_prefix: "transactions_"
      table_index: 1 # Second HTML table
      classification: "Transaction_Data"
    notes: "Extracts data from the second HTML table in transaction emails. Table name includes entity and date."

  # Example for a future web scraping task
  - subject_pattern: "N/A" # This rule wouldn't be triggered by email subject
    trigger_type: "web_scrape_schedule" # Could be triggered by a separate scheduler in 'app'
    task_name: "web_tasks.scrape_financial_news"
    task_params:
      url: "https://example.com/financial_news"
      css_selector: ".article-headline"
      target_table: "financial.news_headlines"
      classification: "News_Data"
    notes: "Scrapes financial news headlines from a website."

  - subject_pattern: ".*" # Catch-all for any other email subject
    task_name: "email_tasks.process_metadata_only"
    task_params:
      classification: "Unclassified"
    notes: "Only stores email metadata for unclassified subjects."


Adding/Subtracting Configurations:
To add a new rule: Simply append a new entry to the rules list in rules.yaml. This can be for a new email subject, a new email account type (e.g., IMAP), or an entirely different automation task (e.g., web scraping).
To modify a rule: Edit the corresponding entry in rules.yaml.
To subtract a rule: Remove the corresponding entry from rules.yaml.
After any change to rules.yaml, the app container (producer) and worker containers need to be restarted to load the new configuration. In a Docker Compose setup, this means docker-compose restart app worker.
9. Scalability Considerations
Decoupling with Message Queue: The producer (fetching email IDs and dispatching tasks) is completely decoupled from the consumers (workers processing full emails/web scrapes). This ensures that fetching/dispatching is not blocked by heavy processing tasks.
Horizontal Scaling of Workers: The worker containers are stateless and designed for parallel processing. You can easily scale the number of worker replicas up or down based on the processing load across all your automation tasks. In Docker Compose, this is docker-compose up --scale worker=N. In Kubernetes, this is handled by increasing the replica count in the worker-deployment or by using a Horizontal Pod Autoscaler (HPA) based on CPU usage or queue length.
Database Scaling: PostgreSQL can be scaled vertically (more resources) or horizontally (read replicas, sharding) if the data volume becomes extremely large. This project assumes a single PostgreSQL instance initially.
Gmail API Rate Limits: The producer will implement exponential backoff and potentially batching (messages.batchGet) to stay within Gmail API quotas. Full email fetches are distributed among workers, which helps manage per-user rate limits more effectively.
10. Error Handling and Resilience
Retry Mechanisms:
Gmail API: Exponential backoff for rateLimitExceeded and other transient API errors.
Celery Tasks: Configured with max_retries and retry_backoff for database connection issues, parsing errors, or other processing failures. Failed tasks will be retried automatically by Celery.
Idempotency: Processing logic is designed to be idempotent where possible (e.g., updating a status flag, inserting data with unique constraints) to prevent issues if a task is processed multiple times due to retries.
Status Tracking: The processed_status in email_metadata (0: unprocessed, 1: processed, 2: failed) is critical for identifying and re-attempting failed processing tasks on subsequent runs.
State Persistence: last_history_id and email_metadata status flags are stored in PostgreSQL to ensure that processing resumes correctly after any system restart or failure.
Dead-Letter Queue (DLQ): Celery/RabbitMQ can be configured with a DLQ where tasks that have exhausted all retries are sent for manual inspection and debugging.
11. Deployment Strategy
The system will be deployed using Docker for containerization, with an alternative for direct LXC deployment.
Development & Testing: docker-compose will be used to spin up the app, worker, broker, flower, and db containers locally, providing a consistent development environment.
Initial Production Deployment (Docker Compose): The same docker-compose.yml can be used on a dedicated "Docker server" (which could be a VM or an LXC container configured to run Docker directly on Proxmox, avoiding nesting Docker within another LXC for the application itself).
Data Dumps & Logs (using Bind Mounts):
Data Dumps (PostgreSQL Backups): Use pg_dump command-line utility. Schedule via cron (on the Docker host for docker exec commands) or a dedicated backup container in Docker Compose. Output backup files to a bind-mounted directory or a named volume, ensuring persistence outside the container for easy access and off-site backup.
Example docker-compose.yml volume setup: - ./backups:/backups
Logs: Configure Python applications (producer and workers) to log to stdout/stderr. Docker will capture these logs (docker-compose logs -f <service_name>). For persistence, you can configure Docker's logging drivers to write to a file system or an external logging service. Alternatively, have your application write logs directly to a bind-mounted directory.
Example docker-compose.yml volume setup: - ./logs:/app/logs (if your app is configured to write to /app/logs)
rsync for Environment Synchronization and Backup Transfer:
rsync is an excellent tool for synchronizing your project directory (excluding sensitive files like .env and credentials.json from the Git repo) between your local workstation and the remote server.
It can also be used to transfer the generated database backup files (.sql) and application log files from the remote server's bind-mounted directories to a central backup location or your local machine.
Example rsync command for deployment: rsync -avz --exclude='.env' --exclude='credentials.json' --exclude='app_data/' --exclude='backups/' --exclude='logs/' ./ your_user@your_remote_server:/path/to/remote/project/
Example rsync command for pulling backups: rsync -avz your_user@your_remote_server:/path/to/remote/project/backups/ ./local_backups/
n8n Integration: n8n can be used to trigger backup scripts (via SSH to the Docker host or LXC, or via HTTP if a small API is exposed), monitor log files for specific events, or orchestrate post-ingestion workflows (e.g., sending notifications, triggering reports, moving backup files to cloud storage).
12. Monitoring and Logging
Celery Flower: Provides a real-time web UI for monitoring task queues, worker status, and task execution details.
Container Logs: All application logs (from app, worker, and celery_beat containers) will be directed to standard output/error, making them accessible via docker-compose logs.
Application-Level Logging: Python's logging module will capture detailed information about email processing, errors, and task status.
PostgreSQL Monitoring: Standard PostgreSQL monitoring tools can be used to track database performance, connections, and storage.
13. Security Considerations
OAuth 2.0: Securely handles Gmail authentication using OAuth 2.0. Tokens are stored securely in the PostgreSQL database.
Credential Management: credentials.json (Google API client secrets) should be securely stored and and mounted as read-only volumes. Database credentials for PostgreSQL should use environment variables (.env file in Docker Compose), never hardcoded or committed to version control.
Network Security: Configure firewalls and network policies to restrict access to PostgreSQL, RabbitMQ, and Flower ports only to necessary services or trusted IPs.
Least Privilege: Configure Gmail API scopes to the minimum required (e.g., gmail.readonly for fetching, gmail.modify if marking emails as read is desired). Database users should have only the necessary permissions.
Data Sanitization: Implement input validation and sanitization when parsing HTML content to prevent potential injection attacks before inserting data into the database.
14. Future Enhancements
Web UI: A simple web interface for monitoring system status, viewing processed emails, and managing rules (beyond Flower).
Alerting: Integrate with alerting systems (e.g., PagerDuty, Slack) for critical failures or rate limit warnings.
Schema Evolution: Implement a more sophisticated schema migration tool (e.g., Alembic) for managing database schema changes.
Data Validation Rules: Add more granular validation rules for extracted data before ingestion.
Alternative Email Sources: Extend the system to support other email providers (e.g., Microsoft Exchange, custom IMAP servers).
Machine Learning for Classification: Use ML models to classify emails and suggest rules, especially for new or ambiguous subjects.
Data Transformation Pipelines: Implement more complex data transformation steps using tools like Apache Airflow if data requires significant manipulation before ingestion.
Kubernetes Deployment: Transition to a Kubernetes cluster for enterprise-grade orchestration, auto-scaling, and high availability.
15. High-Level Project Phases and Timeline (Example)
Phase 1: Foundation & Core Logic (Weeks 1-3)
Set up Docker environment (docker-compose.yml, Dockerfile) including RabbitMQ, Celery Flower, and Celery Beat.
Implement Gmail API authentication and basic email ID fetching in the producer, with OAuth token storage in PostgreSQL.
Develop DBManager for basic PostgreSQL connection and email_metadata, system_state, and oauth_tokens table creation.
Configure Celery Beat to trigger the email fetching task periodically.
Initial logging and error handling.
Phase 2: Data Extraction & Ingestion (Weeks 4-6)
Implement Celery tasks for processing email IDs, fetching full email content (metadata, HTML, attachments) in workers.
Implement CSV attachment download and parsing within worker tasks.
Implement HTML body extraction and table parsing (BeautifulSoup4, pandas.read_html) within worker tasks.
Develop dynamic table creation logic in DBManager using SQLAlchemy.
Implement data ingestion for both CSV and HTML data into the financial schema.
Develop rules.yaml configuration and subject-based classification logic within worker tasks.
Phase 3: Testing & Deployment (Weeks 7-9)
Comprehensive unit and integration testing.
Performance testing and optimization for the distributed setup.
Security review.
Deployment to a staging environment using Docker Compose.
Set up data dump and log allocation strategy using bind mounts.
Documentation of setup, configuration, and operation.
Phase 4: Production Readiness & Monitoring (Weeks 10+)
Set up basic monitoring and alerting (leveraging Celery Flower).
Ongoing maintenance and support.
(Optional) Implement additional automation tasks (web scraping, IMAP processing) by adding new Celery tasks and updating rules.yaml.
16. Team and Roles (Placeholder)
Project Lead/Developer: Oversees project, designs architecture, develops code, manages deployment, ensures quality.
This project plan provides a solid foundation for developing a robust and scalable email data extraction system, tailored for a rapid, in-house deployment by a sole developer, with a clear vision for expanding into a comprehensive personal automation hub.
