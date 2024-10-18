FROM python:3.9

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

#ARG DB_CONN
#ENV DB_CONN ${DB_CONN}

ARG TG_TOKEN
ENV TG_TOKEN ${TG_TOKEN}

ENTRYPOINT ["python3", "main.py"]