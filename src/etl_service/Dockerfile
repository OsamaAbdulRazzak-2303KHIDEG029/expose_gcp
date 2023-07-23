FROM python:3.11-slim

# Install Java and cron
RUN apt-get update && apt-get install -y openjdk-17-jdk cron

# Set Java environment variables
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:${PATH}"

# Install Python
RUN apt-get update && apt-get install -y python3

WORKDIR /home/app

# Copy the Python dependencies
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the rest of the files
COPY . .

# Copy the cronjob file and give it proper permissions
COPY cronjob /etc/cron.d/cronjob
RUN chmod 0644 /etc/cron.d/cronjob

# Apply the cronjob
RUN crontab /etc/cron.d/cronjob

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Start cron and tail the log file
CMD cron && tail -f /var/log/cron.log
