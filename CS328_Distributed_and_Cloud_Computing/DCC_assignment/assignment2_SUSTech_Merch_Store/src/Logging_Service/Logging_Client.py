import time

import grpc
from visualdl.server.api import result

from Logging_Service_pb2 import LoggingRequest
from Logging_Service_pb2_grpc import LoggingServiceStub


def run():
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = LoggingServiceStub(channel)
        message1 = LoggingRequest(message='message1', timestamp="1")
        message2 = LoggingRequest(message='message2', timestamp="2")
        message3 = LoggingRequest(message='message3', timestamp="3")

        def generate_logs():
            yield message1
            yield message2
            yield message3

        try:
            response = stub.LoggingService(generate_logs())
            print(response)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    run()
