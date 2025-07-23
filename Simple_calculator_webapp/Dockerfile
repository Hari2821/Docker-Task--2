FROM python:3.11-slim

WORKDIR /app

# Copy only the requirements first
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

EXPOSE 5000

CMD ["python", "app.py"]

