# gRPC - A Cross-Language Example
This part implements a Go gRPC client and a Python gRPC server, demonstrating the cross-language capability of Protobuf.

## Requirements
- Check `requirements.txt` for Python requirements. Set up with `python -m pip install -r requirements.txt`.
- For Go requirements, check the following content.

First, install the relevant libraries listed here: https://grpc.io/docs/languages/go/quickstart/#prerequisites. It is an **IMPORTANT** step to add the `bin` folder where `go install` happens into `$PATH`.

```bash
sudo apt update; sudo apt install -y protobuf-compiler
go install google.golang.org/protobuf/cmd/protoc-gen-go@latest
go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@latest
export PATH="$PATH:$(go env GOPATH)/bin"  # add to .bashrc to take effect permenantly
```

After generating the code stub for Go, set up with `go mod tidy` in the `client/` directory. Check `go.mod` in the `client/` directory for Go requirements. They are automatically managed and are added on demand according to our code implementation.

For beginners to Go, check this official tutorial: https://go.dev/doc/tutorial/getting-started.

## Write a `.proto` File
Check the `assistant.proto` file. It includes an Assistant Service provided by the server, in which there are 2 remote procedures defined. The request and response messages for the remote procedures are also defined at the bottom of the file.

More info on Proto Best Practices is provided here: https://protobuf.dev/programming-guides/dos-donts/.

The **IMPORTANT** thing for this part is that we need to set the `go_package` option for Go to deliver the generated code to the corresponding Go package. Here we write:
```proto
option go_package = "./pb";
```
This means `protoc` will generate the code to the `pb` package in the destination directory `client/`.

## Generate Message Classes, Client Stubs, and Service Template
### Python
To generate for Python, run:
```bash
python -m grpc_tools.protoc -I./ --python_out=./server/ --pyi_out=./server/ --grpc_python_out=./server/ assistant.proto
```

- `protoc` is already installed in `grpc_tools`.
- `-I` specifies `./` as the path to import the proto files.
- The following 3 flags look similar but have actually different purposes:
  - `--python_out` specifies where to generate the Python **message** classes. It will create `*_pb2.py` files for specifically the **messages** defined in the proto files. Required even when gRPC is not used.
  - `--pyi_out` specifies where to generate Python **type hinting** `.pyi` files. It will create `*_pb2.pyi` files for Python IDEs to perform type suggestions and error checking. It is optional but provides better coding experience.
  - `--grpc_python_out` specifies where to generate **gRPC service** templates and client stubs for the defined services in the proto files. It will create `*_pb2_grpc.py` files that handle the gRPC communication logic between client and server. It is optional for users using Protobuf without gRPC.

As a result, 3 files will be generated:

1. `assistant_pb2.py` for the Python message classes.
2. `assistant_pb2.pyi` for the Python IDEs to support type hinting.
3. `assistant_pb2_grpc.py` for the gRPC service stubs.

### Go
To generate for Go, run:
```bash
protoc -I=./ --go_out=./client/ --go-grpc_out=./client/ assistant.proto
```
- `protoc` is already installed by `apt install`.
- `-I` specifies `./` as the path to import the proto files.
- `--go_out` specifies where to generate the Go **message** classes. It will create `*.pb.go` files for specifically the **messages** defined in the proto files. Required even when gRPC is not used.
- `--go-grpc_out` specifies where to generate **gRPC service** templates and client stubs for the defined services in the proto files. It will create `*_grpc.pb.go` files that handle the gRPC communication logic between client and server. It is optional for users using Protobuf without gRPC.

As a result, 2 files will be generated:

1. `assistant.pb.go` for the Go message classes.
2. `assistant_grpc.pb.go` for the gRPC service templates and client stubs.

These files will be generated in the `client/pb/` folder, marked as `package pb` in the `.go` files.

Now we examine the files a bit.

#### Generated Message Classes
The official documentation is provided here: https://protobuf.dev/getting-started/gotutorial/#protobuf-api.

Check the `assistant.pb.go` file. First some version checking is performed. Then, the four messages are constructed into `struct` types with a set of relevant functions like field getters/setters.

The rest of the part defines and initializes the file descriptor for the proto file. The `Exporter` function is crucial for the reflection mechanism within the Protobuf framework in Go. It provides a way to retrieve internal properties of a message and supports dynamic field access by using an index parameter `i`.

#### Generated gRPC Client Stubs and Service Templates
The official documentation is provided here: https://grpc.io/docs/languages/go/generated-code/.

Check the `assistant_grpc.pb.go` file.

The client stub is provided by the `NewAssistantServiceClient` function, where a `assistantServiceClient` implementing the `AssistantServiceClient` interface is created.

The server template follows the `AssistantServiceServer` interface. An unimplemented server struct type `UnimplementedAssistantServiceServer` is performed to provide a base implementation. The `UnsafeAssistantServiceServer` is used for compatibility and we will skip for this part.

Below, the `RegisterAssistantServiceServer` function registers the service implementation with the gRPC server. Finally, the service procedure handler functions are specified and assigned to the service descriptor `AssistantService_ServiceDesc`.

## Implement and Run the Python gRPC Server
Check the `server/hw_server.py` file where an `Assistant` implements the registered procedures from `AssistantServiceServicer`. In the serving function, the gRPC server uses a thread pool executor to enable concurrent request handling. The server is served at port=`8082` via:
```bash
python server/hw_server.py
```

## Implement and Run the gRPC Client
Check the `client/hw_client.go` file. An insecure channel (without SSL/TLS) is constructed between the client and the server. This channel is then used to construct a client stub and the following remote procedure calls can be made by the stub. To run the client:
```bash
cd client/  # skip if already in the directory
go run hw_client.go
```

Optionally, you might be able to execute the `./client/hw_client` file directory without a Go environment. This file is generated via `go build -o hw_client` from the `client/` directory.

A sample output is as follows:
```text
> Greet: Hello Assistant?
Client received:
message:"Hello Peter from SUSTech!"
> Mult: Requesting a multiplication task
> Client received:
xin:3.5 yin:5 result:17.5
```
