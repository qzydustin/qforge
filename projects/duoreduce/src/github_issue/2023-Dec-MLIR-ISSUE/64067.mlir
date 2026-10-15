//mlir-opt -sparsifier=vl=8 temp.mlir
module {
  func.func private @func1(%arg0: tensor<?xf16>) { 
    %c0 = arith.constant 0 : index
    %c2 = arith.constant 2 : index  
    %alloc_9 = memref.alloc(%c0, %c2, %c2) : memref<?x?x?xi16>  
    %53 = tensor.empty(%c2, %c2, %c2) : tensor<?x?x?x24xi16>
    %broadcasted = linalg.broadcast ins(%alloc_9 : memref<?x?x?xi16>) outs(%53 : tensor<?x?x?x24xi16>) dimensions = [3] 
    %62 = scf.index_switch %c2 -> index 
    default {
      %141 = memref.alloca_scope  -> (index) { 
        %alloc_33 = memref.alloc(%c2, %c2, %c2) : memref<?x?x24x?xi16>
        linalg.transpose ins(%broadcasted : tensor<?x?x?x24xi16>) outs(%alloc_33 : memref<?x?x24x?xi16>) permutation = [2, 0, 3, 1]  
        memref.alloca_scope.return %c2 : index
      } 
      scf.yield %c2 : index
    } 
    return
  }
}
