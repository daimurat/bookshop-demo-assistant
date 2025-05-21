FROM python:3.11

WORKDIR /code

COPY ./data /code/data
COPY ./ingest.py /code/ingest.py

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV CHROMA_COLLECTION_NAME='books'

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "9000"]