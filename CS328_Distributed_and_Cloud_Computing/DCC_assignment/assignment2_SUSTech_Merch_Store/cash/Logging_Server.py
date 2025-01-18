import asyncio
import logging
from typing import Iterator

import grpc
from confluent_kafka import Producer

from Logging_Service_pb2 import LoggingRequest, LoggingResponse
from Logging_Service_pb2_grpc import LoggingServiceServicer, add_LoggingServiceServicer_to_server

# Kafka Producer configuration
producer = Producer({'bootstrap.servers': 'localhost:9093'})
topic = 'log-channel'


class LoggingService(LoggingServiceServicer):
    def __init__(self) -> None:
        super().__init__()

    async def LoggingService(self, request_iterator: Iterator[LoggingRequest], context):
        # greeting message
        logging.info('Received logging request.')

        # Iterate through incoming request stream
        try:
            async for request in request_iterator:
                try:
                    msg = f'Received message: {request.message} sent at time = {request.timestamp}'
                    producer.produce(topic, msg.encode('utf-8'))
                    producer.poll(0)
                    logging.info(f"Produced message: {msg}")
                    await asyncio.sleep(1)
                except KeyboardInterrupt:
                    return LoggingResponse(message='Logging service stopped.')
                except Exception as e:
                    return LoggingResponse(message=f'Error producing message: {e}')
                finally:
                    producer.flush()
        except Exception as e:
            return LoggingResponse(message=f'Error producing message: {e}')
        finally:
            return LoggingResponse(message='Logging service stopped.')


# Graceful shutdown for gRPC aio server
_cleanup_coroutines = []


async def serve():
    port = '50051'
    # aio: gRPC's Asynchronous Python API - non-blocking I/O operations
    server = grpc.aio.server()  # no need for ThreadPoolExecutor in asyncio
    add_LoggingServiceServicer_to_server(LoggingService(), server)
    server.add_insecure_port(f'[::]:{port}')
    # wait for the server start
    await server.start()
    logging.info(f'Server started on port {port}')

    async def graceful_shutdown():
        logging.info('Server gracefully shutting down...')
        await server.stop(3)
        logging.info('Server gracefully shut down.')

    _cleanup_coroutines.append(graceful_shutdown())

    # wait for termination asynchronously
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
