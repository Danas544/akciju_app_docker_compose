FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

WORKDIR /app/
ENV PYTHONPATH=/app
CMD [ "/start-reload.sh" ]