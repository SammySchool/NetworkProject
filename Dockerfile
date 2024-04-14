# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the server script into the container at /usr/src/app
COPY myserver.py ./
COPY tictactoe_game.py ./

# Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# Make port 5555 available to the world outside this container
EXPOSE 5555

# Define environment variable
ENV NAME World

# Run myserver.py when the container launches
CMD ["python", "./myserver.py"]