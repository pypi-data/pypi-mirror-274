from typing import Mapping, Protocol, TypedDict, Generic, Sequence, TypeVar, TypeAlias
from haskellian import Left, Either
from q.api import Queue, ReadQueue, WriteQueue, QueueError
from .specs import Pipeline, Workflow

A = TypeVar('A')
B = TypeVar('B')

class PipelineQueues(TypedDict, Generic[A, B]):
  Qin: ReadQueue[A]
  Qout: WriteQueue[B]

WorkflowQueues: TypeAlias = PipelineQueues | Mapping[str, 'WorkflowQueues']

class prejoin(WriteQueue[A], Generic[A]):
  def __init__(self, queues: Sequence[tuple[WriteQueue[A], Sequence[type[A]]]]):
    self.queues = queues

  async def push(self, key: str, value: A) -> Either[QueueError, None]:
    for q, types in self.queues:
      for t in types:
        if isinstance(value, t):
          return await q.push(key, value)
    return Left(QueueError(f'Invalid type {type(value).__name__} for {value}'))

class MakeQueue(Protocol):
  def __call__(self, id: Sequence[str], type: type[A]) -> Queue[A]:
    ...

def make_queues(
  workflow: Workflow,
  make_queue: MakeQueue,
  output_queue: WriteQueue
) -> WorkflowQueues:
  
  def _input_queue(task: Pipeline, prefix: tuple[str, ...]) -> tuple[Queue[A], Sequence[type[A]]]:
    match task:
      case Workflow():
        return _input_queue(task.pipelines[task.input_task], prefix + (task.input_task,))
      case Pipeline():
        return make_queue(prefix, task.input_type), [task.input_type]
      
  def _make_queues(task: Pipeline, prefix: tuple[str, ...], output_queue: WriteQueue) -> WorkflowQueues:
    match task:
      case Workflow():
        queues = {
          id: _make_queues(
            pipe, prefix + (id,),
            prejoin([
              ((output_queue, task.output_types) if id == 'output' else _input_queue(task.pipelines[id], prefix + (id,)))
              for id in task.next_tasks(pipe.output_types)
            ])
          )
          for id, pipe in task.pipelines.items()
        }
        return queues | { 'Qin': queues[task.input_task]['Qin'] } # type: ignore
      case Pipeline():
        return PipelineQueues(
          Qin=_input_queue(task, prefix)[0],
          Qout=output_queue
        )

  return _make_queues(workflow, (), output_queue)
