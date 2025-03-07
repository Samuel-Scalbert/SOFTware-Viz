# Dockerfile

FROM python:3.10-slim
LABEL authors="sscalbert"

# Set the working directory
WORKDIR /SOFTware-Viz

# Copy the requirements file into the container
COPY requirements.txt /SOFTware-Viz/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files into the container
COPY . /SOFTware-Viz/

# Expose the port the app runs on
EXPOSE 8080