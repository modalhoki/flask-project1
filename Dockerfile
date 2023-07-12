# Use an official Python runtime as the base image
FROM swipl:7.6.4

# Update stretch repositories
RUN sed -i -e 's/deb.debian.org/archive.debian.org/g' \
           -e 's|security.debian.org|archive.debian.org/|g' \
           -e '/stretch-updates/d' /etc/apt/sources.list

RUN mkdir -p /usr/share/man/man1 && mkdir -p /usr/share/man/man7

RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y curl wget build-essential libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev

RUN wget https://www.python.org/ftp/python/3.9.17/Python-3.9.17.tgz && \
    tar xzf Python-3.9.17.tgz && \
    cd Python-3.9.17 && \
    ./configure --enable-optimizations && \
    make altinstall

RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3.9 get-pip.py

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