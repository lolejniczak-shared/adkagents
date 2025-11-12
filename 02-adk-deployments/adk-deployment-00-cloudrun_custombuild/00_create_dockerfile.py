import os 
from dotenv import load_dotenv

load_dotenv()

with_ui = True
with_cloud_trace = True
gcp_project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
gcp_region = os.getenv("GOOGLE_CLOUD_LOCATION")
app_name = os.getenv("ADK_APP_NAME")
temp_folder = "./"

##COPY "/{app_name}" "/app/agents/{app_name}/"
##RUN pip install -r "/app/agents/{app_name}/requirements.txt"


_DOCKERFILE_TEMPLATE = """
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
ENV GOOGLE_CLOUD_PROJECT={gcp_project_id}
ENV GOOGLE_CLOUD_LOCATION={gcp_region}

# Set up environment variables - End

# Install ADK - Start
RUN pip install google-adk
# Install ADK - End

# Copy agent - Start


COPY "/" "/app/agents/"
RUN pip install -r "/app/agents/requirements.txt"

# Copy agent - End

EXPOSE {port}

CMD adk {command} --port={port} --host=0.0.0.0 "/app/agents"
"""

dockerfile_content = _DOCKERFILE_TEMPLATE.format(
        gcp_project_id=gcp_project_id,
        gcp_region=gcp_region,
        ##app_name=app_name,
        port="8000",
        command='web' if with_ui else 'api_server',
        trace_to_cloud_option='--trace_to_cloud' if with_cloud_trace else '',
    )

dockerfile_path = os.path.join(temp_folder, 'Dockerfile')
os.makedirs(temp_folder, exist_ok=True)
with open(dockerfile_path, 'w', encoding='utf-8') as f:
      f.write(
          dockerfile_content,
      )