FROM python:latest

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
ADD . /app

# Install any needed packages specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Set the environment variable for the port
ENV PORT=5000

# Expose the port specified in the environment variable
EXPOSE $PORT

# Run app.py when the container launches
CMD ["python", "app.py"]