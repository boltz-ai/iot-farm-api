# pull official base image
FROM python:3.8-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE 1
ARG DEBIAN_FRONTEND=noninteractive

# set work directory
ENV APP_DIR /iot_farm
RUN mkdir -p $APP_DIR
WORKDIR $APP_DIR

# Add repository
RUN echo "deb http://apt.postgresql.org/pub/repos/apt/ buster-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add -
RUN apt-get update
RUN apt-get install -y build-essential netcat gcc musl-dev libpq-dev libpq5
RUN apt autoremove

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt $APP_DIR
RUN pip install --no-cache-dir -r requirements.txt

# copy project
COPY ./entrypoint.sh /usr/src
COPY ./iot_farm $APP_DIR

# run entrypoint.sh
ENTRYPOINT ["/usr/src/entrypoint.sh"]
