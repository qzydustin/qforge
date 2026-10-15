//mlir-opt --convert-cf-to-llvm a.mlir
func.func private @func2(%arg0: tensor<27x16xi64>, %arg1: f16, %arg2: memref<?x16xi16>)  {
  %cst_6 = arith.constant dense<true> : vector<10xi1>
  %cst_8 = arith.constant dense<true> : vector<27xi1>
    %c1 = arith.constant 1 : index
    %c2 = arith.constant 2 : index
    %c3 = arith.constant 3 : index
    %c4 = arith.constant 4 : index
    %c5 = arith.constant 5 : index
    %c7 = arith.constant 7 : index
    %c6 = arith.constant 6 : index
  %6 = llvm.mlir.constant(24583 : i16) : i16
  %7 = vector.mask %cst_8 { vector.mask %cst_6 { vector.multi_reduction <and>, %cst_6, %cst_6 [] : vector<10xi1> to vector<10xi1> } : vector<10xi1> -> vector<10xi1> } : vector<27xi1> -> vector<27xi1>
  %8 = llvm.mlir.constant(24583 : i16) : i16
  %9 = llvm.mlir.constant(24583 : i16) : i16
  %16 = llvm.mlir.constant(24583 : i16) : i16
  %17 = llvm.mlir.constant(24583 : i16) : i16
  %18 = llvm.mlir.constant(24583 : i16) : i16
  %19 = llvm.mlir.constant(24583 : i16) : i16
  %26 = llvm.mlir.constant(24583 : i16) : i16
  %27 = llvm.mlir.constant(24583 : i16) : i16
  %28 = llvm.mlir.constant(24583 : i16) : i16
  %29 = llvm.mlir.constant(24583 : i16) : i16
  return
}
