FROM python:3.8

RUN apt -y update
RUN apt -y install libusb-1.0-0-dev libportaudio2

RUN pip install tflite-runtime tflite-support==0.4.0 fastapi "uvicorn[standard]" python-multipart

WORKDIR /app

ADD plant_recognition.py .
ADD PlantDetect.tflite .

ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
# ENV IMG=

# CMD ["sh", "-c", "python plant_recognition.py /app/images/${IMG}"]
# CMD ["sh", "-c", "echo ${IMG}"]