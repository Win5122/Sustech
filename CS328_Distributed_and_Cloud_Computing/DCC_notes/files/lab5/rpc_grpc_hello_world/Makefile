setup-python:
	python -m pip install -r requirements.txt

gen-proto: setup-python
	python -m grpc_tools.protoc -I./ --python_out=. --pyi_out=. --grpc_python_out=. assistant.proto
