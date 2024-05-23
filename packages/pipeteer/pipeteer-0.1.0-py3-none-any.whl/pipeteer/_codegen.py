# BEGIN
from typing import Unpack, TypedDict
from dataclasses import dataclass
from q.api import WriteQueue
from pipeteer import MakeQueue, make_queues as _make_queues, PipelineQueues
# UNCOMMENT from MODULE import MOD_IMPORTS

class SUBFLOW_CLASS: # DELETE
  Queues = int # DELETE
# DELETE
INPUTS = str; OUTPUTS = str; INPUT_TYPE = str; OUTPUT_TYPE = str # DELETE
class WORKFLOW:
  class Queues(TypedDict):
    Qin: WriteQueue[INPUT_TYPE]
    # LOOP SUBFLOW_ID SUBFLOW_CLASS
    SUBFLOW_ID: SUBFLOW_CLASS.Queues
    # END
    # LOOP PIPELINE_ID INPUTS OUTPUTS
    PIPELINE_ID: PipelineQueues[INPUTS, OUTPUTS]
    # END

  @staticmethod
  def make_queues(make_queue: MakeQueue, output_queue: WriteQueue[OUTPUT_TYPE]) -> Queues:
    VARIABLE = ... # type: ignore # DELETE
    return _make_queues(VARIABLE, make_queue, output_queue) # type: ignore
  
  @staticmethod
  def artifacts(**queues: Unpack['WORKFLOW.Queues']):
    ...
    
# END
from typing import Sequence
from haskellian import Thunk
from templang import parse
from pipeteer import Workflow

source = Thunk(lambda: open(__file__).read())

def union_type(types: Sequence[type]):
  return  ' | '.join(t.__name__ for t in types)

def codegen(workflow: Workflow, *, variable: str, module: str, classname: str) -> str:

  translations = {
    'MODULE': module,
    'WORKFLOW': classname,
    'VARIABLE': variable,
    'INPUT_TYPE': workflow.input_type.__name__,
    'OUTPUT_TYPE': union_type(workflow.output_types),
    'MOD_IMPORTS': '*',
    'SUBFLOW_CLASS': [],
    'SUBFLOW_ID': [],
    'PIPELINE_CLASS': [],
    'PIPELINE_ID': [],
    'INPUTS': [],
    'OUTPUTS': [],
  }

  for id, pipe in workflow.pipelines.items():
    match pipe:
      case Workflow():
        translations['SUBFLOW_CLASS'].append(id.title())
        translations['SUBFLOW_ID'].append(id)
      case _:
        translations['INPUTS'].append(pipe.input_type.__name__)
        translations['OUTPUTS'].append(union_type(pipe.output_types))
        translations['PIPELINE_CLASS'].append(id.title())
        translations['PIPELINE_ID'].append(id)

  return parse(source(), translations)
  