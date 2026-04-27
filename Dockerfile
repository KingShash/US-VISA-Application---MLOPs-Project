FROM python:3.12-slim-bullseye

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["python3", "app.py"]