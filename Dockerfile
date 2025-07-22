FROM --platform=linux/amd64 python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Copy all files and folders into the container's /app
COPY . /app

# Install required Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# The command that should run when container starts
CMD ["python", "extract_outline.py"]
