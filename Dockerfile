# The first instruction is what image we want to base our container on
# We Use an official Python runtime as a parent image
FROM python:3.11-alpine3.15

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

# create root directory for our project in the container
RUN mkdir /bakery_admin_backend

# Set the working directory to /music_service
WORKDIR /bakery_admin_backend

# Copy the current directory contents into the container at /music_service
ADD . /bakery_admin_backend/

# Install postgresql-dev
# RUN apk add postgresql-client
# RUN apk add postgresql-dev
# RUN python -m pip install psycopg2-binary

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements_docker.txt

RUN apk add postgresql-client
