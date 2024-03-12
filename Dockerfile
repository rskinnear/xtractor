# Use an official Python runtime as a parent image
FROM python:3.11.4-slim-bookworm

# Update the package list
RUN apt-get update

# Install Firefox and wget
RUN apt-get install -y firefox-esr wget

# Install GeckoDriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz \
    && tar -xzf geckodriver-v0.34.0-linux64.tar.gz \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/

# Clean up the cache and remove unnecessary packages
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* geckodriver-v0.34.0-linux64.tar.gz

# Copy the current directory contents into the container at /usr/src/app
WORKDIR /usr/src/app
COPY . .

# Install Python dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the tester.py script when the container launches
CMD ["python", "tester.py"]
