FROM python:3.10-slim

RUN useradd -u 8877 --create-home userunner
ENV PATH="/home/userunner/.local/bin:$PATH"
USER userunner

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY --chown=userunner . /code/

EXPOSE 8080

CMD python /code/app/app.py
