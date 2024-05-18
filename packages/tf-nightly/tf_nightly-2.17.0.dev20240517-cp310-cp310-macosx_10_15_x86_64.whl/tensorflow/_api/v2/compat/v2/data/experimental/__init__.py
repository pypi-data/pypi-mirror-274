# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.data.experimental namespace
"""

import sys as _sys

from tensorflow._api.v2.compat.v2.data.experimental import service
from tensorflow.python.data.experimental.ops.batching import dense_to_ragged_batch # line: 30
from tensorflow.python.data.experimental.ops.batching import dense_to_sparse_batch # line: 94
from tensorflow.python.data.experimental.ops.batching import map_and_batch # line: 210
from tensorflow.python.data.experimental.ops.batching import unbatch # line: 269
from tensorflow.python.data.experimental.ops.cardinality import INFINITE as INFINITE_CARDINALITY # line: 26
from tensorflow.python.data.experimental.ops.cardinality import UNKNOWN as UNKNOWN_CARDINALITY # line: 28
from tensorflow.python.data.experimental.ops.cardinality import assert_cardinality # line: 67
from tensorflow.python.data.experimental.ops.cardinality import cardinality # line: 33
from tensorflow.python.data.experimental.ops.counter import CounterV2 as Counter # line: 24
from tensorflow.python.data.experimental.ops.distribute import SHARD_HINT # line: 31
from tensorflow.python.data.experimental.ops.distributed_save_op import distributed_save # line: 28
from tensorflow.python.data.experimental.ops.enumerate_ops import enumerate_dataset # line: 21
from tensorflow.python.data.experimental.ops.error_ops import ignore_errors # line: 20
from tensorflow.python.data.experimental.ops.from_list import from_list # line: 75
from tensorflow.python.data.experimental.ops.get_single_element import get_single_element # line: 22
from tensorflow.python.data.experimental.ops.grouping import Reducer # line: 388
from tensorflow.python.data.experimental.ops.grouping import bucket_by_sequence_length # line: 112
from tensorflow.python.data.experimental.ops.grouping import group_by_reducer # line: 28
from tensorflow.python.data.experimental.ops.grouping import group_by_window # line: 59
from tensorflow.python.data.experimental.ops.interleave_ops import choose_from_datasets_v2 as choose_from_datasets # line: 176
from tensorflow.python.data.experimental.ops.interleave_ops import parallel_interleave # line: 29
from tensorflow.python.data.experimental.ops.interleave_ops import sample_from_datasets_v2 as sample_from_datasets # line: 92
from tensorflow.python.data.experimental.ops.io import load # line: 108
from tensorflow.python.data.experimental.ops.io import save # line: 26
from tensorflow.python.data.experimental.ops.iterator_ops import get_model_proto # line: 103
from tensorflow.python.data.experimental.ops.iterator_ops import make_saveable_from_iterator # line: 41
from tensorflow.python.data.experimental.ops.lookup_ops import DatasetInitializer # line: 54
from tensorflow.python.data.experimental.ops.lookup_ops import index_table_from_dataset # line: 190
from tensorflow.python.data.experimental.ops.lookup_ops import table_from_dataset # line: 102
from tensorflow.python.data.experimental.ops.pad_to_cardinality import pad_to_cardinality # line: 26
from tensorflow.python.data.experimental.ops.parsing_ops import parse_example_dataset # line: 105
from tensorflow.python.data.experimental.ops.prefetching_ops import copy_to_device # line: 65
from tensorflow.python.data.experimental.ops.prefetching_ops import prefetch_to_device # line: 33
from tensorflow.python.data.experimental.ops.random_access import at # line: 22
from tensorflow.python.data.experimental.ops.random_ops import RandomDatasetV2 as RandomDataset # line: 28
from tensorflow.python.data.experimental.ops.readers import CsvDatasetV2 as CsvDataset # line: 667
from tensorflow.python.data.experimental.ops.readers import SqlDatasetV2 as SqlDataset # line: 1155
from tensorflow.python.data.experimental.ops.readers import make_batched_features_dataset_v2 as make_batched_features_dataset # line: 915
from tensorflow.python.data.experimental.ops.readers import make_csv_dataset_v2 as make_csv_dataset # line: 327
from tensorflow.python.data.experimental.ops.resampling import rejection_resample # line: 21
from tensorflow.python.data.experimental.ops.scan_ops import scan # line: 21
from tensorflow.python.data.experimental.ops.shuffle_ops import shuffle_and_repeat # line: 62
from tensorflow.python.data.experimental.ops.snapshot import snapshot # line: 190
from tensorflow.python.data.experimental.ops.take_while_ops import take_while # line: 21
from tensorflow.python.data.experimental.ops.unique import unique # line: 21
from tensorflow.python.data.experimental.ops.writers import TFRecordWriter # line: 27
from tensorflow.python.data.ops.dataset_ops import AUTOTUNE # line: 105
from tensorflow.python.data.ops.dataset_ops import from_variant # line: 4516
from tensorflow.python.data.ops.dataset_ops import get_structure # line: 4351
from tensorflow.python.data.ops.dataset_ops import to_variant # line: 4531
from tensorflow.python.data.ops.debug_mode import enable_debug_mode # line: 24
from tensorflow.python.data.ops.iterator_ops import get_next_as_optional # line: 1015
from tensorflow.python.data.ops.optional_ops import Optional # line: 31
from tensorflow.python.data.ops.options import AutoShardPolicy # line: 88
from tensorflow.python.data.ops.options import AutotuneAlgorithm # line: 30
from tensorflow.python.data.ops.options import AutotuneOptions # line: 193
from tensorflow.python.data.ops.options import DistributeOptions # line: 278
from tensorflow.python.data.ops.options import ExternalStatePolicy # line: 155
from tensorflow.python.data.ops.options import OptimizationOptions # line: 320
from tensorflow.python.data.ops.options import ThreadingOptions # line: 479
