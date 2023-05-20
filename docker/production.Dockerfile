# This docker file is used for production
# Creating image based on official python3 image
FROM python:3.11.2
ENV BASE_DIR=/app
ENV APP_HOME=${BASE_DIR}/backend
ENV PYTHONUNBUFFERD=1

RUN useradd -ms /bin/bash appuser
RUN mkdir -p ${APP_HOME} &&\
    chown -R appuser:appuser ${BASE_DIR}

WORKDIR ${APP_HOME}

COPY requirements/ requirements/
RUN pip install -r requirements/production.txt

USER appuser
RUN mkdir staticfiles media
COPY --chown=appuser:appuser . ${APP_HOME}
EXPOSE 8000