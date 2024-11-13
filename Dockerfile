FROM python:3.11-slim

ENV PIPENV_VENV_IN_PROJECT=1
ENV PIPENV_IGNORE_VIRTUALENVS=1

RUN apt-get update && apt-get install -y supervisor && \
    pip install --upgrade pip && \
    pip install pipenv

WORKDIR /app

COPY Pipfile Pipfile.lock /app/
RUN pipenv install --deploy --ignore-pipfile

COPY . /app

# Copy supervisord configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8000

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
