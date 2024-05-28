# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy only the requirements file, to cache the installed Python packages
COPY requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app

# Download the models and necessary files during the build
RUN python -c "from sentence_transformers import SentenceTransformer; \
    SentenceTransformer('all-MiniLM-L6-v2')"

# Combine commands into the Dockerfile CMD directive
CMD ls -trl && sleep 40 && python3 initialise_database.py && exec streamlit run app.py --server.address 0.0.0.0
