# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tensorflow/core/protobuf/config.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tensorflow.core.framework import cost_graph_pb2 as tensorflow_dot_core_dot_framework_dot_cost__graph__pb2
from tensorflow.core.framework import graph_pb2 as tensorflow_dot_core_dot_framework_dot_graph__pb2
from tensorflow.core.framework import step_stats_pb2 as tensorflow_dot_core_dot_framework_dot_step__stats__pb2
from tensorflow.core.protobuf import cluster_pb2 as tensorflow_dot_core_dot_protobuf_dot_cluster__pb2
from tensorflow.core.protobuf import debug_pb2 as tensorflow_dot_core_dot_protobuf_dot_debug__pb2
from tensorflow.core.protobuf import rewriter_config_pb2 as tensorflow_dot_core_dot_protobuf_dot_rewriter__config__pb2
from tensorflow.core.protobuf import rpc_options_pb2 as tensorflow_dot_core_dot_protobuf_dot_rpc__options__pb2
try:
  tsl_dot_protobuf_dot_rpc__options__pb2 = tensorflow_dot_core_dot_protobuf_dot_rpc__options__pb2.tsl_dot_protobuf_dot_rpc__options__pb2
except AttributeError:
  tsl_dot_protobuf_dot_rpc__options__pb2 = tensorflow_dot_core_dot_protobuf_dot_rpc__options__pb2.tsl.protobuf.rpc_options_pb2
