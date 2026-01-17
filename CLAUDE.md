# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python Flask project for collecting user data (name, age) via a web form and storing it in a local SQLite database. The application has two main pages:
- A form page to input and save user data
- A display page to view stored data from the database

## Development Commands

```bash
# Install dependencies
pip install flask

# Run the Flask development server
python app.py
# or
flask run

# The app runs at http://localhost:5000 by default
```

## Architecture

- **app.py**: Main Flask application with routes and database logic
- **templates/**: Jinja2 HTML templates for the form and display pages
- **database.db**: SQLite database file (created in the same directory)
