//mlir-opt --convert-cf-to-llvm a.mlir
func.func private @func2(%arg0: tensor<27x16xi64>, %arg1: f16, %arg2: memref<?x16xi16>)  {
  %cst_6 = arith.constant dense<true> : vector<10xi1>
  %cst_8 = arith.constant dense<true> : vector<27xi1>
  %7 = vector.mask %cst_8 { vector.mask %cst_6 { vector.multi_reduction <and>, %cst_6, %cst_6 [] : vector<10xi1> to vector<10xi1> } : vector<10xi1> -> vector<10xi1> } : vector<27xi1> -> vector<27xi1>
  return 
}
