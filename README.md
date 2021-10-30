## ENCYCLO-FLOWER SITE (v2)

### Development install and run
#### backend
**API is running on Python 3.10**  
Install:  
Tests:  
```bash
# pwd
# ./encyclo-flower
# enter venv
pytest -v -x -s --cov=src/api/ --cov-report xml --cov-report html:.cov_html

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





### dev environment:
* express - [http://localhost:8081/](http://localhost:8081/)
* swagger - [http://localhost:8000/docs](http://localhost:8000/docs)


### docs
#### learning assets
[fastapi](https://fastapi.tiangolo.com/)  
[pydantic](https://pydantic-docs.helpmanual.io/)  
[full-stack-fastapi-postgresql](https://github.com/tiangolo/full-stack-fastapi-postgresql/tree/master/%7B%7Bcookiecutter.project_slug%7D%7D/backend/app/app)  
[ohad24/market](https://github.com/ohad24/market)