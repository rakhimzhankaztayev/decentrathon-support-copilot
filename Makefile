.PHONY: predict

predict:
	python3 -m scripts.predict data/tickets_valid.jsonl -o predictions.jsonl
