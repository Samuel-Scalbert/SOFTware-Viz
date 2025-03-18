# Use the slim Python image
FROM python:3.10-slim
LABEL authors="sscalbert"

# Set the working directory
WORKDIR /SOFTware-Viz

# Install required system packages
RUN apt update && apt install -y nano curl && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt /SOFTware-Viz/

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . /SOFTware-Viz/

# Expose the port the app runs on
EXPOSE 8080

# Specify the command to run on container start
CMD ["python", "run.py"]
