# Use an official Python runtime as a parent image
FROM python:3.11-slim-bookworm

# Set version label
LABEL version="2.0"
# Custom image name: latex-pdf-converter

# Install necessary dependencies for Tectonic
RUN apt-get update && apt-get install -y \
    libfontconfig1 \
    libgraphite2-3 \
    libharfbuzz0b \
    libicu72 \
    libssl3 \
    zlib1g \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Tectonic
RUN wget https://github.com/tectonic-typesetting/tectonic/releases/download/tectonic%400.15.0/tectonic-0.15.0-x86_64-unknown-linux-gnu.tar.gz \
    && tar -xzvf tectonic-0.15.0-x86_64-unknown-linux-gnu.tar.gz \
    && mv tectonic /usr/local/bin/ \
    && rm tectonic-0.15.0-x86_64-unknown-linux-gnu.tar.gz

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run app.py when the container launches
CMD ["python3", "server.py"]