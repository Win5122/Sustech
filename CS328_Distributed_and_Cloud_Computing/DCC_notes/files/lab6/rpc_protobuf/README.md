# Protobuf as a Data Serialization Mechanism
Protocol Buffers are a language-neutral, platform-neutral extensible mechanism for serializing structured data. This part explores how messages can be serialized for RPC, including text-based via JSON and binary-based via Protobuf.

**`x_main_reduced.py` is the file provided to students. It includes a mini-task to implement decoding of the `MultResponse` message.**

The official documentation of Protobuf with Python can be found here: https://protobuf.dev/getting-started/pythontutorial/.

## Requirements
- Check `requirements.txt` for Python requirements. Set up with `python -m pip install -r requirements.txt`.

## Write a `.proto` File
Check the `assistant.proto` file. It includes an Assistant Service provided by the server, in which there are 2 remote procedures defined. The request and response messages for the remote procedures are also defined at the bottom of the file.

More info on Proto Best Practices is provided here: https://protobuf.dev/programming-guides/dos-donts/.

## Generate Message Classes
Run:
```bash
python -m grpc_tools.protoc -I./ --python_out=. --pyi_out=. assistant.proto
```
- `protoc` is already installed in `grpc_tools`.
- `-I` specifies `./` as the path to import the proto files.
- `--python_out` specifies where to generate the Python **message** classes. It will create `*_pb2.py` files for specifically the **messages** defined in the proto files. Required even when gRPC is not used.
- `--pyi_out` specifies where to generate Python **type hinting** `.pyi` files. It will create `*_pb2.pyi` files for Python IDEs to perform type suggestions and error checking. It is optional but provides better coding experience.

For more information/options on `protoc`, check the Hello World part.

## Play with Serialization
In the `main.py` file, there are two verification code snippets for reference:
1. `serialize_and_deserialize()` verifies that:
    1. Protobuf supports easy serialization and deserialization functions to implement our own gRPC, if necessary.
    2. Protobuf uses a specific binary encoding scheme - we will explore a bit how our messages are encoded behind the scene, via implementing `try_decode_proto_binary(binary_str)`.
2. `compare_with_json()` compares the serialization result between JSON and Protobuf, showing that Protobuf provides much lighter payload.

To run the python code, simply:
```bash
python main.py
```

Below is a sample output for reference:
```text
serialize_and_deserialize
> Initial Message:
user_name: "Peter"
institution: "SUSTech"

> After Serialization: b'\n\x05Peter\x12\x07SUSTech'
>> Binary form: 00001010 00000101 01010000 01100101 01110100 01100101 01110010 00010010 00000111 01010011 01010101 01010011 01010100 01100101 01100011 01101000
>> Hex Representation: 0a 05 50 65 74 65 72 12 07 53 55 53 54 65 63 68
>>> Trying to decode the serialized message...
-----------------------------------------------------------------------
>>> Record: {'field_number': 1, 'wire_type': 2, 'wire_type_name': 'LEN', 'length': 5, 'payload': 'Peter'}
>>> Record: {'field_number': 2, 'wire_type': 2, 'wire_type_name': 'LEN', 'length': 7, 'payload': 'SUSTech'}
>>> Final Result:
{1: 'Peter', 2: 'SUSTech'}
-----------------------------------------------------------------------
> Deserialized Message:
user_name: "Peter"
institution: "SUSTech"


compare_with_json
> JSON serialized into 48 bytes: b'{"user_name": "Peter", "institution": "SUSTech"}'
> Protobuf serialized into 16 bytes: b'\n\x05Peter\x12\x07SUSTech'
```
