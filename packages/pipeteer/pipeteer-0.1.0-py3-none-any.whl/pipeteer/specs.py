from typing import Mapping, Generic, TypeVar, Sequence, Union
import os

A = TypeVar('A', covariant=True)
B = TypeVar('B', covariant=True)

class Pipeline(Generic[A, B]):
  def __init__(self, input_type: type[A], *output_types: type[B]):
    self.input_type = input_type
    self.output_types: Sequence[type] = output_types

  @property
  def output_type(self) -> type[B]:
    return Union[*self.output_types] # type: ignore

class Workflow(Pipeline[A, B], Generic[A, B]):
  input_task: str
  pipelines: Mapping[str, Pipeline]

  def __init__(self, input_task: str, *output_types: type[B], pipelines: Mapping[str, Pipeline]):
    self.input_task = input_task
    self.output_types = output_types
    self.pipelines = pipelines

  @property
  def input_type(self):
    return self.pipelines[self.input_task].input_type
  
  def next_tasks(self, output_types: Sequence[type]) -> Sequence[str]:
    tasks = [
      task for task, pipeline in self.pipelines.items()
        if pipeline.input_type in output_types
    ]
    if set(output_types) & set(self.output_types):
      tasks.append('output')
    return tasks
  
  def codegen(
    self, __file__: str, *,
    variable: str = 'workflow',
    classname: str = 'Workflow',
  ):
    folder, file = os.path.split(__file__)
    module, py = os.path.splitext(file)
    outfile = os.path.join(folder, f'{module}_codegen{py}')

    from ._codegen import codegen
    source = codegen(self, variable=variable, module=f'.{module}', classname=classname)

    try:
      with open(outfile, 'x') as f:
        f.write(source)
    except FileExistsError:
      print('Codegen file already exists. Delete it to regenerate. File:', outfile)