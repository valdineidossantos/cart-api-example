FROM python:3.10.4-slim-buster

RUN apt-get update && apt-get -y upgrade && \
    apt-get install git python3-psutil libssl-dev gcc g++ curl jq make -y wait-for-it \
    && apt-get clean && rm -rf /var/lib/apt/lists/*



RUN pip install poetry==1.1.14
RUN pip install setuptools==59.6.0



RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

RUN poetry install

COPY . /app/src/


#RUN pip install --use-feature=in-tree-build  .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
