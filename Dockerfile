FROM tiangolo/uvicorn-gunicorn:python3.11

COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

# Install playwright and Chromium
RUN playwright install chromium

EXPOSE $PORT

CMD uvicorn main:app --host 0.0.0.0 --port $PORT --reload 