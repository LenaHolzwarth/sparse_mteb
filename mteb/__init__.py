from __future__ import annotations

from importlib.metadata import version

from .benchmarks.benchmarks import (
    MTEB_MAIN_EN,
    #MTEB_MAIN_RU,
    #MTEB_RETRIEVAL_LAW,
    #MTEB_RETRIEVAL_WITH_INSTRUCTIONS,
    #CoIR,
)
from .evaluation import *

from .load_results import BenchmarkResults, load_results
from .models import get_model, get_model_meta  #, get_model_metas
from .overview import TASKS_REGISTRY, get_task, get_tasks

#from .benchmarks.benchmarks import Benchmark
from .benchmarks.get_benchmark import get_benchmark, get_benchmarks

__version__ = version("mteb")  # fetch version from install metadata


__all__ = [
    "MTEB_MAIN_EN",
    "MTEB_MAIN_RU",
    "MTEB_RETRIEVAL_LAW",
    "MTEB_RETRIEVAL_WITH_INSTRUCTIONS",
    "CoIR",
    "TASKS_REGISTRY",
    "get_tasks",
    "get_task",
    "get_model",
    "get_model_meta",
    "get_model_metas",  
    "load_results",
    "Benchmark",
    "get_benchmark",
    "get_benchmarks",
    "BenchmarkResults",
]
