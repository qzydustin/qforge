func.func @main(%arg0 : i32, %arg1 : i32) -> i32 attributes {fileName = "4842.sv"} {
  %0 = arith.cmpi slt, %arg0, %arg1 : i32
  cf.cond_br %0, ^bb1, ^bb2
^bb1:
  cf.br ^bb3(%arg0 : i32)
^bb2:
  cf.br ^bb3(%arg1 : i32)
^bb3(%1 : i32):
  return %1 : i32
}