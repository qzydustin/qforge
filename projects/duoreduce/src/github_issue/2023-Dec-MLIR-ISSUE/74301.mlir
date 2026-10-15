//~/circt/llvm/build/bin/mlir-opt --canonicalize 74301.mlir
func.func private @func2() {
  %cst_12 = arith.constant dense<23> : vector<15xindex>
  %cst_13 = arith.constant dense<false> : vector<15xi1>
  %cst_18 = arith.constant 1.000000e+00 : f16
  %c0 = arith.constant 0 : index
  %c7 = arith.constant 7 : index
  %c18 = arith.constant 18 : index
  %alloc_27 = memref.alloc(%c18, %c7) : memref<?x?xf16>
  %10 = affine.for %arg3 = 0 to 114 iter_args(%arg4 = %c18) -> (index) {
    affine.yield %arg3 : index
  }
  %13 = memref.alloca_scope  -> (f16) {
    memref.alloca_scope.return %cst_18 : f16
  }
  memref.alloca_scope  {
    %16 = vector.broadcast %13 : f16 to vector<15xf16>
    vector.scatter %alloc_27[%10, %c0] [%cst_12], %cst_13, %16 : memref<?x?xf16>, vector<15xindex>, vector<15xi1>, vector<15xf16>
  }
  return
}
