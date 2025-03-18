# Dockerfile

FROM python:3.10-slim
LABEL authors="sscalbert"

# Set the working directory
WORKDIR /SOFTware-Viz

# Install curl (or inetutils-ping for ping)
RUN apt-get update && apt-get install -y curl

# Copy the requirements file into the container
COPY requirements.txt /SOFTware-Viz/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . /SOFTware-Viz/

# Expose the correct port (8040 for Flask app)
EXPOSE 8040
