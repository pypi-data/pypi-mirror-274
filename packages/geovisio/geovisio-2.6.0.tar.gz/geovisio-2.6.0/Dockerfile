FROM python:3.9-slim


# Install system dependencies
# and create a `geovisio` user, to run the app as non root user
RUN apt update \
    && apt install -y git \
    && pip install waitress \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /opt/geovisio /data/geovisio \
    && groupadd --gid 1000 geovisio \
    && useradd --uid 1000 --gid 1000 -m geovisio \
    && chown -R geovisio:geovisio /opt/geovisio /data/geovisio

WORKDIR /opt/geovisio
USER geovisio

# Install Python dependencies
COPY ./README.md ./LICENSE ./pyproject.toml ./
COPY ./geovisio/__init__.py ./geovisio/
RUN pip install -e . --user

# Add source files
COPY ./images ./images/
COPY ./docker/docker-entrypoint.sh ./
COPY ./geovisio ./geovisio
COPY ./migrations ./migrations

# Environment variables
ENV FLASK_APP=geovisio
ENV FS_URL="/data/geovisio"

# Expose service
EXPOSE 5000
ENTRYPOINT ["./docker-entrypoint.sh"]
