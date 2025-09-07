.PHONY: demo
demo:
	uvicorn mocks.server:app --port 4010 --reload & echo $$! > .mock.pid
	python -m aegisapi.cli plan --spec examples/openapi_v1.yaml --base-url http://localhost:4010
	python -m aegisapi.cli gen  --spec examples/openapi_v1.yaml --out tests_generated
	python -m aegisapi.cli run  --tests tests_generated --spec examples/openapi_v1.yaml --base-url http://localhost:4010 --with-fuzz
	python -m aegisapi.cli report
