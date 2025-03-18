# Dockerfile

FROM python:3.10-slim
LABEL authors="sscalbert"

# Set the working directory
WORKDIR /SOFTware-Viz

# Copy the requirements file into the container
COPY requirements.txt /SOFTware-Viz/

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the wait-for-it script to /usr/local/bin
COPY wait-for-it.sh /usr/local/bin/wait-for-it.sh

# Ensure the script is executable
RUN chmod +x /usr/local/bin/wait-for-it.sh

# Copy the rest of the application files into the container
COPY . /SOFTware-Viz/

# Expose the port the app runs on
EXPOSE 8080

# Specify the command to run on container start
CMD ["python", "run.py"]