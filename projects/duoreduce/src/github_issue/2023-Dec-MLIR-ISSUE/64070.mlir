//mlir-opt --test-written-to temp.mlir
module {
  func.func @func1(%arg0: vector<23x23xi1>, %arg1: f32, %arg2: f32) -> memref<23x23xf16> {
    %c2 = arith.constant 2 : index
    %c3 = arith.constant 3 : index
    %c12 = arith.constant 12 : index
    %c14 = arith.constant 14 : index
    %c17 = arith.constant 17 : index
    %c28 = arith.constant 28 : index
    %6 = tensor.empty() : tensor<14xi64>
    %30 = index.maxs %c12, %c28
    %55 = scf.parallel (%arg3, %arg4) = (%c14, %c3) to (%30, %c2) step (%c28, %c17) init (%6) -> tensor<14xi64> {
      %131 = tensor.empty() : tensor<14xi64>
      scf.reduce(%131)  : tensor<14xi64> {
      ^bb0(%arg5: tensor<14xi64>, %arg6: tensor<14xi64>):
        %139 = tensor.empty() : tensor<14xi64>
        scf.reduce.return %139 : tensor<14xi64>
      }
      scf.yield
    }
    %alloc_35 = memref.alloc() : memref<23x23xf16>
    return %alloc_35 : memref<23x23xf16>
  }
}
