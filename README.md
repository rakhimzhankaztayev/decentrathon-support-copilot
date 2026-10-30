# Grand Support Copilot

Локальный baseline для классификации и подготовки ответов на обращения в поддержку.

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

API: `POST /triage`, проверка состояния: `GET /health`.

## Пакетный инференс

```bash
make predict
```

Входной формат — JSONL с полями `id`, `subject`, `text`. Результат записывается в `predictions.jsonl`; команда также печатает число обработанных тикетов, время и скорость.

## Данные

Файлы в `data/` считаются локальными и исключены из Git. В репозитории оставлены небольшие JSON-примеры для локального запуска; реальные обучающие файлы (`tickets_train.jsonl.gz`) добавляются отдельно.
