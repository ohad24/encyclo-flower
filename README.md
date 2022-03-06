## ENCYCLO-FLOWER SITE (v2)

### Development install and run
Environment variables:  
* GOOGLE_APPLICATION_CREDENTIALS - path to Google Cloud Service Account JSON file.
* MONGO_URI - MongoDB connection string. (default: mongodb://localhost:27017/)
* MONGO_DB_NAME - MongoDB database name. (default: dev)

#### Generic commands

* Find all `todo:`s and urgent (`# !`) comments in the code (`src/api`).  

    ```bash
    # -r search subdirectories
    # -n print line numbers
    # -i ignore case
    # -E extended regex
    grep -r -n -i -E 'todo\:|\# \!' src/api
    ```

#### backend
**API is running on Python 3.10**  
Install:  
Tests:  
Environment variables:  
* TESTS_GET_PLANTS_NAMES_LIMIT - query limit for get_plants_names
```bash
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


### quick setup test environment
    curl https://raw.githubusercontent.com/ohad24/encyclo-flower/main/scripts/test-environment.sh | bash


### dev environment:
* express - [http://localhost:8081/](http://localhost:8081/)
* swagger - [http://localhost:8000/docs](http://localhost:8000/docs)


### docs
#### learning assets
[fastapi](https://fastapi.tiangolo.com/)  
[pydantic](https://pydantic-docs.helpmanual.io/)  
[full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app)  
[ohad24/market](https://github.com/ohad24/market)