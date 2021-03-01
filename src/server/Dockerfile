FROM python:3.7
LABEL maintainer="Salomon KABONGO <salomon@aims.ac.za>"

WORKDIR /app

ADD requirements.txt /app

# Install requirements
RUN \
  pip install --upgrade pip && \
  pip install --no-cache -r requirements.txt && \
  rm -rf ~/.cache/


# Add the rest of the code to the app folder
ADD . /app

ADD ../../data/external /app
ADD ../../models/joeynmt /app

EXPOSE 5000

# Apply the migration to the database and run the application
CMD flask db init && flask db upgrade && python app.py
