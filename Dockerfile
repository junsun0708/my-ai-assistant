# ============================================
# my-ai-assistant Docker Configuration
# ============================================

# Stage 1: Builder
FROM python:3.11-slim AS builder

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Install Node.js and npm for Claude CLI
RUN apt-get update && apt-get install -y --no-install-recommends \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Install Claude CLI
RUN npm install -g @anthropic-ai/claude-code

WORKDIR /app

# Copy installed packages from builder to accessible location
COPY --from=builder /root/.local /app/.packages
ENV PATH=/app/.packages/bin:$PATH
ENV PYTHONPATH=/app/.packages/lib/python3.11/site-packages:$PYTHONPATH

# Copy application code
COPY . .

# Run as non-root user for security
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Default command
CMD ["python", "app.py"]
