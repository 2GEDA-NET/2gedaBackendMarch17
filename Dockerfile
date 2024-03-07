FROM python:3.10-alpine

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt /tmp/requirements.txt

# Install any needed packages specified in requirements.txt
RUN python -m venv /py && \
    source /py/bin/activate && \
    pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        gcc libc-dev ffmpeg linux-headers build-base postgresql-dev && \
    pip install -r /tmp/requirements.txt && \
    apk del .tmp-build-deps && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        togeda-user

# Copy the rest of the working directory contents into the container at /app
COPY . /app

# Update the PATH environment variable
ENV PATH="/py/bin:$PATH"

# Set the user to use when running this image
USER togeda-user