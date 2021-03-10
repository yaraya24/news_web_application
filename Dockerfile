FROM python:3.8

# Environment Variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Work directory
WORKDIR /backend

# Install dependencies
COPY ./backend/Pipfile ./backend/Pipfile.lock /backend/
RUN pip install pipenv && pipenv install --system

# Copy the project
COPY ./backend /backend