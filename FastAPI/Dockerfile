FROM python:3.10

WORKDIR /api

COPY ./requirements.txt /FASTAPI/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /FASTAPI/requirements.txt

COPY ./app /api/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]