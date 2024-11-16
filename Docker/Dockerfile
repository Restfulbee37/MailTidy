FROM python:3.13-slim

RUN apt update && apt install curl -y 

# Set the working directory in the container
WORKDIR /MailTidy

# Copy the parent directory contents into the container
COPY . /MailTidy

# Install packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
#EXPOSE 8080

# Define environment variable
#ENV PYTHONUNBUFFERED=1

# Run app.py when the container launches
CMD ["python", "app/sortmail.py"]
