import openai
import os
import json
import re
from datetime import datetime

# Helper function to read a file
def read_file(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File {file_path} not found")
    with open(file_path, 'r') as file:
        return file.read()

# Helper function to execute tasks based on description
def execute_task(task_description):
    # Use LLM to process the task description and map it to operations
    task_type = parse_task_description(task_description)
    if task_type == "A1":
        return execute_a1()
    elif task_type == "A2":
        return execute_a2()
    # Implement other task executors like A3, A4, A5, etc.
    else:
        raise ValueError(f"Unknown task type: {task_type}")

# Parse the task description to identify the task type
def parse_task_description(description):
    # Example: Check if task_description contains certain keywords or patterns
    if "Install uv" in description:
        return "A1"
    elif "Format the contents" in description:
        return "A2"
    # Add more parsing logic to identify other tasks
    else:
        raise ValueError("Invalid task description")

# Task A1: Execute script with user.email
def execute_a1():
    # Extract the user's email from the task description
    user_email = extract_email_from_task_description("user.email")
    # Call the external datagen.py script with the provided email
    os.system(f"python3 datagen.py {user_email}")
    return "Data generation completed."

# Task A2: Format file contents using prettier
def execute_a2():
    file_path = "/data/format.md"
    os.system(f"prettier --write {file_path}")
    return f"File {file_path} formatted using Prettier."

# Helper to extract email from description (if applicable)
def extract_email_from_task_description(description):
    # Here you would parse the email address from the description, e.g.:
    match = re.search(r"(\S+@\S+)", description)
    return match.group(1) if match else None
