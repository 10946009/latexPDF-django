FROM --platform=linux/arm64/v8 sd030/my-latex:my-latex-0318

# Install libpq-dev and pip install poetry
RUN apt-get update && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/* && \
    pip install poetry

# Copy requirements.txt and pyproject.toml (if available)
COPY requirements.txt ./
COPY pyproject.toml ./

# Copy the rest of the application
COPY . /app

WORKDIR /app

# Set PATH to include Poetry's bin directory
ENV PATH="${PATH}:/root/.local/bin"

# Install Python dependencies
RUN poetry install

# Set the entrypoint to run the server
ENTRYPOINT ["poetry", "run", "python3", "manage.py", "runserver", "0.0.0.0:8000"]
