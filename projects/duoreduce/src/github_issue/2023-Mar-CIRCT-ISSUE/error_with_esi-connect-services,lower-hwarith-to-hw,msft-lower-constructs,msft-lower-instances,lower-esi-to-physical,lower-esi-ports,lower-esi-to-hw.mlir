// passes ran: msft-export-tcl{tops=PolynomialSystem tcl-file=PolynomialSystem.tcl}
module {
  hw.module @PolynomialSystem<__INST_HIER: none = "INSTANTIATE_WITH_INSTANCE_PATH">() -> (y: i32) attributes {output_file = #hw.output_file<"PolynomialSystem.sv", includeReplicatedOps>} {
    %c23_i32 = hw.constant 23 : i32
    %example.y = hw.instance "example" sym @example @PolyComputeForCoeff__62__42__6_<__INST_HIER: none = #hw.param.expr.str.concat<#hw.param.decl.ref<"__INST_HIER">, ".example">>(x: %c23_i32: i32) -> (y: i32) {msft.appid = #msft.appid<"poly"[0]>}
    %example2.y = hw.instance "example2" sym @example2 @PolyComputeForCoeff__62__42__6_<__INST_HIER: none = #hw.param.expr.str.concat<#hw.param.decl.ref<"__INST_HIER">, ".example2">>(x: %example.y: i32) -> (y: i32)
    %example2_1.y = hw.instance "example2_1" sym @example2_1 @PolyComputeForCoeff__1__2__3__4__5_<__INST_HIER: none = #hw.param.expr.str.concat<#hw.param.decl.ref<"__INST_HIER">, ".example2_1">>(x: %example.y: i32) -> (y: i32)
    %CoolPolynomialCompute.y = hw.instance "CoolPolynomialCompute" sym @CoolPolynomialCompute @supercooldevice(x: %c23_i32: i32) -> (y: i32)
    hw.instance "M" sym @M @parameterized_extern<a: i64 = 8, b: i64 = 3>() -> ()
    hw.output %example.y : i32
  }
  hw.module @PolyComputeForCoeff__62__42__6_<__INST_HIER: none = "INSTANTIATE_WITH_INSTANCE_PATH">(%x: i32) -> (y: i32) attributes {output_file = #hw.output_file<"PolynomialCompute.sv", includeReplicatedOps>} {
    %c6_i32 = hw.constant 6 : i32
    %c62_i32 = hw.constant 62 : i32
    %c42_i32 = hw.constant 42 : i32
    %0 = comb.mul %x, %c42_i32 : i32
    %1 = comb.mul %x, %x, %c6_i32 : i32
    %2 = comb.add %0, %1, %c62_i32 : i32
    hw.output %2 : i32
  }
  hw.module @PolyComputeForCoeff__1__2__3__4__5_<__INST_HIER: none = "INSTANTIATE_WITH_INSTANCE_PATH">(%x: i32) -> (y: i32) attributes {output_file = #hw.output_file<"PolynomialCompute.sv", includeReplicatedOps>} {
    %c0_i2 = hw.constant 0 : i2
    %false = hw.constant false
    %c5_i32 = hw.constant 5 : i32
    %c3_i32 = hw.constant 3 : i32
    %c1_i32 = hw.constant 1 : i32
    %0 = comb.extract %x from 0 : (i32) -> i31
    %1 = comb.concat %0, %false : i31, i1
    %2 = comb.mul %x, %x, %c3_i32 : i32
    %3 = comb.extract %x from 0 : (i32) -> i30
    %4 = comb.mul %3, %3, %3 : i30
    %5 = comb.concat %4, %c0_i2 : i30, i2
    %6 = comb.mul %x, %x, %x, %x, %c5_i32 : i32
    %7 = comb.add %1, %2, %5, %6, %c1_i32 : i32
    hw.output %7 : i32
  }
  hw.module.extern @supercooldevice(%x: i32) -> (y: i32) attributes {output_file = #hw.output_file<"PolynomialSystem.sv", includeReplicatedOps>, verilogName = "supercooldevice"}
  hw.module.extern @parameterized_extern<a: i64, b: i64>() attributes {output_file = #hw.output_file<"PolynomialSystem.sv", includeReplicatedOps>, verilogName = "parameterized_extern"}
  sv.verbatim "{\0A  \22declarations\22: [],\0A  \22top_levels\22: [\0A    {\0A      \22module\22: \22@PolynomialSystem\22,\0A      \22services\22: []\0A    }\0A  ],\0A  \22modules\22: []\0A}" {output_file = #hw.output_file<"services.json">}
  sv.verbatim "" {output_file = #hw.output_file<"PolynomialSystem.tcl">}
}
