setup-python:
	python -m pip install -r requirements.txt

gen-only-proto: setup-python
	python -m grpc_tools.protoc -I./ --python_out=. --pyi_out=. assistant.proto
