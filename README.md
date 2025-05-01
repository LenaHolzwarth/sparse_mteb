# Sparse MTEB
Adapting MTEB (massive text embedding benchmark) to work with sparse embedding methods, such as TF-IDF 

Original MTEB: https://github.com/embeddings-benchmark/mteb

## Folder structure
This acts as an overview of the folders and files of MTEB

- `abstasks`
    - abstract classes, one superclass (`AbsTask.py`) and one subclass for each task type (e.g. `AbsTaskClustering.py`)
    - `TaskMetadata.py`: Metadata class for tasks -> necessary for querying task properties
- `benchmarks`
    - defines the `Benchmark` object and defines the benchmarks that are queriable by MTEB by enlisting their component tasks
- `evaluation`
    - `Evaluators`: one for each task type, the evaluator performs the actual task, computes the metrics and returns the results
    - `MTEB.py`: defines the Evaluation pipeline for an MTEB query. First file getting called during MTEB processing, the `MTEB.run()` function is defined here
- `leaderboard`
- `load_results`: syntax for loading pre-existing results, s.t. metrics aren't computed twice
- `models`: defines models in a way that they are compatible to MTEB. `instructions.py` gives the prompt version of each task for prompt-based models
- `tasks`: contains class definitions with metadata information for all tasks, grouped by task type and language
- `cli.py`: defines command line interface with instructions on how to call MTEB
- `encoder_interface`: defines the encoder class that needs to be instanciated by all models
- `model_meta.py`: metadata class for models
- `overview.py`: functions used to get an overview of MTEB (e.g. list all tasks)
- `task_aggregation.py`: function to compute aggregate scores of multiple task runs or different tasks of the same type
- `task_selection.py`: helper functions


### Function path for one task call
This gives an example of which files and functions are traversed during a `MTEB.run` call, using the example of STS15
```
task = mteb.get_tasks(["STS15"])
evaluation = mteb.MTEB(task)
results = evaluation.run(model)
```
- `evaluators/MTEB.py`:
    - `MTEB.run()`
        - create model meta
        - create or call output folder
        - iterate through selected tasks (here, only STS15)
        - check if task results already exist
        - create task_results dict
        - call `MTEB.run_eval()`
        - save & return results
    - `MTEB.run_eval()`
        - call `AbsTask.evaluate()`
- `abstasks/AbsTask.py`:
    - `AbsTask.evaluate()`
        - call `AbsTask.load_data()` (loads & transforms dataset, each task defines its own transform function in its task class definition in the task folder)
        - create scores dict
        - get scores for each data subset: `AbsTask.evaluate_subset()` (`evaluate_subset()` is not defined for the AbsTask superclass, only for the inheriting classes)
        - return scores dict
- `abstasks/AbsTaskSTS.py`:
    - `AbsTaskSTS.evaluate_subset()`
        - create instance of evaluator for relevant task type: `STSEvaluator()`
        - call `evaluator()` to perform the task
        - return scores
- `evaluation/evaluators/STSEvaluator.py`:
    - `__call__()`
        - this is where the actual task is performed and the scores computed and returned

### Files changed for TF-IDF compatibility
The issue with TF-IDF embeddings is that they have a variable embedding size, depending on the document to be embedded.
The original MTEB is only constructed for models with fixed embedding sizes. 
To work around this, we create the vocabulary that underlies the TF-IDF embeddings before the actual embedding call.
We can then pass the fixed vocabulary to the embedding call, such that each embedding call for one task uses the same vocab and thus creates embeddings of the same size.

For most tasks, this means that the `get_vocab` call is in the task-specific AbsTask file (e.g. AbsTaskSTS for STS tasks), which is after the dataset is loaded, but before the individual dataset entries get embedded.
This is the case for Classification, Clustering, Paiclassification, Reranking, Retrieval and STS. 
The other tasks were not adapted for TF-IDF.

The `get_vocab`function is in the evaluation/evaluators folder. 


