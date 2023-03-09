FROM python:3.10 as base
LABEL maintainer="Espoir Murhabazi<espoir.mur [] gmail>"


# Never prompt the user for choices on installation/configuration of packages
ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED=1 \
    PORT=9000 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 


FROM base AS python-deps
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential\
        software-properties-common

RUN python -m venv /opt/venv
# Make sure we use the virtualenv:
ENV PATH="/opt/venv/bin:$PATH"

# Install pip
COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt



FROM base AS runtime
# copy nltk data
COPY --from=python-deps /opt/venv /opt/venv


RUN useradd --create-home masakhane
RUN usermod -aG sudo masakhane
RUN mkdir /home/masakhane/translation_app/
ENV WORKING_DIR=/home/masakhane/translation_app/
ENV PATH="${WORKING_DIR}:$PATH"
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH="/opt/venv/bin:$PYTHONPATH"
ENV PYTHONPATH="${PYTHONPATH}:${WORKING_DIR}"

ENV MODEL_NAME model_handlers.OptimizedM100Model

ENV SERVICE_TYPE MODEL

COPY model_handlers.py ${WORKING_DIR}
WORKDIR ${WORKING_DIR}
RUN chown -R masakhane:masakhane ${WORKING_DIR}
RUN chmod -R 777 ${WORKING_DIR}
USER masakhane
EXPOSE 9000 5000

CMD exec seldon-core-microservice $MODEL_NAME --service-type $SERVICE_TYPE
