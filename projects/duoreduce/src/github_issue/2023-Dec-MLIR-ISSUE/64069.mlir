//mlir-opt "-sparsifier=enable-runtime-library=false vl=2 reassociate-fp-reductions=true" temp.mlir
module {
  func.func @func1(%arg0: memref<26xi1>, %arg1: vector<12x26xi1>) -> memref<?x?x?xi1> {
    %c17 = arith.constant 17 : index
    %c24 = arith.constant 24 : index
    %c30 = arith.constant 30 : index
    %alloc_18 = memref.alloc() : memref<12x26xi1>
    %alloc_23 = memref.alloc() : memref<12x26x21xi1>
    linalg.broadcast ins(%alloc_18 : memref<12x26xi1>) outs(%alloc_23 : memref<12x26x21xi1>) dimensions = [2] 
    %alloc_26 = memref.alloc(%c24, %c17, %c30) : memref<?x?x?xi1>
    return %alloc_26 : memref<?x?x?xi1>
  }
}
