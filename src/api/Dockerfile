FROM python:3.10-slim 

ARG USERNAME=appuser
ARG APPDIR=/app

# These env variables MUST be provided in all environments
ENV MONGO_DB_NAME=
ENV MONGO_URI=
ENV GOOGLE_APPLICATION_CREDENTIALS=
ENV CLOUD_BUCKET=

# These env variables are optional in test/dev but must be in production
ENV SECRET_KEY=
ENV SMTP_USER=
ENV SMTP_PASS=

# These env variables should be provided in test/dev environments only
ENV SMTP_TEST=

WORKDIR ${APPDIR}
COPY . ${APPDIR}

# These values need to match the user on the host machine
# Fixes bug #42 but will should be removed to switch to dynamic values
ARG UID=2000
ARG GID=2000

RUN groupadd --gid ${GID} ${USERNAME} \
  && useradd --no-create-home --home-dir=${APPDIR} --uid=${UID} --gid=${GID} ${USERNAME} \
  && chown -R ${USERNAME}:${USERNAME} ${APPDIR}

RUN python -m pip install --upgrade --no-cache-dir pip \
  && pip install --upgrade --no-cache-dir -r ${APPDIR}/requirements.txt

ENV PYTHONPATH=${APPDIR}

USER ${USERNAME}
EXPOSE 8000
CMD [ "uvicorn", "main:app", "--host=0.0.0.0" ]
