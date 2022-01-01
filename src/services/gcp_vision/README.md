# GCP Vision service

## Install
Create new virtual environment and then install the required packages:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Tests
### Python script (run main function)
```bash
python vision.py
```

### Bash script
Run with unicorn (with service 5001)
```bash
Uvicorn vision:app --reload --port 5001
```bash
Then run ./test.sh
```

## Deploy
### Docker
### Cloud Run