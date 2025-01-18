import grpc
from assistant_pb2 import GreetRequest, MultRequest
from assistant_pb2_grpc import AssistantServiceStub

def run():
  with grpc.insecure_channel('localhost:8082') as channel:
    stub = AssistantServiceStub(channel)
    # Greeting
    print('> Greet: Hello Assistant?')
    res = stub.GreetWithInfo(GreetRequest(user_name='Peter', institution='SUSTech'))
    print(f'> Client received:\n{res}')
    # Multiplication
    print('> Mult: Requesting a multiplication task')
    res = stub.Multiply(MultRequest(xin=3.5, yin=5))
    print(f'> Client received:\n{res}')
  
if __name__ == '__main__':
  run()
