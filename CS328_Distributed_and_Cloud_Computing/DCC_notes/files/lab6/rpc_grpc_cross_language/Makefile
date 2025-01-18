SHELL := /bin/bash

go_out_dir=./client/
python_out_dir=./server/

init-go:
	cd client; go mod init dncc/grpc

setup-go:
	apt install -y protobuf-compiler
	go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
	go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
	@echo add \`export PATH=\"\$$PATH:\$$\(go env GOPATH\)/bin\"\` to your .bashrc

gen-proto-go: setup-go
	protoc -I=./ --go_out=${go_out_dir} --go-grpc_out=${go_out_dir} assistant.proto
	cd client; go mod tidy

build-go-client: gen-proto-go
	cd client; go build -o hw_client

setup-python:
	python -m pip install -r requirements.txt

gen-proto-python: setup-python
	python -m grpc_tools.protoc -I./ --python_out=${python_out_dir} --pyi_out=${python_out_dir} --grpc_python_out=${python_out_dir} assistant.proto
