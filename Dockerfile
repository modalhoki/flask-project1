# Use an official Python runtime as the base image
FROM swipl:stable

RUN apt-get update && apt-get install -y python3.9 python3-pip

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose any necessary ports
EXPOSE 5000

# Set the command to run the application
CMD [ "python3.9", "app.py" ]