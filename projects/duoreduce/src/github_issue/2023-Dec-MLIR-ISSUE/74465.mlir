// mlir-opt test.mlir -test-diagnostic-filter=filters=mysource1
module {
  func.func @main(%arg2: tensor<34x1x55x47xi32>){
    %collapsed = tensor.collapse_shape %arg2 [[0, 1], [2], [3]] : tensor<34x1x55x47xi32> into tensor<34x55x47xi32>
    return
  }
}
