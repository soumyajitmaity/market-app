FROM python:3.10.6

WORKDIR /app

COPY ./r.txt /app

RUN pip install --no-cache-dir --upgrade -r r.txt

COPY ./src/ /app
RUN pytest 
CMD ["python3", "-m", "flask", "run", "--host","0.0.0.0"]
