# Dockerfile

# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.10-alpine

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Mounts the application code to the image
WORKDIR /code

# Allows docker to cache installed dependencies between builds
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

EXPOSE 8000

# runs the production server
CMD ["python", "manage.py", "runserver"]