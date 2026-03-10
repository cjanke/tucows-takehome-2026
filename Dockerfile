FROM python:3.12-slim

# Set working directory inside the container
WORKDIR /app

# Install dependencies first (Docker will this layer, => faster rebuilds
# since it's not updated frequently)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Run the app variable in app/main.py on port 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]