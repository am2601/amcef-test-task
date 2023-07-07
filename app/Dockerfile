FROM python:3.10

# Set the working directory in the container
WORKDIR /app


# Create a virtual environment
RUN python -m venv venv

# Activate the virtual environment
RUN . venv/bin/activate

# Upgrade pip and install the Python dependencies
RUN pip install --upgrade pip

# Copy project files to the container
COPY server /app
COPY Makefile /
COPY entrypoint.sh /

# Install the Python dependencies
RUN pip install -r /app/requirements.txt

ENTRYPOINT ["/entrypoint.sh"]