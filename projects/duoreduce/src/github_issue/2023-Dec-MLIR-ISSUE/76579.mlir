// mlir-opt -convert-vector-to-llvm -finalize-memref-to-llvm -convert-arith-to-llvm -convert-openmp-to-llvm
module {
  func.func @omp_target() {
    %alloca = memref.alloca() : memref<64x64xf64>
    %alloca_0 = memref.alloca() : memref<64x64xf64>
    %0 = omp.map_info var_ptr(%alloca : memref<64x64xf64>, tensor<?xi32>) map_clauses(to) capture(ByRef) -> memref<64x64xf64>
    %1 = omp.map_info var_ptr(%alloca_0 : memref<64x64xf64>, tensor<?xi32>) map_clauses(from) capture(ByRef) -> memref<64x64xf64>
    omp.target map_entries(%0 -> %arg0, %1 -> %arg1 : memref<64x64xf64>, memref<64x64xf64>) {
    ^bb0(%arg0: memref<64x64xf64>, %arg1: memref<64x64xf64>):
      omp.teams {
        omp.parallel {
          %c0 = arith.constant 0 : index
          %c1 = arith.constant 1 : index
          %c8192 = arith.constant 8192 : index
          omp.wsloop for  (%arg2, %arg3, %arg4, %arg5) : index = (%c0, %c0, %c0, %c0) to (%c8192, %c8192, %c8192, %c8192) step (%c1, %c1, %c1, %c1) {
            %2 = vector.load %arg0[%arg2, %arg3] : memref<64x64xf64>, vector<16xf64>
            %3 = vector.load %arg1[%arg4, %arg5] : memref<64x64xf64>, vector<16xf64>
            %4 = vector.load %arg1[%arg3, %arg2] : memref<64x64xf64>, vector<16xf64>
            %5 = arith.mulf %2, %3 : vector<16xf64>
            %6 = arith.divf %3, %4 : vector<16xf64>
            %7 = arith.addf %5, %6 : vector<16xf64>
            vector.store %7, %arg1[%arg2, %arg3] : memref<64x64xf64>, vector<16xf64>
            omp.terminator
          }
          omp.terminator
        }
        omp.terminator
      }
      omp.terminator
    }
    omp.barrier
    return
  }
}