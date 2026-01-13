FROM ubuntu:24.04

# Set non-interactive front-end
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y cron python3.9 python3-pip

# Install poetry
RUN pip3 install poetry

# Set the working directory in the container
WORKDIR /app

# Copy project files
COPY . .

# Make the cron script executable
RUN chmod +x /app/scripts/run_cron.sh

# Install python dependencies
# Note: A poetry.lock file is required. Generate it by running `poetry lock`.
RUN poetry config virtualenvs.create false && poetry install --no-dev --no-interaction --no-ansi

# Copy crontab file
COPY crontab /etc/cron.d/blob_cron

# Give execution rights to the cron job
RUN chmod 0644 /etc/cron.d/blob_cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
ENTRYPOINT ["cron", "-f"]
