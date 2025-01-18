# gRPC - Hello World
A Hello World example for gRPC.

## Requirements
- Check `requirements.txt` for Python requirements. Set up with `python -m pip install -r requirements.txt`.

## Write a `.proto` File
Check the `assistant.proto` file. It includes an Assistant Service provided by the server, in which there are 2 remote procedures defined. The request and response messages for the remote procedures are also defined at the bottom of the file.

More info on Proto Best Practices is provided here: https://protobuf.dev/programming-guides/dos-donts/.

## Generate Message Classes and Client Stub
Run:

```bash
python -m grpc_tools.protoc -I./ --python_out=. --pyi_out=. --grpc_python_out=. assistant.proto
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

Now we examine the three files a bit.

### Generated Message Classes
The official documentation is provided here: https://protobuf.dev/getting-started/pythontutorial/#protobuf-api.

In the `assistant_pb2.py` file, Protobuf messages are **dynamically** set up with serialization/deserialization features.

- The `descriptor` is used to describe the structure of the messaages and services.
- The `symbol_database` manages the symbols (e.g., message and enum definitions) created by Protobuf.
- The `builder` dynamically buildes message and enum classes using the information in the Protobuf descriptor.

The top code checks the version of the Protobuf runtime.

`_sym_db = _symbol_database.Default()` creates a default symbol database used to look up and register message and enum types at runtime.

The `DESCRIPTOR` stores the binary representation of the `.proto` file. This binary data is added to the descriptor pool - a global registry that holds information about all registered descriptors:
```python
DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'...')
```

Then, the builder will build the message and enum descriptors (not actual Python classes) from the `DESCRIPTOR`. The built descriptors are then used to build the top-level Python classes for the messages and services:
```python
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'assistant_pb2', _globals)
```

Finally, the starting and ending byte positions in the serialized descriptor for each message and service are specified:
```python
_globals['_GREETREQUEST']._serialized_start=19
_globals['_GREETREQUEST']._serialized_end=73
...
```

This dynamic approach is specific for Python. Other programming languages like Go still generate the message and enum classes statically.

### Generated Type Hinting Files
Since message classes are dynamically generated in Python, `.pyi` files are generated to tell Python IDEs these classes will be there at runtime.

### Generated gRPC Service Templates and Client Stubs
The official documentation is provided here: https://grpc.io/docs/languages/python/generated-code/#code-elements.

In the `assistant_pb2_grpc.py` file, version checking is performed at the top:
```python
...
if _version_not_supported:
    raise RuntimeError(...)
```
The `RuntimeError` will be raised if the installed gRPC library version is lower than that for the generation.

#### Client Stub
The `AssistantServiceStub` class represents the **client stub** for the `AssistantService` we define. In the initialization, it uses [`channel.unary_unary`](https://grpc.github.io/grpc/python/grpc.html#grpc.Channel.unary_unary) to create a [`grpc.UnaryUnaryMultiCallable`](https://grpc.github.io/grpc/python/grpc.html#grpc.UnaryUnaryMultiCallable) that is able to handle method calling and serialization/deserialization:
```python
self.GreetWithInfo = channel.unary_unary(
  '/AssistantService/GreetWithInfo',
  request_serializer=assistant__pb2.GreetRequest.SerializeToString,
  response_deserializer=assistant__pb2.GreetResponse.FromString,
  _registered_method=True)
```
Note that gRPC supports streaming requests/reponses from the clients/servers. When streaming is used, the term `unary` will be changed to the term `stream` accordingly.

#### Service Base Class for Server Implementation

The `AssistantServiceServicer` class defines the **server-side implementation** of the service methods:
```python
def GreetWithInfo(self, request, context):
  """Constructs a greeting message based on the given information of the user.
  """
  context.set_code(grpc.StatusCode.UNIMPLEMENTED)
  context.set_details('Method not implemented!')
  raise NotImplementedError('Method not implemented!')
```
It serves as a base class for our future implementation. In our actual server code, we will inherit this class and provide the actual implementation. Note that the `context` field is typically used to pass additional info like errors back to the clients (similar to returning HTTP response status code + additional message in RESTful API).

The `add_AssistantServiceServicer_to_server` function adds the implemented servicer to the gRPC server instance:
```python
rpc_method_handlers = {
  'GreetWithInfo': grpc.unary_unary_rpc_method_handler(
    servicer.GreetWithInfo,
    request_deserializer=assistant__pb2.GreetRequest.FromString,
    response_serializer=assistant__pb2.GreetResponse.SerializeToString,
  ),
  ...
}
generic_handler = grpc.method_handlers_generic_handler('AssistantService', rpc_method_handlers)
```
The method handlers are defined similarly to the one in the client stub. These handlers will be utilized by the gRPC server to handle a specific procedure/function. The generic handler is used to intercept any RPC method request dynamically and handle it with extra implementation logic. This handler usually serves middleware, logging, proxying, or dynamic dispatching logic.

#### High-level Service Class
The `AssistantService` class provides static methods for making RPC calls without needing to create a client stub manually. This class is still under experimental phase, and it does not follow the traditional RPC design, so we do not use it for this module.

## Implement and Run the gRPC Server
Check the `hw_server.py` file where an `Assistant` implements the registered procedures from `AssistantServiceServicer`. In the serving function, the gRPC server uses a thread pool executor to enable concurrent request handling. The server is served at port=`8082` via:
```bash
python hw_server.py
```

## Implement and Run the gRPC Client
Check the `hw_client.py` file. An insecure channel (without SSL/TLS) is constructed between the client and the server. This channel is then used to construct a client stub and the following remote procedure calls can be made by the stub. To run the client:
```bash
python hw_client.py
```

A sample output is as follows:
```text
> Greet: Hello Assistant?
> Client received:
message: "Hello Peter from SUSTech!"

> Mult: Requesting a multiplication task
> Client received:
xin: 3.5
yin: 5
result: 17.5
```
