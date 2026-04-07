# 1. Use an official, lightweight Python image as the base operating system
FROM python:3.10-slim

# 2. Prevent Python from writing .pyc files and force stdout to log instantly
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Set the working directory inside the container
WORKDIR /app

# 4. Install the complex C-libraries required by GeoDjango and PostGIS
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    python3-gdal \
    && rm -rf /var/lib/apt/lists/*

# 5. Copy your requirements file into the container
COPY requirements.txt /app/

# 6. Install your Python packages
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# 7. Copy the rest of your Django project into the container
COPY . /app/