//mlir-opt -pass-pipeline='builtin.module(func.func(test-match-reduction))' temp.mlir
module {
  func.func @func2(%arg0: tensor<?x?x?xi1>, %arg1: tensor<5x5xi32>) {
    %c9777_i16 = arith.constant 9777 : i16
    %c-3527_i16 = arith.constant -3527 : i16
    %c2 = arith.constant 2 : index 
    %18 = index.ceildivu %c2, %c2
    %28 = index.ceildivu %c2, %c2
    %43 = index.sizeof
    %46 = index.divs %c2, %c2
    %92 = affine.apply affine_map<(d0, d1, d2, d3) -> (d0 - 16)>(%46, %28, %c2, %43)
    scf.index_switch %92 
    default {
      %136 = scf.index_switch %c2 -> memref<23x8xi1> 
      default {
        %147 = tensor.empty() : tensor<7xi16>
        %148 = tensor.empty() : tensor<i16>
        %149 = linalg.dot ins(%147, %147 : tensor<7xi16>, tensor<7xi16>) outs(%148 : tensor<i16>) -> tensor<i16>
        %alloc_37 = memref.alloc() : memref<23x8xi1>
        scf.yield %alloc_37 : memref<23x8xi1>
      }
    } 
    return
  }
}
