# This file is MACHINE GENERATED! Do not edit.
# Generated by: tensorflow/python/tools/api/generator2/generator/generator.py script.
"""Public API for tf._api.v2.quantization namespace
"""

import sys as _sys

from tensorflow._api.v2.compat.v1.quantization import experimental
from tensorflow.python.ops.gen_array_ops import fake_quant_with_min_max_args # line: 2698
from tensorflow.python.ops.gen_array_ops import fake_quant_with_min_max_args_gradient # line: 2867
from tensorflow.python.ops.gen_array_ops import fake_quant_with_min_max_vars # line: 3003
from tensorflow.python.ops.gen_array_ops import fake_quant_with_min_max_vars_gradient # line: 3145
from tensorflow.python.ops.gen_array_ops import fake_quant_with_min_max_vars_per_channel # line: 3276
from tensorflow.python.ops.gen_array_ops import fake_quant_with_min_max_vars_per_channel_gradient # line: 3423
from tensorflow.python.ops.gen_array_ops import quantized_concat # line: 8206
from tensorflow.python.ops.array_ops import dequantize # line: 5859
from tensorflow.python.ops.array_ops import quantize # line: 5820
from tensorflow.python.ops.array_ops import quantize_and_dequantize # line: 5896
from tensorflow.python.ops.array_ops import quantize_and_dequantize_v2 # line: 5963

from tensorflow.python.util import module_wrapper as _module_wrapper

if not isinstance(_sys.modules[__name__], _module_wrapper.TFModuleWrapper):
  _sys.modules[__name__] = _module_wrapper.TFModuleWrapper(
      _sys.modules[__name__], "quantization", public_apis=None, deprecation=False,
      has_lite=False)
