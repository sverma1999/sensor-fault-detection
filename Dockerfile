FROM python:3.8.5-slim-buster
RUN apt update -y && apt install awscli -y

WORKDIR /app

COPY ./sfd_project /app

RUN pip install -r /app/requirements.txt

CMD ["python3", "/app/main.py"]