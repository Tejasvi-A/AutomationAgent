from flask import Flask, request, jsonify
from utils import execute_task, read_file
import openai
import os
import requests
import git
import sqlite3
from bs4 import BeautifulSoup
import requests
import markdown2
from datetime import datetime


app = Flask(__name__)

API_KEY = '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'

# Configure OpenAI API Key
openai.api_key = API_KEY

@app.route('/run', methods=['POST'])
def run_task():
    task_description = request.args.get('task')
    if not task_description:
        return jsonify({"error": "Task description is required"}), 400

    try:
        result = execute_task(task_description)
        return jsonify({"message": "Task executed successfully", "result": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/read', methods=['GET'])
def read_file_endpoint():
    file_path = request.args.get('path')
    if not file_path:
        return jsonify({"error": "File path is required"}), 400

    try:
        content = read_file(file_path)
        return content, 200
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)


#Validate File Paths:
def validate_file_path(file_path):
    if not file_path.startswith("/data/"):
        raise ValueError("Access outside /data directory is prohibited.")


def execute_a3():
    # Read the list of dates from /data/dates.txt
    dates_file_path = "/data/dates.txt"
    with open(dates_file_path, 'r') as f:
        dates = f.readlines()

    # Count Wednesdays
    wednesdays_count = sum(1 for date_str in dates if datetime.strptime(date_str.strip(), "%Y-%m-%d").weekday() == 2)

    # Write the result to /data/dates-wednesdays.txt
    with open("/data/dates-wednesdays.txt", 'w') as f:
        f.write(str(wednesdays_count))

    return f"Count of Wednesdays: {wednesdays_count} written to /data/dates-wednesdays.txt"

#B3: Fetch data from an API and save it:
def execute_b3():
    api_url = "https://example.com/api/data"
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        with open("/data/fetched_data.json", 'w') as file:
            json.dump(data, file)
        return "Data fetched from API and saved to /data/fetched_data.json"
    else:
        raise ValueError("Failed to fetch data from API.")

#B4: Clone a Git repo and make a commit:
def execute_b4():
    repo_url = "https://github.com/user/repo.git"
    repo_dir = "/data/repo"
    
    # Clone the repository
    repo = git.Repo.clone_from(repo_url, repo_dir)
    
    # Add and commit a change
    file_path = os.path.join(repo_dir, "file.txt")
    with open(file_path, "w") as f:
        f.write("Sample commit content.")
    
    repo.git.add(file_path)
    repo.index.commit("Automated commit")
    
    # Push the changes (ensure you have configured authentication)
    repo.git.push()
    
    return f"Changes committed and pushed to {repo_url}"


#B5: Run a SQL query on SQLite database:
def execute_b5():
    conn = sqlite3.connect("/data/ticket-sales.db")
    cursor = conn.cursor()
    
    # Run a query (e.g., total sales of "Gold" ticket type)
    cursor.execute("SELECT SUM(price * units) FROM tickets WHERE type='Gold'")
    total_sales = cursor.fetchone()[0]
    
    with open("/data/ticket-sales-gold.txt", "w") as f:
        f.write(str(total_sales))
    
    conn.close()
    return f"Total Gold ticket sales: {total_sales}"

#B6: Scrape data from a website (Using BeautifulSoup):
def execute_b6():
    url = "https://example.com"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract all H1 headings
    headings = [h1.text for h1 in soup.find_all('h1')]
    
    with open("/data/scraped_headings.txt", "w") as f:
        for heading in headings:
            f.write(heading + "\n")
    
    return "Website scraped and H1 headings saved."

#B9: Convert Markdown to HTML:
def execute_b9():
    with open("/data/markdown_file.md", "r") as f:
        markdown_content = f.read()

    html_content = markdown2.markdown(markdown_content)
    
    with open("/data/markdown_file.html", "w") as f:
        f.write(html_content)
    
    return "Markdown file converted to HTML."

