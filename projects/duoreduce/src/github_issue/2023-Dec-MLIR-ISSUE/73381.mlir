//mlir-opt --arith-emulate-wide-int a.mlir
func.func @func2() {
  %cst_0 = arith.constant dense<0> : vector<2xi64>
  %cst_4 = arith.constant dense<true> : vector<2xi1>
  %2 = vector.mask %cst_4 { vector.multi_reduction <xor>, %cst_0, %cst_0 [] : vector<2xi64> to vector<2xi64> } : vector<2xi1> -> vector<2xi64>
  return
}
