FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen

COPY . .

ENV PORT=8000

EXPOSE 8000

CMD [ "uv","run","uvicorn","main:app","--host","0.0.0.0","--port","8000" ]