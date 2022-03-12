FROM python:3.10-slim 

ARG USERNAME=appuser
ARG APPDIR=/app

# These env variables should be provided in deployment
ENV MONGO_DB_NAME=
ENV MONGO_URI=
ENV GOOGLE_APPLICATION_CREDENTIALS=

WORKDIR ${APPDIR}
COPY . ${APPDIR}

RUN useradd --no-create-home --home-dir=${APPDIR} ${USERNAME} \
  && chown -R ${USERNAME}:${USERNAME} ${APPDIR}

RUN python -m pip install --upgrade --no-cache-dir pip \
  && pip install --upgrade --no-cache-dir -r ${APPDIR}/requirements.txt

ENV PYTHONPATH=${APPDIR}

USER ${USERNAME}
EXPOSE 8000
CMD [ "uvicorn", "main:app", "--host=0.0.0.0" ]
