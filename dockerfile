FROM python:3.11

WORKDIR /app

ADD . /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && \
    apt-get install -y build-essential && \
    apt-get install -y python3-dev && \
    pip install --upgrade pip && \
    pip install -r requirements.txt 

EXPOSE 5000
CMD ["python", "appAIFlask.py"]