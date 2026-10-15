//mlir-opt -test-vector-unrolling-patterns=unroll-based-on-type temp.mlir
module {
  func.func @func1(%arg0: tensor<23x12xf16>, %arg1: tensor<?x?x12xi16>, %arg2: vector<23x21x23xi1>) -> i1 {
    %cst = arith.constant 2.05639219E+9 : f32
    %true = arith.constant true
    %c0 = arith.constant 0 : index
    %c5 = arith.constant 5 : index
    %c6 = arith.constant 6 : index
    %111 = vector.broadcast %cst : f32 to vector<21x12x12xf32>
    %112 = vector.fma %111, %111, %111 : vector<21x12x12xf32>
    vector.print %112 : vector<21x12x12xf32>
    return %true : i1
  }
}
