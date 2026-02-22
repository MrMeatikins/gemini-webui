FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install dependencies needed for gemini
RUN apt-get update && apt-get install -y \
    openssh-client \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Assuming gemini is installed via pip or a script, but we need it available.
# Since it's a CLI tool, let's install it globally if we can.
RUN curl -L https://github.com/openclaw/gemini-cli/releases/latest/download/gemini-linux-amd64 -o /usr/local/bin/gemini && chmod +x /usr/local/bin/gemini

COPY . .

# Set environment variables for Gemini
ENV GEMINI_HOME=/home/node/.gemini
# Expose the Flask port
EXPOSE 5000

# Create a non-root user (optional but good practice)
RUN useradd -m -u 1000 node
USER node

# We need access to the mounted volume for the host
CMD ["python", "app.py"]