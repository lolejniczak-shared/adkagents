
FROM python:3.11-slim
WORKDIR /app

# Create a non-root user
RUN adduser --disabled-password --gecos "" myuser

# Change ownership of /app to myuser
RUN chown -R myuser:myuser /app

# Switch to the non-root user
USER myuser

# Set up environment variables - Start
ENV PATH="/home/myuser/.local/bin:$PATH"

ENV GOOGLE_GENAI_USE_VERTEXAI=1
ENV GOOGLE_CLOUD_PROJECT=genai-app-builder
ENV GOOGLE_CLOUD_LOCATION=us-central1

# Set up environment variables - End

# Install ADK - Start
RUN pip install google-adk
# Install ADK - End

# Copy agent - Start


COPY "/" "/app/agents/"
RUN pip install -r "/app/agents/requirements.txt"

# Copy agent - End

EXPOSE 8000

CMD adk web --port=8000 --host=0.0.0.0 "/app/agents"
