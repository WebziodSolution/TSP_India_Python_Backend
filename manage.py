#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calcsalary.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

# .\venv\Scripts\pip.exe install -r requirements.txt
# .\venv\Scripts\python manage.py runserver
# http://localhost:8000/api/schema/swagger-ui/
# {
#   "userName": "admin",
#   "companyId": "2026013001",
#   "password": "admin@123",
#   "noPassword": false
# }
# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOiIxMjIiLCJyb2xlSWQiOiIyMjciLCJyb2xlTmFtZSI6IjIyNyIsInJvbGUiOiIyMjciLCJjb21wYW55SWQiOiIxMjgiLCJ1c2VyTmFtZSI6IkFkbWluIiwic3ViIjoiQWRtaW4iLCJpYXQiOjE3ODA5OTk1MzIsImV4cCI6MTc4MTAzNTUzMn0.Jrsuc7LrLeLovR9jcxIIU7RJ30ervyowIVHrmAMQdzQ