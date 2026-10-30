PYTHON ?= python3
IN ?= data/tickets_valid.jsonl
OUT ?= pred.jsonl

.PHONY: run predict

run:
	$(PYTHON) -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

predict:
	$(PYTHON) scripts/predict.py --input $(IN) --output $(OUT)
