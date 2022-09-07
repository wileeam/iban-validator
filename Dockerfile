FROM python:3.10-slim

# Environment variables for flask app
ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "app.py"
ENV FLASK_RUN_HOST "0.0.0.0"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True

# Copying the content in the app directory
COPY . /app

# Changing to the working directory
WORKDIR /app 

# Installing the system and Pytohon dependencies
RUN apt-get update && \
    apt-get install -y libgomp1 gcc
RUN pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm requirements.txt

# Expose the port
EXPOSE 5000

# Entry level command to execute
CMD ["flask", "run"]
