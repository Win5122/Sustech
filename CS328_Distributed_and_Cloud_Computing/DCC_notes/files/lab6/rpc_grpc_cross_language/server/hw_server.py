from concurrent import futures
import logging

import grpc
from assistant_pb2_grpc import AssistantServiceServicer, add_AssistantServiceServicer_to_server
from assistant_pb2 import GreetRequest, GreetResponse, MultRequest, MultResponse

class Assistant(AssistantServiceServicer):
  def GreetWithInfo(self, request: GreetRequest, context):
    msg = f'Hello {request.user_name} from {request.institution}!'
    return GreetResponse(message=msg)
  
  def Multiply(self, request: MultRequest, context):
    res = request.xin * request.yin
    return MultResponse(xin=request.xin, yin=request.yin, result=res)

def serve():
  port = '8082'
  # the server can handle 10 client requests concurrently
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  add_AssistantServiceServicer_to_server(Assistant(), server)
  # [::] specifies the listen on all ipv4/ipv6 addresses
  server.add_insecure_port('[::]:' + port)
  server.start()
  logging.info(f'Server started, listening on {port}')
  server.wait_for_termination()
  
if __name__ == '__main__':
  logging.basicConfig(level=logging.INFO)
  serve()