from tensorflow.tsl.protobuf import coordination_config_pb2 as tsl_dot_protobuf_dot_coordination__config__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%tensorflow/core/protobuf/config.proto\x12\ntensorflow\x1a*tensorflow/core/framework/cost_graph.proto\x1a%tensorflow/core/framework/graph.proto\x1a*tensorflow/core/framework/step_stats.proto\x1a&tensorflow/core/protobuf/cluster.proto\x1a$tensorflow/core/protobuf/debug.proto\x1a.tensorflow/core/protobuf/rewriter_config.proto\x1a*tensorflow/core/protobuf/rpc_options.proto\x1a&tsl/protobuf/coordination_config.proto\"\x89\n\n\nGPUOptions\x12\'\n\x1fper_process_gpu_memory_fraction\x18\x01 \x01(\x01\x12\x14\n\x0c\x61llow_growth\x18\x04 \x01(\x08\x12\x16\n\x0e\x61llocator_type\x18\x02 \x01(\t\x12\x1f\n\x17\x64\x65\x66\x65rred_deletion_bytes\x18\x03 \x01(\x03\x12\x1b\n\x13visible_device_list\x18\x05 \x01(\t\x12\"\n\x1apolling_active_delay_usecs\x18\x06 \x01(\x05\x12$\n\x1cpolling_inactive_delay_msecs\x18\x07 \x01(\x05\x12\x1c\n\x14\x66orce_gpu_compatible\x18\x08 \x01(\x08\x12\x39\n\x0c\x65xperimental\x18\t \x01(\x0b\x32#.tensorflow.GPUOptions.Experimental\x1a\xc2\x07\n\x0c\x45xperimental\x12K\n\x0fvirtual_devices\x18\x01 \x03(\x0b\x32\x32.tensorflow.GPUOptions.Experimental.VirtualDevices\x12#\n\x1bnum_virtual_devices_per_gpu\x18\x0f \x01(\x05\x12\x1a\n\x12use_unified_memory\x18\x02 \x01(\x08\x12#\n\x1bnum_dev_to_dev_copy_streams\x18\x03 \x01(\x05\x12\x1d\n\x15\x63ollective_ring_order\x18\x04 \x01(\t\x12\x1d\n\x15timestamped_allocator\x18\x05 \x01(\x08\x12#\n\x1bkernel_tracker_max_interval\x18\x07 \x01(\x05\x12 \n\x18kernel_tracker_max_bytes\x18\x08 \x01(\x05\x12\"\n\x1akernel_tracker_max_pending\x18\t \x01(\x05\x12\'\n\x1finternal_fragmentation_fraction\x18\n \x01(\x01\x12\x1d\n\x15use_cuda_malloc_async\x18\x0b \x01(\x08\x12,\n$disallow_retry_on_allocation_failure\x18\x0c \x01(\x08\x12 \n\x18gpu_host_mem_limit_in_mb\x18\r \x01(\x02\x12$\n\x1cgpu_host_mem_disallow_growth\x18\x0e \x01(\x08\x12$\n\x1cgpu_system_memory_size_in_mb\x18\x10 \x01(\x05\x12.\n&populate_pjrt_gpu_client_creation_info\x18\x11 \x01(\x08\x12\x0f\n\x07node_id\x18\x12 \x01(\x05\x12T\n\x14stream_merge_options\x18\x13 \x01(\x0b\x32\x36.tensorflow.GPUOptions.Experimental.StreamMergeOptions\x1aS\n\x0eVirtualDevices\x12\x17\n\x0fmemory_limit_mb\x18\x01 \x03(\x02\x12\x10\n\x08priority\x18\x02 \x03(\x05\x12\x16\n\x0e\x64\x65vice_ordinal\x18\x03 \x03(\x05\x1a\x85\x01\n\x12StreamMergeOptions\x12#\n\x1bmerge_host_to_device_stream\x18\x01 \x01(\x08\x12#\n\x1bmerge_device_to_host_stream\x18\x02 \x01(\x08\x12%\n\x1dmerge_device_to_device_stream\x18\x03 \x01(\x08\"\x9d\x03\n\x10OptimizerOptions\x12+\n#do_common_subexpression_elimination\x18\x01 \x01(\x08\x12\x1b\n\x13\x64o_constant_folding\x18\x02 \x01(\x08\x12$\n\x1cmax_folded_constant_in_bytes\x18\x06 \x01(\x03\x12\x1c\n\x14\x64o_function_inlining\x18\x04 \x01(\x08\x12\x35\n\topt_level\x18\x03 \x01(\x0e\x32\".tensorflow.OptimizerOptions.Level\x12\x45\n\x10global_jit_level\x18\x05 \x01(\x0e\x32+.tensorflow.OptimizerOptions.GlobalJitLevel\x12\x16\n\x0e\x63pu_global_jit\x18\x07 \x01(\x08\" \n\x05Level\x12\x06\n\x02L1\x10\x00\x12\x0f\n\x02L0\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\"C\n\x0eGlobalJitLevel\x12\x0b\n\x07\x44\x45\x46\x41ULT\x10\x00\x12\x10\n\x03OFF\x10\xff\xff\xff\xff\xff\xff\xff\xff\xff\x01\x12\x08\n\x04ON_1\x10\x01\x12\x08\n\x04ON_2\x10\x02\"\xee\x02\n\x0cGraphOptions\x12\x1e\n\x16\x65nable_recv_scheduling\x18\x02 \x01(\x08\x12\x37\n\x11optimizer_options\x18\x03 \x01(\x0b\x32\x1c.tensorflow.OptimizerOptions\x12\x18\n\x10\x62uild_cost_model\x18\x04 \x01(\x03\x12\x1e\n\x16\x62uild_cost_model_after\x18\t \x01(\x03\x12\x14\n\x0cinfer_shapes\x18\x05 \x01(\x08\x12\x1a\n\x12place_pruned_graph\x18\x06 \x01(\x08\x12 \n\x18\x65nable_bfloat16_sendrecv\x18\x07 \x01(\x08\x12\x15\n\rtimeline_step\x18\x08 \x01(\x05\x12\x33\n\x0frewrite_options\x18\n \x01(\x0b\x32\x1a.tensorflow.RewriterConfigJ\x04\x08\x01\x10\x02R%skip_common_subexpression_elimination\"A\n\x15ThreadPoolOptionProto\x12\x13\n\x0bnum_threads\x18\x01 \x01(\x05\x12\x13\n\x0bglobal_name\x18\x02 \x01(\t\"0\n\x0fSessionMetadata\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0f\n\x07version\x18\x02 \x01(\x03\"\x95\x10\n\x0b\x43onfigProto\x12>\n\x0c\x64\x65vice_count\x18\x01 \x03(\x0b\x32(.tensorflow.ConfigProto.DeviceCountEntry\x12$\n\x1cintra_op_parallelism_threads\x18\x02 \x01(\x05\x12$\n\x1cinter_op_parallelism_threads\x18\x05 \x01(\x05\x12\x1f\n\x17use_per_session_threads\x18\t \x01(\x08\x12G\n\x1csession_inter_op_thread_pool\x18\x0c \x03(\x0b\x32!.tensorflow.ThreadPoolOptionProto\x12\x18\n\x10placement_period\x18\x03 \x01(\x05\x12\x16\n\x0e\x64\x65vice_filters\x18\x04 \x03(\t\x12+\n\x0bgpu_options\x18\x06 \x01(\x0b\x32\x16.tensorflow.GPUOptions\x12\x1c\n\x14\x61llow_soft_placement\x18\x07 \x01(\x08\x12\x1c\n\x14log_device_placement\x18\x08 \x01(\x08\x12/\n\rgraph_options\x18\n \x01(\x0b\x32\x18.tensorflow.GraphOptions\x12\x1f\n\x17operation_timeout_in_ms\x18\x0b \x01(\x03\x12+\n\x0brpc_options\x18\r \x01(\x0b\x32\x16.tensorflow.RPCOptions\x12+\n\x0b\x63luster_def\x18\x0e \x01(\x0b\x32\x16.tensorflow.ClusterDef\x12\x1d\n\x15isolate_session_state\x18\x0f \x01(\x08\x12(\n share_cluster_devices_in_session\x18\x11 \x01(\x08\x12:\n\x0c\x65xperimental\x18\x10 \x01(\x0b\x32$.tensorflow.ConfigProto.Experimental\x1a\x32\n\x10\x44\x65viceCountEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x05:\x02\x38\x01\x1a\x8f\n\n\x0c\x45xperimental\x12\x1f\n\x17\x63ollective_group_leader\x18\x01 \x01(\t\x12\x15\n\rexecutor_type\x18\x03 \x01(\t\x12\x1a\n\x12recv_buf_max_chunk\x18\x04 \x01(\x05\x12\x19\n\x11use_numa_affinity\x18\x05 \x01(\x08\x12\x35\n-collective_deterministic_sequential_execution\x18\x06 \x01(\x08\x12\x17\n\x0f\x63ollective_nccl\x18\x07 \x01(\x08\x12\x36\n.share_session_state_in_clusterspec_propagation\x18\x08 \x01(\x08\x12\x1f\n\x17\x64isable_thread_spinning\x18\t \x01(\x08\x12(\n share_cluster_devices_in_session\x18\n \x01(\x08\x12\x35\n\x10session_metadata\x18\x0b \x01(\x0b\x32\x1b.tensorflow.SessionMetadata\x12!\n\x19optimize_for_static_graph\x18\x0c \x01(\x08\x12\x1a\n\x12\x65nable_mlir_bridge\x18\r \x01(\x08\x12S\n\x13mlir_bridge_rollout\x18\x11 \x01(\x0e\x32\x36.tensorflow.ConfigProto.Experimental.MlirBridgeRollout\x12&\n\x1e\x65nable_mlir_graph_optimization\x18\x10 \x01(\x08\x12\'\n\x1f\x64isable_output_partition_graphs\x18\x0e \x01(\x08\x12#\n\x1bxla_fusion_autotuner_thresh\x18\x0f \x01(\x03\x12\x10\n\x08use_tfrt\x18\x12 \x01(\x08\x12\x19\n\x11\x65nable_multi_host\x18\x1b \x01(\x08\x12\x1b\n\x13\x62\x61\x63kend_server_port\x18\x1c \x01(\x05\x12\x12\n\ntarget_tpu\x18\x1d \x01(\x08\x12\x12\n\ntarget_gpu\x18\x1e \x01(\x08\x12\x1e\n\x16stream_merge_threshold\x18\x1f \x01(\x05\x12\'\n\x1f\x64isable_functional_ops_lowering\x18\x15 \x01(\x08\x12\'\n\x1fxla_prefer_single_graph_cluster\x18\x16 \x01(\x08\x12\x42\n\x13\x63oordination_config\x18\x17 \x01(\x0b\x32%.tensorflow.CoordinationServiceConfig\x12)\n!disable_optimize_for_static_graph\x18\x18 \x01(\x08\x12\x30\n(disable_eager_executor_streaming_enqueue\x18\x1a \x01(\x08\"\xde\x01\n\x11MlirBridgeRollout\x12#\n\x1fMLIR_BRIDGE_ROLLOUT_UNSPECIFIED\x10\x00\x12\x1f\n\x1bMLIR_BRIDGE_ROLLOUT_ENABLED\x10\x01\x12 \n\x1cMLIR_BRIDGE_ROLLOUT_DISABLED\x10\x02\"\x04\x08\x03\x10\x03\"\x04\x08\x04\x10\x04*%MLIR_BRIDGE_ROLLOUT_SAFE_MODE_ENABLED*.MLIR_BRIDGE_ROLLOUT_SAFE_MODE_FALLBACK_ENABLEDJ\x04\x08\x02\x10\x03J\x04\x08\x13\x10\x14J\x04\x08\x14\x10\x15J\x04\x08\x19\x10\x1a\"\xe1\x04\n\nRunOptions\x12\x36\n\x0btrace_level\x18\x01 \x01(\x0e\x32!.tensorflow.RunOptions.TraceLevel\x12\x15\n\rtimeout_in_ms\x18\x02 \x01(\x03\x12\x1c\n\x14inter_op_thread_pool\x18\x03 \x01(\x05\x12\x1f\n\x17output_partition_graphs\x18\x05 \x01(\x08\x12/\n\rdebug_options\x18\x06 \x01(\x0b\x32\x18.tensorflow.DebugOptions\x12*\n\"report_tensor_allocations_upon_oom\x18\x07 \x01(\x08\x12\x39\n\x0c\x65xperimental\x18\x08 \x01(\x0b\x32#.tensorflow.RunOptions.Experimental\x1a\xd2\x01\n\x0c\x45xperimental\x12\x1c\n\x14\x63ollective_graph_key\x18\x01 \x01(\x03\x12\x1c\n\x14use_run_handler_pool\x18\x02 \x01(\x08\x12[\n\x18run_handler_pool_options\x18\x03 \x01(\x0b\x32\x39.tensorflow.RunOptions.Experimental.RunHandlerPoolOptions\x1a)\n\x15RunHandlerPoolOptions\x12\x10\n\x08priority\x18\x01 \x01(\x03\"R\n\nTraceLevel\x12\x0c\n\x08NO_TRACE\x10\x00\x12\x12\n\x0eSOFTWARE_TRACE\x10\x01\x12\x12\n\x0eHARDWARE_TRACE\x10\x02\x12\x0e\n\nFULL_TRACE\x10\x03J\x04\x08\x04\x10\x05\"\xbe\x03\n\x0bRunMetadata\x12)\n\nstep_stats\x18\x01 \x01(\x0b\x32\x15.tensorflow.StepStats\x12,\n\ncost_graph\x18\x02 \x01(\x0b\x32\x18.tensorflow.CostGraphDef\x12.\n\x10partition_graphs\x18\x03 \x03(\x0b\x32\x14.tensorflow.GraphDef\x12?\n\x0f\x66unction_graphs\x18\x04 \x03(\x0b\x32&.tensorflow.RunMetadata.FunctionGraphs\x12\x35\n\x10session_metadata\x18\x05 \x01(\x0b\x32\x1b.tensorflow.SessionMetadata\x1a\xad\x01\n\x0e\x46unctionGraphs\x12.\n\x10partition_graphs\x18\x01 \x03(\x0b\x32\x14.tensorflow.GraphDef\x12\x34\n\x16pre_optimization_graph\x18\x02 \x01(\x0b\x32\x14.tensorflow.GraphDef\x12\x35\n\x17post_optimization_graph\x18\x03 \x01(\x0b\x32\x14.tensorflow.GraphDef\":\n\x10TensorConnection\x12\x13\n\x0b\x66rom_tensor\x18\x01 \x01(\t\x12\x11\n\tto_tensor\x18\x02 \x01(\t\"\xb0\x03\n\x0f\x43\x61llableOptions\x12\x0c\n\x04\x66\x65\x65\x64\x18\x01 \x03(\t\x12\r\n\x05\x66\x65tch\x18\x02 \x03(\t\x12\x0e\n\x06target\x18\x03 \x03(\t\x12+\n\x0brun_options\x18\x04 \x01(\x0b\x32\x16.tensorflow.RunOptions\x12\x37\n\x11tensor_connection\x18\x05 \x03(\x0b\x32\x1c.tensorflow.TensorConnection\x12\x42\n\x0c\x66\x65\x65\x64_devices\x18\x06 \x03(\x0b\x32,.tensorflow.CallableOptions.FeedDevicesEntry\x12\x44\n\rfetch_devices\x18\x07 \x03(\x0b\x32-.tensorflow.CallableOptions.FetchDevicesEntry\x12\x17\n\x0f\x66\x65tch_skip_sync\x18\x08 \x01(\x08\x1a\x32\n\x10\x46\x65\x65\x64\x44\x65vicesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x1a\x33\n\x11\x46\x65tchDevicesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x42\x84\x01\n\x18org.tensorflow.frameworkB\x0c\x43onfigProtosP\x01ZUgithub.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_proto\xf8\x01\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tensorflow.core.protobuf.config_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030org.tensorflow.frameworkB\014ConfigProtosP\001ZUgithub.com/tensorflow/tensorflow/tensorflow/go/core/protobuf/for_core_protos_go_proto\370\001\001'
  _CONFIGPROTO_DEVICECOUNTENTRY._options = None
  _CONFIGPROTO_DEVICECOUNTENTRY._serialized_options = b'8\001'
  _CALLABLEOPTIONS_FEEDDEVICESENTRY._options = None
  _CALLABLEOPTIONS_FEEDDEVICESENTRY._serialized_options = b'8\001'
  _CALLABLEOPTIONS_FETCHDEVICESENTRY._options = None
  _CALLABLEOPTIONS_FETCHDEVICESENTRY._serialized_options = b'8\001'
  _GPUOPTIONS._serialized_start=391
  _GPUOPTIONS._serialized_end=1680
  _GPUOPTIONS_EXPERIMENTAL._serialized_start=718
  _GPUOPTIONS_EXPERIMENTAL._serialized_end=1680
  _GPUOPTIONS_EXPERIMENTAL_VIRTUALDEVICES._serialized_start=1461
  _GPUOPTIONS_EXPERIMENTAL_VIRTUALDEVICES._serialized_end=1544
  _GPUOPTIONS_EXPERIMENTAL_STREAMMERGEOPTIONS._serialized_start=1547
  _GPUOPTIONS_EXPERIMENTAL_STREAMMERGEOPTIONS._serialized_end=1680
  _OPTIMIZEROPTIONS._serialized_start=1683
  _OPTIMIZEROPTIONS._serialized_end=2096
  _OPTIMIZEROPTIONS_LEVEL._serialized_start=1995
  _OPTIMIZEROPTIONS_LEVEL._serialized_end=2027
  _OPTIMIZEROPTIONS_GLOBALJITLEVEL._serialized_start=2029
  _OPTIMIZEROPTIONS_GLOBALJITLEVEL._serialized_end=2096
  _GRAPHOPTIONS._serialized_start=2099
  _GRAPHOPTIONS._serialized_end=2465
  _THREADPOOLOPTIONPROTO._serialized_start=2467
  _THREADPOOLOPTIONPROTO._serialized_end=2532
  _SESSIONMETADATA._serialized_start=2534
  _SESSIONMETADATA._serialized_end=2582
  _CONFIGPROTO._serialized_start=2585
  _CONFIGPROTO._serialized_end=4654
  _CONFIGPROTO_DEVICECOUNTENTRY._serialized_start=3306
  _CONFIGPROTO_DEVICECOUNTENTRY._serialized_end=3356
  _CONFIGPROTO_EXPERIMENTAL._serialized_start=3359
  _CONFIGPROTO_EXPERIMENTAL._serialized_end=4654
  _CONFIGPROTO_EXPERIMENTAL_MLIRBRIDGEROLLOUT._serialized_start=4408
  _CONFIGPROTO_EXPERIMENTAL_MLIRBRIDGEROLLOUT._serialized_end=4630
  _RUNOPTIONS._serialized_start=4657
  _RUNOPTIONS._serialized_end=5266
  _RUNOPTIONS_EXPERIMENTAL._serialized_start=4966
  _RUNOPTIONS_EXPERIMENTAL._serialized_end=5176
  _RUNOPTIONS_EXPERIMENTAL_RUNHANDLERPOOLOPTIONS._serialized_start=5135
  _RUNOPTIONS_EXPERIMENTAL_RUNHANDLERPOOLOPTIONS._serialized_end=5176
  _RUNOPTIONS_TRACELEVEL._serialized_start=5178
  _RUNOPTIONS_TRACELEVEL._serialized_end=5260
  _RUNMETADATA._serialized_start=5269
  _RUNMETADATA._serialized_end=5715
  _RUNMETADATA_FUNCTIONGRAPHS._serialized_start=5542
  _RUNMETADATA_FUNCTIONGRAPHS._serialized_end=5715
  _TENSORCONNECTION._serialized_start=5717
  _TENSORCONNECTION._serialized_end=5775
  _CALLABLEOPTIONS._serialized_start=5778
  _CALLABLEOPTIONS._serialized_end=6210
  _CALLABLEOPTIONS_FEEDDEVICESENTRY._serialized_start=6107
  _CALLABLEOPTIONS_FEEDDEVICESENTRY._serialized_end=6157
  _CALLABLEOPTIONS_FETCHDEVICESENTRY._serialized_start=6159
  _CALLABLEOPTIONS_FETCHDEVICESENTRY._serialized_end=6210
# @@protoc_insertion_point(module_scope)
