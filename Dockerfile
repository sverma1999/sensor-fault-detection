FROM python:3.8.5-slim-buster
RUN apt update -y && apt install awscli -y

WORKDIR /app

COPY . /app

RUN pip install -r sf_project/requirements.txt

CMD ["python3", "sf_project/main.py"]