# Use a base image with Python
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt /app/requirements.txt
# RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire FastAPI app directory into the container
COPY . /app

# Copy the .env file into the container
COPY .env /app/.env

# Expose the port where the FastAPI app will run
EXPOSE 8000

# Start the FastAPI server using uvicorn
CMD ["python", "-m", "main"]
#docker run -d -p 3000:3000 --restart=unless-stopped your_image_name