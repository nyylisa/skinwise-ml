# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Create a non-root user, which is a Hugging Face Spaces requirement
RUN useradd -m -u 1000 appuser

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application's code into the container
COPY . .

# Change ownership of the app directory to the non-root user
RUN chown -R appuser:appuser /app
USER appuser

# Make port 7860 available to the world outside this container
# Hugging Face Spaces requires the app to run on port 7860
EXPOSE 7860

# Command to run the application using Uvicorn when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]
