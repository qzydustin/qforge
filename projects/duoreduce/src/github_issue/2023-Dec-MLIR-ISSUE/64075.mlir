//mlir-opt -test-vector-unrolling-patterns=unroll-based-on-type temp.mlir
module {
  func.func nested @func1(%arg0: i64, %arg1: memref<?x?xf16>, %arg2: i16) -> f32 {
    %cst_1 = arith.constant 1.0 : f32
    %23 = vector.broadcast %cst_1 : f32 to vector<23x8xf32>
    %24 = vector.extract_strided_slice %23 {offsets = [14], sizes = [6], strides = [1]} : vector<23x8xf32> to vector<6x8xf32>
    %115 = vector.multi_reduction <minf>, %24, %cst_1 [0, 1] : vector<6x8xf32> to f32
    return %115 : f32
  }
}
