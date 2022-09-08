# Image Detection

This service is used to detect objects in images. It uses the TensorFlow Object Detection API.

❗ **This service only works with Python 3.8.**

## Run and test the service

Run:

```bash
uvicorn plant_recognition:app --reload --port 5000
```

Text with CURL:

```bash
curl -X 'POST' \
    'http://localhost:5000/detect/' \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -F 'file=@images4tests/Kalanit.jpg;type=image/jpeg' | jq .
```
