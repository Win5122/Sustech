'''
TASK: refactor this local procedure `report_stats` into a gRPC procedure. This procedure belongs to a
gRPC service called `AssistantService`. Then, use a gRPC client to test the remote procedure.

Hints:
1. Python `float` is FP64.
2. For array/list types, check: https://protobuf.dev/programming-guides/proto3/#field-labels
'''

def report_stats(user_name: str, institution: str, values: list[float]) -> tuple[float, float, float, str]:
  '''
  report_add calculates the min, max, avg of the provided numeric values, and gives a response
  in natural language.
  '''
  val_min = min(values)
  val_max = max(values)
  val_avg = sum(values) / len(values)
  resp_msg = f'Hi {user_name} from {institution}! For {values}: min={val_min}; max={val_max}, avg={val_avg}'
  return val_min, val_max, val_avg, resp_msg

if __name__ == '__main__':
  # (-3, 5, 0.2, 'Hi Peter S from SUSTech! For [1, 1.5, 2, 2.5, 5, -1, -1.5, -2, -2.5, -3]: min=-3; max=5, avg=0.2')
  print(report_stats(
    user_name='Peter S', institution='SUSTech',
    values=[1, 1.5, 2, 2.5, 5, -1, -1.5, -2, -2.5, -3],
  ))
