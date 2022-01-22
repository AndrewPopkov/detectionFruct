FROM python:3.7-slim
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y
WORKDIR /detectionFruct
COPY app ./app
COPY model ./model
COPY config.py ./config.py
COPY requirements.txt ./requirements.txt
COPY run.py ./run.py

RUN pip install -r requirements.txt

CMD ["python3", "run.py"]