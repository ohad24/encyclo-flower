FROM python:3.8

RUN apt -y update
RUN apt -y install libusb-1.0-0-dev libportaudio2

ADD requirements.txt .

# RUN pip install tflite-runtime tflite-support==0.4.0 fastapi "uvicorn[standard]" python-multipart
RUN pip install -r requirements.txt

WORKDIR /app

ADD plant_recognition.py .

ADD PlantDetect.tflite .

ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
# ENV IMG=

# CMD ["sh", "-c", "python plant_recognition.py /app/images/${IMG}"]
# CMD ["sh", "-c", "echo ${IMG}"]

CMD ["uvicorn", "plant_recognition:app", "--port", "8080" , "--host", "0.0.0.0"]
