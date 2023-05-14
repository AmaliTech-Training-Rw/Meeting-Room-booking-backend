FROM python:3.11.3-alpine

LABEL maintainer="Jean Claude GOMBANIRO"
# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

#RUN apk add --no-cache gcc musl-dev linux-headers && \
#    apk update  && \
#    apk add postgresql-dev && \
#    apk add --update --no-cache postgresql-client

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# Install python dependencies in /.venv
COPY Pipfile ./Pipfile
COPY Pipfile.lock ./Pipfile.lock

RUN python -m pip install --upgrade pip && \
    pip install pipenv && \
    pipenv install --dev --system --deploy
#    apk del .tmp-deps

# use system level package
#RUN pipenv install --dev --system --deploy
#use inside project virtual environment
#RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy  --dev

#FROM base AS runtime

# Copy virtual env from python-deps stage
#COPY --from=python-deps /.venv /.venv
#ENV PATH="./.venv/bin:$PATH"

# Install application into container
WORKDIR /app
COPY . /app

# Create and switch to a new user
#RUN useradd --create-home appuser

# Creates a non-root user and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
#WORKDIR /home/appuser
USER appuser

# Install application into container
#COPY . .

# Expose necessary ports
EXPOSE 8000

# Run the application
COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "./entrypoint.sh"]
# Run using the default server
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]