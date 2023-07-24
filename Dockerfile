FROM python:3.10

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt update && apt install -y --no-install-recommends \
        git \
        curl \
        wget \
        sqlite3

WORKDIR /my_project

# ENV PYTHONPATH=${PYTHONPATH}/home/${USERNAME}/app

## Pip dependencies
# Upgrade pip
RUN pip install --upgrade pip

# Install production dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD [ "tail", "-f", "/dev/null" ]