FROM python:3.10 as requirements-stage 

WORKDIR /tmp

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
# RUN poetry add MoviePy

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10

WORKDIR /app/

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
# RUN 
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN apt-get update && apt-get -y install libgl1-mesa-glx
# RUN apt-get -y install libgl1-mesa-glx

COPY . /app/


CMD ["fastapi", "dev", "./src/main.py", "--host", "0.0.0.0", "--port", "???"]