hw.module @Test(in %x : i8, in %clock: i8) {
  %logicvar = sv.logic : !hw.inout<i8>
  sv.assign %logicvar, %x : i8
  %regvar = sv.reg : !hw.inout<i8>
  sv.assign %regvar, %x : i8
}
