//mlir-opt --generate-runtime-verification --vp-counters-per-site=1 "--gpu-to-llvm=use-bare-pointers-for-host use-bare-pointers-for-kernels" temp.mlir
module {
  func.func private @func2(%arg0: tensor<8x32xi32>, %arg1: vector<8x32xi1>, %arg2: vector<32x16xf16>) -> memref<32x16xf32> {
    %c1 = arith.constant 1 : index
    %c6 = arith.constant 6 : index 
    %9 = tensor.empty(%c1, %c6) : tensor<?x?xi64>
    %alloc = memref.alloc() : memref<8x32xi64>
    %alloc_6 = memref.alloc(%c6) : memref<?x16xi1>
    %alloc_16 = memref.alloc(%c6) : memref<?xi1>
    %true_22 = index.bool.constant true
    %72 = scf.while (%arg3 = %9) : (tensor<?x?xi64>) -> tensor<?x?xi64> {
      %147 = tensor.empty(%c1, %c6) : tensor<?x?xi64>
      scf.condition(%true_22) %147 : tensor<?x?xi64>
    } do {
    ^bb0(%arg3: tensor<?x?xi64>):
      %139 = memref.alloca_scope  -> (index) {
        %cast_35 = memref.cast %alloc : memref<8x32xi64> to memref<?x?xi64>
        %168 = memref.realloc %alloc_16 : memref<?xi1> to memref<19xi1>
        %c0_40 = arith.constant 0 : index
        memref.alloca_scope.return %c0_40 : index
      }
      %155 = tensor.empty(%c1, %c6) : tensor<?x?xi64>
      scf.yield %155 : tensor<?x?xi64>
    }
    %alloc_32 = memref.alloc() : memref<32x16xf32>
    return %alloc_32 : memref<32x16xf32>
  }
}

