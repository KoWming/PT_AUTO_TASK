# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Install cron
RUN apt-get update && apt-get install -y cron tzdata

# Set the timezone to UTC+8
RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo "Asia/Shanghai" > /etc/timezone

# Add crontab file in the cron directory
COPY crontab /etc/cron.d/my-cron-job

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/my-cron-job

# Apply cron job
RUN crontab /etc/cron.d/my-cron-job

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Set environment variable for cron expression
ENV CRON_EXPRESSION="30 9,21 * * *"

# Run the command on container startup
CMD printenv | grep CRON_EXPRESSION | awk -F '=' '{print $2 " /usr/local/bin/python /app/main.py >> /var/log/cron.log 2>&1"}' > /etc/cron.d/my-cron-job && \
    crontab /etc/cron.d/my-cron-job && \
    cron && tail -f /var/log/cron.log