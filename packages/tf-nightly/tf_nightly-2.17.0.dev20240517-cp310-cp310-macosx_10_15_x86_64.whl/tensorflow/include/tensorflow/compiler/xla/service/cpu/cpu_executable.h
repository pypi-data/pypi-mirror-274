/* Copyright 2017 The OpenXLA Authors.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
==============================================================================*/

#ifndef XLA_SERVICE_CPU_CPU_EXECUTABLE_H_
#define XLA_SERVICE_CPU_CPU_EXECUTABLE_H_

#include <cstddef>
#include <memory>
#include <string>
#include <string_view>
#include <utility>
#include <variant>
#include <vector>

#include "absl/types/span.h"
#include "xla/hlo/ir/hlo_instruction.h"
#include "xla/hlo/ir/hlo_module.h"
#include "xla/service/buffer_assignment.h"
#include "xla/service/cpu/buffer_desc.h"
#include "xla/service/cpu/simple_orc_jit.h"
#include "xla/service/cpu/xla_framework.h"
#include "xla/service/custom_call_status_internal.h"
#include "xla/service/executable.h"
#include "xla/service/hlo_dataflow_analysis.h"
#include "xla/service/hlo_execution_profile.h"
#include "xla/service/shaped_buffer.h"
#include "xla/statusor.h"
#include "xla/stream_executor/device_memory_allocator.h"
#include "xla/stream_executor/stream_executor.h"
#include "xla/types.h"

namespace xla {
namespace cpu {

// CPU-targeting implementation of the XLA Executable interface.
//
// Wraps a JIT-ed object that can be executed "on device". We JIT for the host
// architecture, so JIT-ed code and host code share the same ABI.
class CpuExecutable : public Executable {
 public:
  static absl::StatusOr<std::unique_ptr<CpuExecutable>> Create(
      std::unique_ptr<SimpleOrcJIT> jit,
      std::unique_ptr<const BufferAssignment> assignment,
      std::unique_ptr<HloModule> hlo_module,
      const std::string& entry_function_name,
      std::unique_ptr<HloProfilePrinterData> hlo_profile_printer_data,
      std::unique_ptr<HloProfileIndexMap> hlo_profile_index_map);
  // XLA Runtime factory method.
  static absl::StatusOr<std::unique_ptr<CpuExecutable>> Create(
      std::unique_ptr<HloModule> hlo_module,
      std::unique_ptr<HloProfilePrinterData> hlo_profile_printer_data,
      std::unique_ptr<HloProfileIndexMap> hlo_profile_index_map,
      std::unique_ptr<const BufferAssignment> assignment);

  ~CpuExecutable() override;

  absl::StatusOr<ExecutionOutput> ExecuteAsyncOnStream(
      const ServiceExecutableRunOptions* run_options,
      std::vector<ExecutionInput> arguments,
      HloExecutionProfile* hlo_execution_profile) override;

  // Calls the generated function performing the computation with the given
  // arguments using the supplied buffers.
  absl::Status ExecuteComputeFunction(
      const ExecutableRunOptions* run_options,
      absl::Span<MaybeOwningDeviceMemory const> buffers,
      HloExecutionProfile* hlo_execution_profile);

  absl::Span<const std::string> obj_files() const { return obj_files_; }

  void set_obj_files(std::vector<std::string> obj_files) {
    obj_files_ = std::move(obj_files);
  }

  // This should be called after set_ir_module_string.
  const std::string& ir_module_string() const { return ir_module_string_; }

  void set_ir_module_string(const std::string& ir_module_string) {
    ir_module_string_ = ir_module_string;
  }

  const std::string& module_name() const { return module_name_; }

  static int64_t ShapeSizeBytes(const Shape& shape);

  // Type of the computation function we expect in the JIT.
  using ComputeFunctionType =
      void (*)(void* /*result*/, const ExecutableRunOptions* /*run_options*/,
               const void** /*args*/, void** /*buffer_table*/,
               XlaCustomCallStatus* /*status*/, int64_t* /*profile_counters*/);

  const ComputeFunctionType& compute_function() const {
    return compute_function_;
  }

  const BufferAssignment& buffer_assignment() const { return *assignment_; }

  int64_t SizeOfGeneratedCodeInBytes() const override;

  absl::Span<const BufferAllocation> GetAllocations() const override {
    return assignment_->Allocations();
  }

 private:
  // Creates an array suitable for passing as the "buffer_table" argument to the
  // JIT compiled function pointer.
  //
  // Returns (unowning_buffers, owning_buffers) where:
  //
  //  - unowning_buffers.data() can be passed as the buffer_table argument as-is
  //    and includes pointers to the scratch storage required by the
  //    computation, the live-out buffer into which the result will be written
  //    and entry computation parameters.
  //
  //  - owning_buffers contains owning pointers to the buffers that were
  //    allocated by this routine.  This routine allocates buffers for temporary
  //    storage and the live-out buffer into which the computation writes it
  //    result.
  //
  //  - buffers_to_free: buffers whose ownership was donated by the caller that
  //    are to be freed by the caller.
  absl::StatusOr<std::vector<MaybeOwningDeviceMemory>> CreateBufferTable(
      se::DeviceMemoryAllocator* memory_allocator, int device_ordinal,
      absl::Span<ExecutionInput const> arguments);

  // Creates an Execution output holding ScopedShapedBuffer for holding the
  // result of the computation, moving buffers out of allocated_buffers and into
  // the result as appropriate.  The addresses are set according to buffer
  // assignment.
  absl::StatusOr<ExecutionOutput> CreateResultShapedBuffer(
      const ServiceExecutableRunOptions* run_options,
      absl::Span<MaybeOwningDeviceMemory> buffers,
      absl::Span<ExecutionInput> arguments);

  // Returns the instruction value set of the root instruction of the entry
  // computation. Uses dataflow analysis from buffer assignment.
  const InstructionValueSet& GetRootValueSet() const;

  // The JIT containing compiled modules.
  std::unique_ptr<SimpleOrcJIT> jit_;

  // Object files (machine code) compiled from an HLO module by the JIT
  // compiler. We capture all object files created by SimpleOrcJIT so we can
  // export them to AOT compilation result.
  std::vector<std::string> obj_files_;

  // Buffer assignment for the buffers we need to allocate.
  const std::unique_ptr<const BufferAssignment> assignment_;

  // The LLVM IR, in string format, of the unoptimized module generated for this
  // CpuExecutable. We save a string instead of an llvm::Module* because leaving
  // llvm::Module* in a singleton can cause the heap checker to emit false
  // positives.
  std::string ir_module_string_;

  // Unique identifier.
  std::string module_name_;

  ComputeFunctionType compute_function_;

  // Entry function name for the computation.
  const std::string entry_function_name_;

  CpuExecutable(std::unique_ptr<HloModule> hlo_module,
                std::unique_ptr<HloProfilePrinterData> hlo_profile_printer_data,
                std::unique_ptr<HloProfileIndexMap> hlo_profile_index_map,
                std::unique_ptr<const BufferAssignment> assignment);
  CpuExecutable(const CpuExecutable&) = delete;
  CpuExecutable& operator=(const CpuExecutable&) = delete;
};

}  // namespace cpu
}  // namespace xla

#endif  // XLA_SERVICE_CPU_CPU_EXECUTABLE_H_
