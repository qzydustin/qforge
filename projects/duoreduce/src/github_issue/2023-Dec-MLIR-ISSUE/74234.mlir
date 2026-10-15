//mlir-opt --int-range-optimizations a.mlir
func.func private @func1() -> index {
  %c30 = arith.constant 30 : index
  %2 = builtin.unrealized_conversion_cast %c30 : index to i32
  llvm.return %2 : i32
}
llvm.func @func2() {
  %c0 = arith.constant 0 : index
  %52 = func.call @func1() : () -> index
  %62 = index.maxu %c0, %52
  llvm.return
}
