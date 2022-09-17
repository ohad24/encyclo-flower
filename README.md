# ENCYCLO-FLOWER SITE (v2)

[![API build](https://github.com/ohad24/encyclo-flower/actions/workflows/api.yml/badge.svg)](https://github.com/ohad24/encyclo-flower/actions/workflows/api.yml)
[![SWAG build](https://github.com/ohad24/encyclo-flower/actions/workflows/swag.yml/badge.svg)](https://github.com/ohad24/encyclo-flower/actions/workflows/swag.yml)
[![Ansible deployment](https://github.com/ohad24/encyclo-flower/actions/workflows/server.yml/badge.svg)](https://github.com/ohad24/encyclo-flower/actions/workflows/server.yml)
[![codecov](https://codecov.io/gh/ohad24/encyclo-flower/branch/main/graph/badge.svg?token=SX4X7ULMXX)](https://codecov.io/gh/ohad24/encyclo-flower)

[![Known Vulnerabilities](https://snyk.io/test/github/ohad24/encyclo-flower/badge.svg?targetFile=src/api/requirements.txt)](https://snyk.io/test/github/ohad24/encyclo-flower)
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/f58c7a17253340d7be1344a12e984e7a)](https://www.codacy.com/gh/ohad24/encyclo-flower/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=ohad24/encyclo-flower&amp;utm_campaign=Badge_Grade)
[![Total alerts](https://img.shields.io/lgtm/alerts/g/ohad24/encyclo-flower.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ohad24/encyclo-flower/alerts/)
[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/ohad24/encyclo-flower.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/ohad24/encyclo-flower/context:python)

Hello all 👋, Welcome to the Encyclo-Flower site source code. This repo contains the source code for the entire site tech stack (Backend API, Frontend, VM configuration, CI/CD automation, tests, and SWAG web server).

## Site main features

* Custom search across more then 3000 species of plants.
* User image recognition to identify plant species.
* Community questions and answers to help users find the right plant they looking for.
* Community observations, users can share their observations and plant images.

## Development install and run

### Backend

**API is running on Python 3.10**  
Install:  
Environment variables:

* GOOGLE_APPLICATION_CREDENTIALS - path to Google Cloud Service Account JSON file.  
* COULD_BUCKET - name of Google Cloud Storage bucket.  
* MONGO_URI - MongoDB connection string. (example: mongodb://root:example@localhost:27017/)  
* MONGO_DB_NAME - MongoDB database name. (default: dev)  
* SECRET_KEY - secret key for session. (default is generated randomly in `config.py`)  
    To create new one run: `openssl rand -hex 32`  
* SMTP_USER - SMTP username (gmail address). Not mandatory.  
* SMTP_PASS - SMTP password. Not mandatory.  
* DETECT_API_SRV - URL to the detect API server. (default: http://localhost:5001)  
* TESTS_GET_PLANTS_NAMES_LIMIT - query limit for get_plants_names  

Tests:

  ```bash
  # For testing + coverage, formatting and linting:
  pip install pytest pytest-cov black flake8

  # pwd
  # ./encyclo-flower
  # enter venv
  pytest -v -x -s --cov=src/api/ --cov-report xml --cov-report html:.cov_html
  
  # exclude one test VIA command line
  pytest -x -s -vv -k 'not detect_image' tests/api/
  
  # format
  black src/api/

  # lint
  flake8 src/api/
  ```

Run:

  ```bash
  # enter venv
  cd src/api
  uvicorn main:app --reload
  ```

#### Dev environment

* express - [http://localhost:8081/](http://localhost:8081/)
* swagger - [http://localhost:8000/docs](http://localhost:8000/docs)

## Ansible (Server automatic configuration)

  ```bash
  sudo apt install ansible
  cd server
  ansible-galaxy role install -r requirements.yml
  ansible-galaxy collection install -r requirements.yml
  # CREATE a 'hosts' file before the next step (see `hosts.example`)
  ansible-playbook -i hosts playbook.yml
  ```

## Docs

### learning assets

[fastapi](https://fastapi.tiangolo.com/)  
[pydantic](https://pydantic-docs.helpmanual.io/)  
[full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app)  
[ohad24/market](https://github.com/ohad24/market)
