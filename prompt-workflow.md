Developer Prompts Guide for CI/CD Workflow Design
This document outlines the sequence of prompts you, the developer, will issue to the LLM assistant to guide the development of your project's CI/CD pipeline and overall system. These prompts will drive the LLM's responses, leading to specific actions, code generation, and Git commits, thereby creating a self-documenting workflow.

Prompt Sequence
Prompt 1: Initial Project Setup Acknowledgment
Purpose: To inform the LLM that the foundational project setup is complete, and to instruct the LLM to read the guiding documents and prepare for the next steps.

Golden Rule for LLM: I will not create code, write documents, commit changes, or perform any modifications without your explicit permission and clear directives.

Your Prompt to LLM:

I have completed the initial project setup. The repository is cloned, and the `prompt-driven-dev-workflow.md` and `ci-cd-pipeline-solopreneur.md` (or `ci-cd-pipeline.md`) documents are now in the root of the project directory. Please acknowledge this setup, read these documents, and update the `project-status-log.md` accordingly.


Prompt 2: Initiate Project Directory and Initial File Creation
Purpose: To instruct the LLM to provide guidance for creating the essential project files and initializing the Git repository, as per Prompt 1.1 in the prompt-driven-dev-workflow.md.

Your Prompt to LLM:

I'm ready for the next step: creating the `.gitignore`, `README.md`, `status.log`, and `.env` files, and initializing Git. Please provide the guidance for Prompt 1.1 from the `prompt-driven-dev-workflow.md`.
you have my permission to create them.


Prompt 3: Initiate Core Development Environment Setup
Purpose: To instruct the LLM to provide guidance for setting up the core containerized development environment, including docker-compose.yml, Dockerfile, and populating the .env file, as per Prompt 1.2 in the prompt-driven-dev-workflow.md.

Your Prompt to LLM:

the initial file creation and Git initialization for the project directory is done. we are now ready to set up the core development environment. Please provide the guidance for Prompt 1.2 from the `prompt-driven-dev-workflow.md`.


Prompt 4: Commit Initial Project Files
Purpose: To instruct the LLM to guide the process of committing the initial project directory setup (including .gitignore, README.md, status.log, and .env files) to Git, with thorough documentation of the current state and next steps.

Your Prompt to LLM:

The initial project directory setup, including `.gitignore`, `README.md`, `status.log`, and `.env` files, is complete. I am now ready to commit these changes. Please guide me through the commit process, emphasizing thorough documentation of what's been done, our current status, and where we're going next.


Prompt 5: Confirm Completion of Initial Project File Creation and Git Initialization
Purpose: To inform the LLM that the actions outlined in Prompt 1.1 of the prompt-driven-dev-workflow.md have been completed and committed (as guided by Prompt 4 in this developer-prompts-guide.md), and to request guidance for the next logical step in the development workflow (Prompt 1.2 from prompt-driven-dev-workflow.md).

Your Prompt to LLM:

I have completed all the actions outlined in Prompt 1.1 of the `prompt-driven-dev-workflow.md`, including creating the project directory, initializing Git, and creating the `.gitignore`, `README.md`, `status.log`, and `.env` files. I have also performed the commit as guided by Prompt 4 in this `developer-prompts-guide.md`. I am now ready for the next logical step in the development workflow as per the `prompt-driven-dev-workflow.md`.


Prompt 6: Initiate Discussion of Project Plan Section
Purpose: To initiate a discussion about a specific section of the project's Project Plan document, to ensure a shared understanding of its goals and implementation details before proceeding with related development tasks. This prompt is designed to be repeatable for each section of the Project Plan.

Your Prompt to LLM:

I have completed all the actions for initial project setup and committed them. I am now ready to discuss the project plan. Please refer to Section [SECTION_NUMBER_OR_NAME] of our Project Plan document and initiate a discussion about its implementation. No code generation, writing, committing, or editing of documents or files without explicit permission.


The Section Development Loop: Ingest, Discuss, Design, Agree, Implement, Commit, Push, Test
For each section of the Project Plan, we will follow an iterative loop to ensure thorough understanding, careful design, and documented implementation.

Prompt 7: Confirm Section Discussion/Design and Initiate Implementation
Purpose: To inform the LLM that the discussion and design for a specific Project Plan section are complete (or sufficiently understood to begin implementation), and to request guidance for the implementation steps, leading to a commit, push, and test cycle. This prompt signifies readiness to transition from planning/design to active coding/configuration.

Your Prompt to LLM:

The discussion and design for Section [SECTION_NUMBER_OR_NAME] of the Project Plan are complete. I am now ready to proceed with its implementation. Please provide guidance for the implementation steps, and prepare for the subsequent commit, push, and test cycle. No code generation, writing, committing, or editing of documents or files without explicit permission.


Prompt 8: Confirm Implementation and Initiate Commit/Push/Test
Purpose: To inform the LLM that the implementation work for a specific Project Plan section is complete, and to request guidance for the final commit, push, and testing steps for that section. This prompt ensures that every implemented piece of functionality is properly documented and verified through the CI/CD pipeline.

Your Prompt to LLM:

I have completed the implementation for Section [SECTION_NUMBER_OR_NAME] of the Project Plan. I am now ready to commit, push, and test these changes. Please guide me through the process, ensuring thorough documentation and verification. No code generation, writing, committing, or editing of documents or files without explicit permission.

(This document will be updated as we design more prompts for subsequent steps in the workflow.)