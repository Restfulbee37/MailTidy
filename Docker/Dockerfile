FROM python:3.13-slim

RUN apt update && apt install curl -y 

# Set the working directory in the container
WORKDIR /MailTidy

# Copy the parent directory contents into the container
COPY . /MailTidy

# Install packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD ["python", "app/sortmail.py"]
