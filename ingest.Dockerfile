# ingest.Dockerfile

FROM python:3.11-slim
WORKDIR /app

# Copy the requirements file first for caching
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the .env file into the container's working directory
COPY ./.env /app/.env

# Copy the documents and the script needed for ingestion
COPY ./documents /app/documents
COPY ./scripts/ingest.py /app/ingest.py

# This is the command that will run when the Job starts
CMD ["python", "ingest.py"]