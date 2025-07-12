# Use official Python slim image
FROM python:3.12-slim

# Install system dependencies for Chromium
RUN apt-get update && apt-get install -y \
    libnss3 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libgbm1 \
    libasound2 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxcb1 \
    libxext6 \
    libxfixes3 \
    libglib2.0-0 \
    libgtk-3-0 \
    libdbus-1-3 \
    libnspr4 \
    libnss3 \
    libx11-6 \
    libexpat1 \
    libatspi2.0-0 \
    libgio-2.0-0 \
    --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy and install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers
RUN playwright install chromium

# Copy your app
COPY . .

# Start your bot
CMD ["python", "main.py"]

CMD ["python", "main.py"]
