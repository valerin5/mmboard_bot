FROM python:3.9-slim

WORKDIR /opt

ENV PYTHONPATH=/opt

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./mmboard_bot mmboard_bot

ENTRYPOINT ["python3", "mmboard_bot"]
