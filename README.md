# Python CLI Task Manager

A simple yet powerful command-line to-do list application built with Python. This CLI tool allows users to easily add, view, mark as complete, and delete tasks, with all data persistently saved to ensure your to-dos are always there when you need them.

## MVP Features
- Add, list, complete, edit, delete tasks
- Tasks have title, due time, priority, and optional project
- All data is stored in a local JSON file
- Tested model and storage layers
- Clean and intuitive CLI powered by argparse

## Folder Structure
```
PYTHON-CLI-TODO/
├── models/
├── storage/
├── tests/
├── todo.py
├── README.md
└── todo.json
```

## 🛠 Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
