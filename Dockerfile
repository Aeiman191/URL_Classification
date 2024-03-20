FROM python:3.10

# Install Dockerfile
RUN apt-get update && apt-get install -y docker.io

# Set the working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the entry point
CMD [ "python", "app.py" ]