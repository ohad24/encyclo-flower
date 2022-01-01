FROM python:3.10-slim

WORKDIR /app

COPY vision.py requirements.txt ./

RUN pip install -r requirements.txt

CMD ["uvicorn", "vision:app", "--reload", "--port", "5001", "--host", "0.0.0.0"]