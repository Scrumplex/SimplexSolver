FROM python:3.10

RUN pip install pipenv
RUN apt-get update \
  && apt-get install -y pandoc texlive-latex-recommended

WORKDIR /app

COPY Pipfile Pipfile.lock ./

RUN pipenv install --system --deploy

COPY . ./

EXPOSE 8000
VOLUME /app/output

ENTRYPOINT ["/usr/local/bin/uvicorn", "--host", "0.0.0.0", "main:app"]

