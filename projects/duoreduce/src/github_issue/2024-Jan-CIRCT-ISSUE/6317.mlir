hw.module @Test(in %x : i8, in %clock: i8, out x : i8) {
  // All of these are equivalent to `var logic x` .

  // logic-type variable, assign to x.
  %logicvar = sv.logic : !hw.inout<i8>
  sv.assign %logicvar, %x : i8

  // Same but use keyword "reg" (reg x; = var logic x;)
  %regvar = sv.reg : !hw.inout<i8>
  sv.assign %regvar, %x : i8
  
  // sv.reg supports initialization operand, demonstrate.
  %regwithinit = sv.reg init %x : !hw.inout<i8>
  hw.output %x : i8
}
