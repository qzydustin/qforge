module {
hw.module @wut() -> (rwDataOut: i8) attributes {fileName = "wut.sv"} {
  %.rwDataOut.output = sv.wire : !hw.inout<i8>
  %0 = sv.read_inout %.rwDataOut.output : !hw.inout<i8>
  sv.assign %.rwDataOut.output, %0 : i8
  hw.output %0 : i8
}
}
