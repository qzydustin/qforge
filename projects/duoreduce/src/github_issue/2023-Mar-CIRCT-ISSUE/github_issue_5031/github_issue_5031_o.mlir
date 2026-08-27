module attributes {tf_saved_model.semantics, tfl.description = "MLIR Converted.", tfl.schema_version = 3 : i32} {
  func.func @main(%arg0: i8 {tf_saved_model.index_path = ["dense_input"]}) -> (i8 {tf_saved_model.index_path = ["dense_2"]}) attributes {fileName = "4842.sv"} {
    %c0_i32 = arith.constant 0 : i32
    %c-128_i32 = arith.constant -128 : i32
    %c1073741824_i64 = arith.constant 1073741824 : i64
    %c-1073741824_i64 = arith.constant -1073741824 : i64
    %c127_i32 = arith.constant 127 : i32
    %c-128_i8 = arith.constant -128 : i8
    %c127_i8 = arith.constant 127 : i8
    %c5_i32 = arith.constant 5 : i32
    %c36_i64 = arith.constant 36 : i64
    %c1630361836_i64 = arith.constant 1630361836 : i64
    %c34359738368_i64 = arith.constant 34359738368 : i64
    %c37_i64 = arith.constant 37 : i64
    %c1561796795_i64 = arith.constant 1561796795 : i64
    %c68719476736_i64 = arith.constant 68719476736 : i64
    %c38_i64 = arith.constant 38 : i64
    %c137438953472_i64 = arith.constant 137438953472 : i64
    %c2039655736_i64 = arith.constant 2039655736 : i64
    %c429_i32 = arith.constant 429 : i32
    %c-729_i32 = arith.constant -729 : i32
    %c1954_i32 = arith.constant 1954 : i32
    %c610_i32 = arith.constant 610 : i32
    %c241_i32 = arith.constant 241 : i32
    %c-471_i32 = arith.constant -471 : i32
    %c-35_i32 = arith.constant -35 : i32
    %c-867_i32 = arith.constant -867 : i32
    %c571_i32 = arith.constant 571 : i32
    %c581_i32 = arith.constant 581 : i32
    %c4260_i32 = arith.constant 4260 : i32
    %c3943_i32 = arith.constant 3943 : i32
    %c591_i32 = arith.constant 591 : i32
    %c-889_i32 = arith.constant -889 : i32
    %c-5103_i32 = arith.constant -5103 : i32
    %c-5438_i32 = arith.constant -5438 : i32
    %c-5515_i32 = arith.constant -5515 : i32
    %c-1352_i32 = arith.constant -1352 : i32
    %c-1500_i32 = arith.constant -1500 : i32
    %c-4152_i32 = arith.constant -4152 : i32
    %c-84_i32 = arith.constant -84 : i32
    %c3396_i32 = arith.constant 3396 : i32
    %c1981_i32 = arith.constant 1981 : i32
    %c-5581_i32 = arith.constant -5581 : i32
    %c-6964_i32 = arith.constant -6964 : i32
    %c3407_i32 = arith.constant 3407 : i32
    %c-7217_i32 = arith.constant -7217 : i32
    %c-9_i32 = arith.constant -9 : i32
    %c-54_i32 = arith.constant -54 : i32
    %c57_i32 = arith.constant 57 : i32
    %c71_i32 = arith.constant 71 : i32
    %c104_i32 = arith.constant 104 : i32
    %c115_i32 = arith.constant 115 : i32
    %c98_i32 = arith.constant 98 : i32
    %c99_i32 = arith.constant 99 : i32
    %c64_i32 = arith.constant 64 : i32
    %c-26_i32 = arith.constant -26 : i32
    %c25_i32 = arith.constant 25 : i32
    %c-82_i32 = arith.constant -82 : i32
    %c68_i32 = arith.constant 68 : i32
    %c95_i32 = arith.constant 95 : i32
    %c86_i32 = arith.constant 86 : i32
    %c-12_i32 = arith.constant -12 : i32
    %c26_i32 = arith.constant 26 : i32
    %c-19_i32 = arith.constant -19 : i32
    %c9_i32 = arith.constant 9 : i32
    %c33_i32 = arith.constant 33 : i32
    %c36_i32 = arith.constant 36 : i32
    %c-32_i32 = arith.constant -32 : i32
    %c-17_i32 = arith.constant -17 : i32
    %c-68_i32 = arith.constant -68 : i32
    %c-11_i32 = arith.constant -11 : i32
    %c-6_i32 = arith.constant -6 : i32
    %c3_i32 = arith.constant 3 : i32
    %c-36_i32 = arith.constant -36 : i32
    %c-46_i32 = arith.constant -46 : i32
    %c2_i32 = arith.constant 2 : i32
    %c6_i32 = arith.constant 6 : i32
    %c-7_i32 = arith.constant -7 : i32
    %c-1_i32 = arith.constant -1 : i32
    %c-15_i32 = arith.constant -15 : i32
    %c-45_i32 = arith.constant -45 : i32
    %c39_i32 = arith.constant 39 : i32
    %c-31_i32 = arith.constant -31 : i32
    %c-5_i32 = arith.constant -5 : i32
    %c-21_i32 = arith.constant -21 : i32
    %c-37_i32 = arith.constant -37 : i32
    %c-28_i32 = arith.constant -28 : i32
    %c23_i32 = arith.constant 23 : i32
    %c-4_i32 = arith.constant -4 : i32
    %c18_i32 = arith.constant 18 : i32
    %c21_i32 = arith.constant 21 : i32
    %c30_i32 = arith.constant 30 : i32
    %c16_i32 = arith.constant 16 : i32
    %c-2_i32 = arith.constant -2 : i32
    %c20_i32 = arith.constant 20 : i32
    %c-38_i32 = arith.constant -38 : i32
    %c28_i32 = arith.constant 28 : i32
    %c-8_i32 = arith.constant -8 : i32
    %c-13_i32 = arith.constant -13 : i32
    %c-30_i32 = arith.constant -30 : i32
    %c-29_i32 = arith.constant -29 : i32
    %c-23_i32 = arith.constant -23 : i32
    %c7_i32 = arith.constant 7 : i32
    %c11_i32 = arith.constant 11 : i32
    %c4_i32 = arith.constant 4 : i32
    %c27_i32 = arith.constant 27 : i32
    %c1_i32 = arith.constant 1 : i32
    %c-34_i32 = arith.constant -34 : i32
    %c-20_i32 = arith.constant -20 : i32
    %c35_i32 = arith.constant 35 : i32
    %c10_i32 = arith.constant 10 : i32
    %c34_i32 = arith.constant 34 : i32
    %c-64_i32 = arith.constant -64 : i32
    %c17_i32 = arith.constant 17 : i32
    %c12_i32 = arith.constant 12 : i32
    %c-27_i32 = arith.constant -27 : i32
    %c-24_i32 = arith.constant -24 : i32
    %c-3_i32 = arith.constant -3 : i32
    %c38_i32 = arith.constant 38 : i32
    %c-25_i32 = arith.constant -25 : i32
    %c-22_i32 = arith.constant -22 : i32
    %c37_i32 = arith.constant 37 : i32
    %c29_i32 = arith.constant 29 : i32
    %c32_i32 = arith.constant 32 : i32
    %c55_i32 = arith.constant 55 : i32
    %c22_i32 = arith.constant 22 : i32
    %c24_i32 = arith.constant 24 : i32
    %c46_i32 = arith.constant 46 : i32
    %c-39_i32 = arith.constant -39 : i32
    %c-40_i32 = arith.constant -40 : i32
    %c19_i32 = arith.constant 19 : i32
    %c-60_i32 = arith.constant -60 : i32
    %c13_i32 = arith.constant 13 : i32
    %c-42_i32 = arith.constant -42 : i32
    %c31_i32 = arith.constant 31 : i32
    %c-41_i32 = arith.constant -41 : i32
    %c-58_i32 = arith.constant -58 : i32
    %c62_i32 = arith.constant 62 : i32
    %c-57_i32 = arith.constant -57 : i32
    %c8_i32 = arith.constant 8 : i32
    %c15_i32 = arith.constant 15 : i32
    %c-18_i32 = arith.constant -18 : i32
    %c41_i32 = arith.constant 41 : i32
    %c88_i32 = arith.constant 88 : i32
    %c59_i32 = arith.constant 59 : i32
    %c-59_i32 = arith.constant -59 : i32
    %0 = arith.extsi %arg0 : i8 to i32
    %1 = arith.subi %0, %c-128_i32 : i32
    %2 = arith.muli %1, %c-9_i32 : i32
    %3 = arith.addi %c0_i32, %2 : i32
    %4 = arith.muli %1, %c-54_i32 : i32
    %5 = arith.addi %c0_i32, %4 : i32
    %6 = arith.muli %1, %c57_i32 : i32
    %7 = arith.addi %c0_i32, %6 : i32
    %8 = arith.muli %1, %c71_i32 : i32
    %9 = arith.addi %c0_i32, %8 : i32
    %10 = arith.muli %1, %c104_i32 : i32
    %11 = arith.addi %c0_i32, %10 : i32
    %12 = arith.muli %1, %c115_i32 : i32
    %13 = arith.addi %c0_i32, %12 : i32
    %14 = arith.muli %1, %c98_i32 : i32
    %15 = arith.addi %c0_i32, %14 : i32
    %16 = arith.muli %1, %c99_i32 : i32
    %17 = arith.addi %c0_i32, %16 : i32
    %18 = arith.muli %1, %c64_i32 : i32
    %19 = arith.addi %c0_i32, %18 : i32
    %20 = arith.muli %1, %c-26_i32 : i32
    %21 = arith.addi %c0_i32, %20 : i32
    %22 = arith.muli %1, %c127_i32 : i32
    %23 = arith.addi %c0_i32, %22 : i32
    %24 = arith.muli %1, %c25_i32 : i32
    %25 = arith.addi %c0_i32, %24 : i32
    %26 = arith.muli %1, %c-82_i32 : i32
    %27 = arith.addi %c0_i32, %26 : i32
    %28 = arith.muli %1, %c68_i32 : i32
    %29 = arith.addi %c0_i32, %28 : i32
    %30 = arith.muli %1, %c95_i32 : i32
    %31 = arith.addi %c0_i32, %30 : i32
    %32 = arith.muli %1, %c86_i32 : i32
    %33 = arith.addi %c0_i32, %32 : i32
    %34 = arith.addi %c0_i32, %3 : i32
    %35 = arith.addi %c0_i32, %5 : i32
    %36 = arith.addi %c-5438_i32, %7 : i32
    %37 = arith.addi %c-5515_i32, %9 : i32
    %38 = arith.addi %c-1352_i32, %11 : i32
    %39 = arith.addi %c-1500_i32, %13 : i32
    %40 = arith.addi %c-4152_i32, %15 : i32
    %41 = arith.addi %c-84_i32, %17 : i32
    %42 = arith.addi %c3396_i32, %19 : i32
    %43 = arith.addi %c0_i32, %21 : i32
    %44 = arith.addi %c1981_i32, %23 : i32
    %45 = arith.addi %c-5581_i32, %25 : i32
    %46 = arith.addi %c0_i32, %27 : i32
    %47 = arith.addi %c-6964_i32, %29 : i32
    %48 = arith.addi %c3407_i32, %31 : i32
    %49 = arith.addi %c-7217_i32, %33 : i32
    %50 = arith.extsi %34 : i32 to i64
    %51 = arith.muli %50, %c2039655736_i64 : i64
    %52 = arith.addi %51, %c137438953472_i64 : i64
    %53 = arith.cmpi sge, %34, %c0_i32 : i32
    cf.cond_br %53, ^bb1, ^bb2
  ^bb1:  // pred: ^bb0
    cf.br ^bb3(%c1073741824_i64 : i64)
  ^bb2:  // pred: ^bb0
    cf.br ^bb3(%c-1073741824_i64 : i64)
  ^bb3(%54: i64):  // 2 preds: ^bb1, ^bb2
    cf.br ^bb4
  ^bb4:  // pred: ^bb3
    %55 = arith.addi %54, %52 : i64
    %56 = arith.shrsi %55, %c38_i64 : i64
    %57 = arith.trunci %56 : i64 to i32
    %58 = arith.addi %57, %c-128_i32 : i32
    %59 = arith.cmpi slt, %58, %c-128_i32 : i32
    cf.cond_br %59, ^bb5, ^bb6
  ^bb5:  // pred: ^bb4
    cf.br ^bb7(%c-128_i32 : i32)
  ^bb6:  // pred: ^bb4
    cf.br ^bb7(%58 : i32)
  ^bb7(%60: i32):  // 2 preds: ^bb5, ^bb6
    cf.br ^bb8
  ^bb8:  // pred: ^bb7
    %61 = arith.cmpi sgt, %58, %c127_i32 : i32
    cf.cond_br %61, ^bb9, ^bb10
  ^bb9:  // pred: ^bb8
    cf.br ^bb11(%c127_i32 : i32)
  ^bb10:  // pred: ^bb8
    cf.br ^bb11(%60 : i32)
  ^bb11(%62: i32):  // 2 preds: ^bb9, ^bb10
    cf.br ^bb12
  ^bb12:  // pred: ^bb11
    %63 = arith.trunci %62 : i32 to i8
    %64 = arith.extsi %35 : i32 to i64
    %65 = arith.muli %64, %c2039655736_i64 : i64
    %66 = arith.addi %65, %c137438953472_i64 : i64
    %67 = arith.cmpi sge, %35, %c0_i32 : i32
    cf.cond_br %67, ^bb13, ^bb14
  ^bb13:  // pred: ^bb12
    cf.br ^bb15(%c1073741824_i64 : i64)
  ^bb14:  // pred: ^bb12
    cf.br ^bb15(%c-1073741824_i64 : i64)
  ^bb15(%68: i64):  // 2 preds: ^bb13, ^bb14
    cf.br ^bb16
  ^bb16:  // pred: ^bb15
    %69 = arith.addi %68, %66 : i64
    %70 = arith.shrsi %69, %c38_i64 : i64
    %71 = arith.trunci %70 : i64 to i32
    %72 = arith.addi %71, %c-128_i32 : i32
    %73 = arith.cmpi slt, %72, %c-128_i32 : i32
    cf.cond_br %73, ^bb17, ^bb18
  ^bb17:  // pred: ^bb16
    cf.br ^bb19(%c-128_i32 : i32)
  ^bb18:  // pred: ^bb16
    cf.br ^bb19(%72 : i32)
  ^bb19(%74: i32):  // 2 preds: ^bb17, ^bb18
    cf.br ^bb20
  ^bb20:  // pred: ^bb19
    %75 = arith.cmpi sgt, %72, %c127_i32 : i32
    cf.cond_br %75, ^bb21, ^bb22
  ^bb21:  // pred: ^bb20
    cf.br ^bb23(%c127_i32 : i32)
  ^bb22:  // pred: ^bb20
    cf.br ^bb23(%74 : i32)
  ^bb23(%76: i32):  // 2 preds: ^bb21, ^bb22
    cf.br ^bb24
  ^bb24:  // pred: ^bb23
    %77 = arith.trunci %76 : i32 to i8
    %78 = arith.extsi %36 : i32 to i64
    %79 = arith.muli %78, %c2039655736_i64 : i64
    %80 = arith.addi %79, %c137438953472_i64 : i64
    %81 = arith.cmpi sge, %36, %c0_i32 : i32
    cf.cond_br %81, ^bb25, ^bb26
  ^bb25:  // pred: ^bb24
    cf.br ^bb27(%c1073741824_i64 : i64)
  ^bb26:  // pred: ^bb24
    cf.br ^bb27(%c-1073741824_i64 : i64)
  ^bb27(%82: i64):  // 2 preds: ^bb25, ^bb26
    cf.br ^bb28
  ^bb28:  // pred: ^bb27
    %83 = arith.addi %82, %80 : i64
    %84 = arith.shrsi %83, %c38_i64 : i64
    %85 = arith.trunci %84 : i64 to i32
    %86 = arith.addi %85, %c-128_i32 : i32
    %87 = arith.cmpi slt, %86, %c-128_i32 : i32
    cf.cond_br %87, ^bb29, ^bb30
  ^bb29:  // pred: ^bb28
    cf.br ^bb31(%c-128_i32 : i32)
  ^bb30:  // pred: ^bb28
    cf.br ^bb31(%86 : i32)
  ^bb31(%88: i32):  // 2 preds: ^bb29, ^bb30
    cf.br ^bb32
  ^bb32:  // pred: ^bb31
    %89 = arith.cmpi sgt, %86, %c127_i32 : i32
    cf.cond_br %89, ^bb33, ^bb34
  ^bb33:  // pred: ^bb32
    cf.br ^bb35(%c127_i32 : i32)
  ^bb34:  // pred: ^bb32
    cf.br ^bb35(%88 : i32)
  ^bb35(%90: i32):  // 2 preds: ^bb33, ^bb34
    cf.br ^bb36
  ^bb36:  // pred: ^bb35
    %91 = arith.trunci %90 : i32 to i8
    %92 = arith.extsi %37 : i32 to i64
    %93 = arith.muli %92, %c2039655736_i64 : i64
    %94 = arith.addi %93, %c137438953472_i64 : i64
    %95 = arith.cmpi sge, %37, %c0_i32 : i32
    cf.cond_br %95, ^bb37, ^bb38
  ^bb37:  // pred: ^bb36
    cf.br ^bb39(%c1073741824_i64 : i64)
  ^bb38:  // pred: ^bb36
    cf.br ^bb39(%c-1073741824_i64 : i64)
  ^bb39(%96: i64):  // 2 preds: ^bb37, ^bb38
    cf.br ^bb40
  ^bb40:  // pred: ^bb39
    %97 = arith.addi %96, %94 : i64
    %98 = arith.shrsi %97, %c38_i64 : i64
    %99 = arith.trunci %98 : i64 to i32
    %100 = arith.addi %99, %c-128_i32 : i32
    %101 = arith.cmpi slt, %100, %c-128_i32 : i32
    cf.cond_br %101, ^bb41, ^bb42
  ^bb41:  // pred: ^bb40
    cf.br ^bb43(%c-128_i32 : i32)
  ^bb42:  // pred: ^bb40
    cf.br ^bb43(%100 : i32)
  ^bb43(%102: i32):  // 2 preds: ^bb41, ^bb42
    cf.br ^bb44
  ^bb44:  // pred: ^bb43
    %103 = arith.cmpi sgt, %100, %c127_i32 : i32
    cf.cond_br %103, ^bb45, ^bb46
  ^bb45:  // pred: ^bb44
    cf.br ^bb47(%c127_i32 : i32)
  ^bb46:  // pred: ^bb44
    cf.br ^bb47(%102 : i32)
  ^bb47(%104: i32):  // 2 preds: ^bb45, ^bb46
    cf.br ^bb48
  ^bb48:  // pred: ^bb47
    %105 = arith.trunci %104 : i32 to i8
    %106 = arith.extsi %38 : i32 to i64
    %107 = arith.muli %106, %c2039655736_i64 : i64
    %108 = arith.addi %107, %c137438953472_i64 : i64
    %109 = arith.cmpi sge, %38, %c0_i32 : i32
    cf.cond_br %109, ^bb49, ^bb50
  ^bb49:  // pred: ^bb48
    cf.br ^bb51(%c1073741824_i64 : i64)
  ^bb50:  // pred: ^bb48
    cf.br ^bb51(%c-1073741824_i64 : i64)
  ^bb51(%110: i64):  // 2 preds: ^bb49, ^bb50
    cf.br ^bb52
  ^bb52:  // pred: ^bb51
    %111 = arith.addi %110, %108 : i64
    %112 = arith.shrsi %111, %c38_i64 : i64
    %113 = arith.trunci %112 : i64 to i32
    %114 = arith.addi %113, %c-128_i32 : i32
    %115 = arith.cmpi slt, %114, %c-128_i32 : i32
    cf.cond_br %115, ^bb53, ^bb54
  ^bb53:  // pred: ^bb52
    cf.br ^bb55(%c-128_i32 : i32)
  ^bb54:  // pred: ^bb52
    cf.br ^bb55(%114 : i32)
  ^bb55(%116: i32):  // 2 preds: ^bb53, ^bb54
    cf.br ^bb56
  ^bb56:  // pred: ^bb55
    %117 = arith.cmpi sgt, %114, %c127_i32 : i32
    cf.cond_br %117, ^bb57, ^bb58
  ^bb57:  // pred: ^bb56
    cf.br ^bb59(%c127_i32 : i32)
  ^bb58:  // pred: ^bb56
    cf.br ^bb59(%116 : i32)
  ^bb59(%118: i32):  // 2 preds: ^bb57, ^bb58
    cf.br ^bb60
  ^bb60:  // pred: ^bb59
    %119 = arith.trunci %118 : i32 to i8
    %120 = arith.extsi %39 : i32 to i64
    %121 = arith.muli %120, %c2039655736_i64 : i64
    %122 = arith.addi %121, %c137438953472_i64 : i64
    %123 = arith.cmpi sge, %39, %c0_i32 : i32
    cf.cond_br %123, ^bb61, ^bb62
  ^bb61:  // pred: ^bb60
    cf.br ^bb63(%c1073741824_i64 : i64)
  ^bb62:  // pred: ^bb60
    cf.br ^bb63(%c-1073741824_i64 : i64)
  ^bb63(%124: i64):  // 2 preds: ^bb61, ^bb62
    cf.br ^bb64
  ^bb64:  // pred: ^bb63
    %125 = arith.addi %124, %122 : i64
    %126 = arith.shrsi %125, %c38_i64 : i64
    %127 = arith.trunci %126 : i64 to i32
    %128 = arith.addi %127, %c-128_i32 : i32
    %129 = arith.cmpi slt, %128, %c-128_i32 : i32
    cf.cond_br %129, ^bb65, ^bb66
  ^bb65:  // pred: ^bb64
    cf.br ^bb67(%c-128_i32 : i32)
  ^bb66:  // pred: ^bb64
    cf.br ^bb67(%128 : i32)
  ^bb67(%130: i32):  // 2 preds: ^bb65, ^bb66
    cf.br ^bb68
  ^bb68:  // pred: ^bb67
    %131 = arith.cmpi sgt, %128, %c127_i32 : i32
    cf.cond_br %131, ^bb69, ^bb70
  ^bb69:  // pred: ^bb68
    cf.br ^bb71(%c127_i32 : i32)
  ^bb70:  // pred: ^bb68
    cf.br ^bb71(%130 : i32)
  ^bb71(%132: i32):  // 2 preds: ^bb69, ^bb70
    cf.br ^bb72
  ^bb72:  // pred: ^bb71
    %133 = arith.trunci %132 : i32 to i8
    %134 = arith.extsi %40 : i32 to i64
    %135 = arith.muli %134, %c2039655736_i64 : i64
    %136 = arith.addi %135, %c137438953472_i64 : i64
    %137 = arith.cmpi sge, %40, %c0_i32 : i32
    cf.cond_br %137, ^bb73, ^bb74
  ^bb73:  // pred: ^bb72
    cf.br ^bb75(%c1073741824_i64 : i64)
  ^bb74:  // pred: ^bb72
    cf.br ^bb75(%c-1073741824_i64 : i64)
  ^bb75(%138: i64):  // 2 preds: ^bb73, ^bb74
    cf.br ^bb76
  ^bb76:  // pred: ^bb75
    %139 = arith.addi %138, %136 : i64
    %140 = arith.shrsi %139, %c38_i64 : i64
    %141 = arith.trunci %140 : i64 to i32
    %142 = arith.addi %141, %c-128_i32 : i32
    %143 = arith.cmpi slt, %142, %c-128_i32 : i32
    cf.cond_br %143, ^bb77, ^bb78
  ^bb77:  // pred: ^bb76
    cf.br ^bb79(%c-128_i32 : i32)
  ^bb78:  // pred: ^bb76
    cf.br ^bb79(%142 : i32)
  ^bb79(%144: i32):  // 2 preds: ^bb77, ^bb78
    cf.br ^bb80
  ^bb80:  // pred: ^bb79
    %145 = arith.cmpi sgt, %142, %c127_i32 : i32
    cf.cond_br %145, ^bb81, ^bb82
  ^bb81:  // pred: ^bb80
    cf.br ^bb83(%c127_i32 : i32)
  ^bb82:  // pred: ^bb80
    cf.br ^bb83(%144 : i32)
  ^bb83(%146: i32):  // 2 preds: ^bb81, ^bb82
    cf.br ^bb84
  ^bb84:  // pred: ^bb83
    %147 = arith.trunci %146 : i32 to i8
    %148 = arith.extsi %41 : i32 to i64
    %149 = arith.muli %148, %c2039655736_i64 : i64
    %150 = arith.addi %149, %c137438953472_i64 : i64
    %151 = arith.cmpi sge, %41, %c0_i32 : i32
    cf.cond_br %151, ^bb85, ^bb86
  ^bb85:  // pred: ^bb84
    cf.br ^bb87(%c1073741824_i64 : i64)
  ^bb86:  // pred: ^bb84
    cf.br ^bb87(%c-1073741824_i64 : i64)
  ^bb87(%152: i64):  // 2 preds: ^bb85, ^bb86
    cf.br ^bb88
  ^bb88:  // pred: ^bb87
    %153 = arith.addi %152, %150 : i64
    %154 = arith.shrsi %153, %c38_i64 : i64
    %155 = arith.trunci %154 : i64 to i32
    %156 = arith.addi %155, %c-128_i32 : i32
    %157 = arith.cmpi slt, %156, %c-128_i32 : i32
    cf.cond_br %157, ^bb89, ^bb90
  ^bb89:  // pred: ^bb88
    cf.br ^bb91(%c-128_i32 : i32)
  ^bb90:  // pred: ^bb88
    cf.br ^bb91(%156 : i32)
  ^bb91(%158: i32):  // 2 preds: ^bb89, ^bb90
    cf.br ^bb92
  ^bb92:  // pred: ^bb91
    %159 = arith.cmpi sgt, %156, %c127_i32 : i32
    cf.cond_br %159, ^bb93, ^bb94
  ^bb93:  // pred: ^bb92
    cf.br ^bb95(%c127_i32 : i32)
  ^bb94:  // pred: ^bb92
    cf.br ^bb95(%158 : i32)
  ^bb95(%160: i32):  // 2 preds: ^bb93, ^bb94
    cf.br ^bb96
  ^bb96:  // pred: ^bb95
    %161 = arith.trunci %160 : i32 to i8
    %162 = arith.extsi %42 : i32 to i64
    %163 = arith.muli %162, %c2039655736_i64 : i64
    %164 = arith.addi %163, %c137438953472_i64 : i64
    %165 = arith.cmpi sge, %42, %c0_i32 : i32
    cf.cond_br %165, ^bb97, ^bb98
  ^bb97:  // pred: ^bb96
    cf.br ^bb99(%c1073741824_i64 : i64)
  ^bb98:  // pred: ^bb96
    cf.br ^bb99(%c-1073741824_i64 : i64)
  ^bb99(%166: i64):  // 2 preds: ^bb97, ^bb98
    cf.br ^bb100
  ^bb100:  // pred: ^bb99
    %167 = arith.addi %166, %164 : i64
    %168 = arith.shrsi %167, %c38_i64 : i64
    %169 = arith.trunci %168 : i64 to i32
    %170 = arith.addi %169, %c-128_i32 : i32
    %171 = arith.cmpi slt, %170, %c-128_i32 : i32
    cf.cond_br %171, ^bb101, ^bb102
  ^bb101:  // pred: ^bb100
    cf.br ^bb103(%c-128_i32 : i32)
  ^bb102:  // pred: ^bb100
    cf.br ^bb103(%170 : i32)
  ^bb103(%172: i32):  // 2 preds: ^bb101, ^bb102
    cf.br ^bb104
  ^bb104:  // pred: ^bb103
    %173 = arith.cmpi sgt, %170, %c127_i32 : i32
    cf.cond_br %173, ^bb105, ^bb106
  ^bb105:  // pred: ^bb104
    cf.br ^bb107(%c127_i32 : i32)
  ^bb106:  // pred: ^bb104
    cf.br ^bb107(%172 : i32)
  ^bb107(%174: i32):  // 2 preds: ^bb105, ^bb106
    cf.br ^bb108
  ^bb108:  // pred: ^bb107
    %175 = arith.trunci %174 : i32 to i8
    %176 = arith.extsi %43 : i32 to i64
    %177 = arith.muli %176, %c2039655736_i64 : i64
    %178 = arith.addi %177, %c137438953472_i64 : i64
    %179 = arith.cmpi sge, %43, %c0_i32 : i32
    cf.cond_br %179, ^bb109, ^bb110
  ^bb109:  // pred: ^bb108
    cf.br ^bb111(%c1073741824_i64 : i64)
  ^bb110:  // pred: ^bb108
    cf.br ^bb111(%c-1073741824_i64 : i64)
  ^bb111(%180: i64):  // 2 preds: ^bb109, ^bb110
    cf.br ^bb112
  ^bb112:  // pred: ^bb111
    %181 = arith.addi %180, %178 : i64
    %182 = arith.shrsi %181, %c38_i64 : i64
    %183 = arith.trunci %182 : i64 to i32
    %184 = arith.addi %183, %c-128_i32 : i32
    %185 = arith.cmpi slt, %184, %c-128_i32 : i32
    cf.cond_br %185, ^bb113, ^bb114
  ^bb113:  // pred: ^bb112
    cf.br ^bb115(%c-128_i32 : i32)
  ^bb114:  // pred: ^bb112
    cf.br ^bb115(%184 : i32)
  ^bb115(%186: i32):  // 2 preds: ^bb113, ^bb114
    cf.br ^bb116
  ^bb116:  // pred: ^bb115
    %187 = arith.cmpi sgt, %184, %c127_i32 : i32
    cf.cond_br %187, ^bb117, ^bb118
  ^bb117:  // pred: ^bb116
    cf.br ^bb119(%c127_i32 : i32)
  ^bb118:  // pred: ^bb116
    cf.br ^bb119(%186 : i32)
  ^bb119(%188: i32):  // 2 preds: ^bb117, ^bb118
    cf.br ^bb120
  ^bb120:  // pred: ^bb119
    %189 = arith.trunci %188 : i32 to i8
    %190 = arith.extsi %44 : i32 to i64
    %191 = arith.muli %190, %c2039655736_i64 : i64
    %192 = arith.addi %191, %c137438953472_i64 : i64
    %193 = arith.cmpi sge, %44, %c0_i32 : i32
    cf.cond_br %193, ^bb121, ^bb122
  ^bb121:  // pred: ^bb120
    cf.br ^bb123(%c1073741824_i64 : i64)
  ^bb122:  // pred: ^bb120
    cf.br ^bb123(%c-1073741824_i64 : i64)
  ^bb123(%194: i64):  // 2 preds: ^bb121, ^bb122
    cf.br ^bb124
  ^bb124:  // pred: ^bb123
    %195 = arith.addi %194, %192 : i64
    %196 = arith.shrsi %195, %c38_i64 : i64
    %197 = arith.trunci %196 : i64 to i32
    %198 = arith.addi %197, %c-128_i32 : i32
    %199 = arith.cmpi slt, %198, %c-128_i32 : i32
    cf.cond_br %199, ^bb125, ^bb126
  ^bb125:  // pred: ^bb124
    cf.br ^bb127(%c-128_i32 : i32)
  ^bb126:  // pred: ^bb124
    cf.br ^bb127(%198 : i32)
  ^bb127(%200: i32):  // 2 preds: ^bb125, ^bb126
    cf.br ^bb128
  ^bb128:  // pred: ^bb127
    %201 = arith.cmpi sgt, %198, %c127_i32 : i32
    cf.cond_br %201, ^bb129, ^bb130
  ^bb129:  // pred: ^bb128
    cf.br ^bb131(%c127_i32 : i32)
  ^bb130:  // pred: ^bb128
    cf.br ^bb131(%200 : i32)
  ^bb131(%202: i32):  // 2 preds: ^bb129, ^bb130
    cf.br ^bb132
  ^bb132:  // pred: ^bb131
    %203 = arith.trunci %202 : i32 to i8
    %204 = arith.extsi %45 : i32 to i64
    %205 = arith.muli %204, %c2039655736_i64 : i64
    %206 = arith.addi %205, %c137438953472_i64 : i64
    %207 = arith.cmpi sge, %45, %c0_i32 : i32
    cf.cond_br %207, ^bb133, ^bb134
  ^bb133:  // pred: ^bb132
    cf.br ^bb135(%c1073741824_i64 : i64)
  ^bb134:  // pred: ^bb132
    cf.br ^bb135(%c-1073741824_i64 : i64)
  ^bb135(%208: i64):  // 2 preds: ^bb133, ^bb134
    cf.br ^bb136
  ^bb136:  // pred: ^bb135
    %209 = arith.addi %208, %206 : i64
    %210 = arith.shrsi %209, %c38_i64 : i64
    %211 = arith.trunci %210 : i64 to i32
    %212 = arith.addi %211, %c-128_i32 : i32
    %213 = arith.cmpi slt, %212, %c-128_i32 : i32
    cf.cond_br %213, ^bb137, ^bb138
  ^bb137:  // pred: ^bb136
    cf.br ^bb139(%c-128_i32 : i32)
  ^bb138:  // pred: ^bb136
    cf.br ^bb139(%212 : i32)
  ^bb139(%214: i32):  // 2 preds: ^bb137, ^bb138
    cf.br ^bb140
  ^bb140:  // pred: ^bb139
    %215 = arith.cmpi sgt, %212, %c127_i32 : i32
    cf.cond_br %215, ^bb141, ^bb142
  ^bb141:  // pred: ^bb140
    cf.br ^bb143(%c127_i32 : i32)
  ^bb142:  // pred: ^bb140
    cf.br ^bb143(%214 : i32)
  ^bb143(%216: i32):  // 2 preds: ^bb141, ^bb142
    cf.br ^bb144
  ^bb144:  // pred: ^bb143
    %217 = arith.trunci %216 : i32 to i8
    %218 = arith.extsi %46 : i32 to i64
    %219 = arith.muli %218, %c2039655736_i64 : i64
    %220 = arith.addi %219, %c137438953472_i64 : i64
    %221 = arith.cmpi sge, %46, %c0_i32 : i32
    cf.cond_br %221, ^bb145, ^bb146
  ^bb145:  // pred: ^bb144
    cf.br ^bb147(%c1073741824_i64 : i64)
  ^bb146:  // pred: ^bb144
    cf.br ^bb147(%c-1073741824_i64 : i64)
  ^bb147(%222: i64):  // 2 preds: ^bb145, ^bb146
    cf.br ^bb148
  ^bb148:  // pred: ^bb147
    %223 = arith.addi %222, %220 : i64
    %224 = arith.shrsi %223, %c38_i64 : i64
    %225 = arith.trunci %224 : i64 to i32
    %226 = arith.addi %225, %c-128_i32 : i32
    %227 = arith.cmpi slt, %226, %c-128_i32 : i32
    cf.cond_br %227, ^bb149, ^bb150
  ^bb149:  // pred: ^bb148
    cf.br ^bb151(%c-128_i32 : i32)
  ^bb150:  // pred: ^bb148
    cf.br ^bb151(%226 : i32)
  ^bb151(%228: i32):  // 2 preds: ^bb149, ^bb150
    cf.br ^bb152
  ^bb152:  // pred: ^bb151
    %229 = arith.cmpi sgt, %226, %c127_i32 : i32
    cf.cond_br %229, ^bb153, ^bb154
  ^bb153:  // pred: ^bb152
    cf.br ^bb155(%c127_i32 : i32)
  ^bb154:  // pred: ^bb152
    cf.br ^bb155(%228 : i32)
  ^bb155(%230: i32):  // 2 preds: ^bb153, ^bb154
    cf.br ^bb156
  ^bb156:  // pred: ^bb155
    %231 = arith.trunci %230 : i32 to i8
    %232 = arith.extsi %47 : i32 to i64
    %233 = arith.muli %232, %c2039655736_i64 : i64
    %234 = arith.addi %233, %c137438953472_i64 : i64
    %235 = arith.cmpi sge, %47, %c0_i32 : i32
    cf.cond_br %235, ^bb157, ^bb158
  ^bb157:  // pred: ^bb156
    cf.br ^bb159(%c1073741824_i64 : i64)
  ^bb158:  // pred: ^bb156
    cf.br ^bb159(%c-1073741824_i64 : i64)
  ^bb159(%236: i64):  // 2 preds: ^bb157, ^bb158
    cf.br ^bb160
  ^bb160:  // pred: ^bb159
    %237 = arith.addi %236, %234 : i64
    %238 = arith.shrsi %237, %c38_i64 : i64
    %239 = arith.trunci %238 : i64 to i32
    %240 = arith.addi %239, %c-128_i32 : i32
    %241 = arith.cmpi slt, %240, %c-128_i32 : i32
    cf.cond_br %241, ^bb161, ^bb162
  ^bb161:  // pred: ^bb160
    cf.br ^bb163(%c-128_i32 : i32)
  ^bb162:  // pred: ^bb160
    cf.br ^bb163(%240 : i32)
  ^bb163(%242: i32):  // 2 preds: ^bb161, ^bb162
    cf.br ^bb164
  ^bb164:  // pred: ^bb163
    %243 = arith.cmpi sgt, %240, %c127_i32 : i32
    cf.cond_br %243, ^bb165, ^bb166
  ^bb165:  // pred: ^bb164
    cf.br ^bb167(%c127_i32 : i32)
  ^bb166:  // pred: ^bb164
    cf.br ^bb167(%242 : i32)
  ^bb167(%244: i32):  // 2 preds: ^bb165, ^bb166
    cf.br ^bb168
  ^bb168:  // pred: ^bb167
    %245 = arith.trunci %244 : i32 to i8
    %246 = arith.extsi %48 : i32 to i64
    %247 = arith.muli %246, %c2039655736_i64 : i64
    %248 = arith.addi %247, %c137438953472_i64 : i64
    %249 = arith.cmpi sge, %48, %c0_i32 : i32
    cf.cond_br %249, ^bb169, ^bb170
  ^bb169:  // pred: ^bb168
    cf.br ^bb171(%c1073741824_i64 : i64)
  ^bb170:  // pred: ^bb168
    cf.br ^bb171(%c-1073741824_i64 : i64)
  ^bb171(%250: i64):  // 2 preds: ^bb169, ^bb170
    cf.br ^bb172
  ^bb172:  // pred: ^bb171
    %251 = arith.addi %250, %248 : i64
    %252 = arith.shrsi %251, %c38_i64 : i64
    %253 = arith.trunci %252 : i64 to i32
    %254 = arith.addi %253, %c-128_i32 : i32
    %255 = arith.cmpi slt, %254, %c-128_i32 : i32
    cf.cond_br %255, ^bb173, ^bb174
  ^bb173:  // pred: ^bb172
    cf.br ^bb175(%c-128_i32 : i32)
  ^bb174:  // pred: ^bb172
    cf.br ^bb175(%254 : i32)
  ^bb175(%256: i32):  // 2 preds: ^bb173, ^bb174
    cf.br ^bb176
  ^bb176:  // pred: ^bb175
    %257 = arith.cmpi sgt, %254, %c127_i32 : i32
    cf.cond_br %257, ^bb177, ^bb178
  ^bb177:  // pred: ^bb176
    cf.br ^bb179(%c127_i32 : i32)
  ^bb178:  // pred: ^bb176
    cf.br ^bb179(%256 : i32)
  ^bb179(%258: i32):  // 2 preds: ^bb177, ^bb178
    cf.br ^bb180
  ^bb180:  // pred: ^bb179
    %259 = arith.trunci %258 : i32 to i8
    %260 = arith.extsi %49 : i32 to i64
    %261 = arith.muli %260, %c2039655736_i64 : i64
    %262 = arith.addi %261, %c137438953472_i64 : i64
    %263 = arith.cmpi sge, %49, %c0_i32 : i32
    cf.cond_br %263, ^bb181, ^bb182
  ^bb181:  // pred: ^bb180
    cf.br ^bb183(%c1073741824_i64 : i64)
  ^bb182:  // pred: ^bb180
    cf.br ^bb183(%c-1073741824_i64 : i64)
  ^bb183(%264: i64):  // 2 preds: ^bb181, ^bb182
    cf.br ^bb184
  ^bb184:  // pred: ^bb183
    %265 = arith.addi %264, %262 : i64
    %266 = arith.shrsi %265, %c38_i64 : i64
    %267 = arith.trunci %266 : i64 to i32
    %268 = arith.addi %267, %c-128_i32 : i32
    %269 = arith.cmpi slt, %268, %c-128_i32 : i32
    cf.cond_br %269, ^bb185, ^bb186
  ^bb185:  // pred: ^bb184
    cf.br ^bb187(%c-128_i32 : i32)
  ^bb186:  // pred: ^bb184
    cf.br ^bb187(%268 : i32)
  ^bb187(%270: i32):  // 2 preds: ^bb185, ^bb186
    cf.br ^bb188
  ^bb188:  // pred: ^bb187
    %271 = arith.cmpi sgt, %268, %c127_i32 : i32
    cf.cond_br %271, ^bb189, ^bb190
  ^bb189:  // pred: ^bb188
    cf.br ^bb191(%c127_i32 : i32)
  ^bb190:  // pred: ^bb188
    cf.br ^bb191(%270 : i32)
  ^bb191(%272: i32):  // 2 preds: ^bb189, ^bb190
    cf.br ^bb192
  ^bb192:  // pred: ^bb191
    %273 = arith.trunci %272 : i32 to i8
    %274 = arith.cmpi slt, %63, %c-128_i8 : i8
    cf.cond_br %274, ^bb193, ^bb194
  ^bb193:  // pred: ^bb192
    cf.br ^bb195(%c-128_i8 : i8)
  ^bb194:  // pred: ^bb192
    cf.br ^bb195(%63 : i8)
  ^bb195(%275: i8):  // 2 preds: ^bb193, ^bb194
    cf.br ^bb196
  ^bb196:  // pred: ^bb195
    %276 = arith.cmpi sgt, %63, %c127_i8 : i8
    cf.cond_br %276, ^bb197, ^bb198
  ^bb197:  // pred: ^bb196
    cf.br ^bb199(%c127_i8 : i8)
  ^bb198:  // pred: ^bb196
    cf.br ^bb199(%275 : i8)
  ^bb199(%277: i8):  // 2 preds: ^bb197, ^bb198
    cf.br ^bb200
  ^bb200:  // pred: ^bb199
    %278 = arith.cmpi slt, %77, %c-128_i8 : i8
    cf.cond_br %278, ^bb201, ^bb202
  ^bb201:  // pred: ^bb200
    cf.br ^bb203(%c-128_i8 : i8)
  ^bb202:  // pred: ^bb200
    cf.br ^bb203(%77 : i8)
  ^bb203(%279: i8):  // 2 preds: ^bb201, ^bb202
    cf.br ^bb204
  ^bb204:  // pred: ^bb203
    %280 = arith.cmpi sgt, %77, %c127_i8 : i8
    cf.cond_br %280, ^bb205, ^bb206
  ^bb205:  // pred: ^bb204
    cf.br ^bb207(%c127_i8 : i8)
  ^bb206:  // pred: ^bb204
    cf.br ^bb207(%279 : i8)
  ^bb207(%281: i8):  // 2 preds: ^bb205, ^bb206
    cf.br ^bb208
  ^bb208:  // pred: ^bb207
    %282 = arith.cmpi slt, %91, %c-128_i8 : i8
    cf.cond_br %282, ^bb209, ^bb210
  ^bb209:  // pred: ^bb208
    cf.br ^bb211(%c-128_i8 : i8)
  ^bb210:  // pred: ^bb208
    cf.br ^bb211(%91 : i8)
  ^bb211(%283: i8):  // 2 preds: ^bb209, ^bb210
    cf.br ^bb212
  ^bb212:  // pred: ^bb211
    %284 = arith.cmpi sgt, %91, %c127_i8 : i8
    cf.cond_br %284, ^bb213, ^bb214
  ^bb213:  // pred: ^bb212
    cf.br ^bb215(%c127_i8 : i8)
  ^bb214:  // pred: ^bb212
    cf.br ^bb215(%283 : i8)
  ^bb215(%285: i8):  // 2 preds: ^bb213, ^bb214
    cf.br ^bb216
  ^bb216:  // pred: ^bb215
    %286 = arith.cmpi slt, %105, %c-128_i8 : i8
    cf.cond_br %286, ^bb217, ^bb218
  ^bb217:  // pred: ^bb216
    cf.br ^bb219(%c-128_i8 : i8)
  ^bb218:  // pred: ^bb216
    cf.br ^bb219(%105 : i8)
  ^bb219(%287: i8):  // 2 preds: ^bb217, ^bb218
    cf.br ^bb220
  ^bb220:  // pred: ^bb219
    %288 = arith.cmpi sgt, %105, %c127_i8 : i8
    cf.cond_br %288, ^bb221, ^bb222
  ^bb221:  // pred: ^bb220
    cf.br ^bb223(%c127_i8 : i8)
  ^bb222:  // pred: ^bb220
    cf.br ^bb223(%287 : i8)
  ^bb223(%289: i8):  // 2 preds: ^bb221, ^bb222
    cf.br ^bb224
  ^bb224:  // pred: ^bb223
    %290 = arith.cmpi slt, %119, %c-128_i8 : i8
    cf.cond_br %290, ^bb225, ^bb226
  ^bb225:  // pred: ^bb224
    cf.br ^bb227(%c-128_i8 : i8)
  ^bb226:  // pred: ^bb224
    cf.br ^bb227(%119 : i8)
  ^bb227(%291: i8):  // 2 preds: ^bb225, ^bb226
    cf.br ^bb228
  ^bb228:  // pred: ^bb227
    %292 = arith.cmpi sgt, %119, %c127_i8 : i8
    cf.cond_br %292, ^bb229, ^bb230
  ^bb229:  // pred: ^bb228
    cf.br ^bb231(%c127_i8 : i8)
  ^bb230:  // pred: ^bb228
    cf.br ^bb231(%291 : i8)
  ^bb231(%293: i8):  // 2 preds: ^bb229, ^bb230
    cf.br ^bb232
  ^bb232:  // pred: ^bb231
    %294 = arith.cmpi slt, %133, %c-128_i8 : i8
    cf.cond_br %294, ^bb233, ^bb234
  ^bb233:  // pred: ^bb232
    cf.br ^bb235(%c-128_i8 : i8)
  ^bb234:  // pred: ^bb232
    cf.br ^bb235(%133 : i8)
  ^bb235(%295: i8):  // 2 preds: ^bb233, ^bb234
    cf.br ^bb236
  ^bb236:  // pred: ^bb235
    %296 = arith.cmpi sgt, %133, %c127_i8 : i8
    cf.cond_br %296, ^bb237, ^bb238
  ^bb237:  // pred: ^bb236
    cf.br ^bb239(%c127_i8 : i8)
  ^bb238:  // pred: ^bb236
    cf.br ^bb239(%295 : i8)
  ^bb239(%297: i8):  // 2 preds: ^bb237, ^bb238
    cf.br ^bb240
  ^bb240:  // pred: ^bb239
    %298 = arith.cmpi slt, %147, %c-128_i8 : i8
    cf.cond_br %298, ^bb241, ^bb242
  ^bb241:  // pred: ^bb240
    cf.br ^bb243(%c-128_i8 : i8)
  ^bb242:  // pred: ^bb240
    cf.br ^bb243(%147 : i8)
  ^bb243(%299: i8):  // 2 preds: ^bb241, ^bb242
    cf.br ^bb244
  ^bb244:  // pred: ^bb243
    %300 = arith.cmpi sgt, %147, %c127_i8 : i8
    cf.cond_br %300, ^bb245, ^bb246
  ^bb245:  // pred: ^bb244
    cf.br ^bb247(%c127_i8 : i8)
  ^bb246:  // pred: ^bb244
    cf.br ^bb247(%299 : i8)
  ^bb247(%301: i8):  // 2 preds: ^bb245, ^bb246
    cf.br ^bb248
  ^bb248:  // pred: ^bb247
    %302 = arith.cmpi slt, %161, %c-128_i8 : i8
    cf.cond_br %302, ^bb249, ^bb250
  ^bb249:  // pred: ^bb248
    cf.br ^bb251(%c-128_i8 : i8)
  ^bb250:  // pred: ^bb248
    cf.br ^bb251(%161 : i8)
  ^bb251(%303: i8):  // 2 preds: ^bb249, ^bb250
    cf.br ^bb252
  ^bb252:  // pred: ^bb251
    %304 = arith.cmpi sgt, %161, %c127_i8 : i8
    cf.cond_br %304, ^bb253, ^bb254
  ^bb253:  // pred: ^bb252
    cf.br ^bb255(%c127_i8 : i8)
  ^bb254:  // pred: ^bb252
    cf.br ^bb255(%303 : i8)
  ^bb255(%305: i8):  // 2 preds: ^bb253, ^bb254
    cf.br ^bb256
  ^bb256:  // pred: ^bb255
    %306 = arith.cmpi slt, %175, %c-128_i8 : i8
    cf.cond_br %306, ^bb257, ^bb258
  ^bb257:  // pred: ^bb256
    cf.br ^bb259(%c-128_i8 : i8)
  ^bb258:  // pred: ^bb256
    cf.br ^bb259(%175 : i8)
  ^bb259(%307: i8):  // 2 preds: ^bb257, ^bb258
    cf.br ^bb260
  ^bb260:  // pred: ^bb259
    %308 = arith.cmpi sgt, %175, %c127_i8 : i8
    cf.cond_br %308, ^bb261, ^bb262
  ^bb261:  // pred: ^bb260
    cf.br ^bb263(%c127_i8 : i8)
  ^bb262:  // pred: ^bb260
    cf.br ^bb263(%307 : i8)
  ^bb263(%309: i8):  // 2 preds: ^bb261, ^bb262
    cf.br ^bb264
  ^bb264:  // pred: ^bb263
    %310 = arith.cmpi slt, %189, %c-128_i8 : i8
    cf.cond_br %310, ^bb265, ^bb266
  ^bb265:  // pred: ^bb264
    cf.br ^bb267(%c-128_i8 : i8)
  ^bb266:  // pred: ^bb264
    cf.br ^bb267(%189 : i8)
  ^bb267(%311: i8):  // 2 preds: ^bb265, ^bb266
    cf.br ^bb268
  ^bb268:  // pred: ^bb267
    %312 = arith.cmpi sgt, %189, %c127_i8 : i8
    cf.cond_br %312, ^bb269, ^bb270
  ^bb269:  // pred: ^bb268
    cf.br ^bb271(%c127_i8 : i8)
  ^bb270:  // pred: ^bb268
    cf.br ^bb271(%311 : i8)
  ^bb271(%313: i8):  // 2 preds: ^bb269, ^bb270
    cf.br ^bb272
  ^bb272:  // pred: ^bb271
    %314 = arith.cmpi slt, %203, %c-128_i8 : i8
    cf.cond_br %314, ^bb273, ^bb274
  ^bb273:  // pred: ^bb272
    cf.br ^bb275(%c-128_i8 : i8)
  ^bb274:  // pred: ^bb272
    cf.br ^bb275(%203 : i8)
  ^bb275(%315: i8):  // 2 preds: ^bb273, ^bb274
    cf.br ^bb276
  ^bb276:  // pred: ^bb275
    %316 = arith.cmpi sgt, %203, %c127_i8 : i8
    cf.cond_br %316, ^bb277, ^bb278
  ^bb277:  // pred: ^bb276
    cf.br ^bb279(%c127_i8 : i8)
  ^bb278:  // pred: ^bb276
    cf.br ^bb279(%315 : i8)
  ^bb279(%317: i8):  // 2 preds: ^bb277, ^bb278
    cf.br ^bb280
  ^bb280:  // pred: ^bb279
    %318 = arith.cmpi slt, %217, %c-128_i8 : i8
    cf.cond_br %318, ^bb281, ^bb282
  ^bb281:  // pred: ^bb280
    cf.br ^bb283(%c-128_i8 : i8)
  ^bb282:  // pred: ^bb280
    cf.br ^bb283(%217 : i8)
  ^bb283(%319: i8):  // 2 preds: ^bb281, ^bb282
    cf.br ^bb284
  ^bb284:  // pred: ^bb283
    %320 = arith.cmpi sgt, %217, %c127_i8 : i8
    cf.cond_br %320, ^bb285, ^bb286
  ^bb285:  // pred: ^bb284
    cf.br ^bb287(%c127_i8 : i8)
  ^bb286:  // pred: ^bb284
    cf.br ^bb287(%319 : i8)
  ^bb287(%321: i8):  // 2 preds: ^bb285, ^bb286
    cf.br ^bb288
  ^bb288:  // pred: ^bb287
    %322 = arith.cmpi slt, %231, %c-128_i8 : i8
    cf.cond_br %322, ^bb289, ^bb290
  ^bb289:  // pred: ^bb288
    cf.br ^bb291(%c-128_i8 : i8)
  ^bb290:  // pred: ^bb288
    cf.br ^bb291(%231 : i8)
  ^bb291(%323: i8):  // 2 preds: ^bb289, ^bb290
    cf.br ^bb292
  ^bb292:  // pred: ^bb291
    %324 = arith.cmpi sgt, %231, %c127_i8 : i8
    cf.cond_br %324, ^bb293, ^bb294
  ^bb293:  // pred: ^bb292
    cf.br ^bb295(%c127_i8 : i8)
  ^bb294:  // pred: ^bb292
    cf.br ^bb295(%323 : i8)
  ^bb295(%325: i8):  // 2 preds: ^bb293, ^bb294
    cf.br ^bb296
  ^bb296:  // pred: ^bb295
    %326 = arith.cmpi slt, %245, %c-128_i8 : i8
    cf.cond_br %326, ^bb297, ^bb298
  ^bb297:  // pred: ^bb296
    cf.br ^bb299(%c-128_i8 : i8)
  ^bb298:  // pred: ^bb296
    cf.br ^bb299(%245 : i8)
  ^bb299(%327: i8):  // 2 preds: ^bb297, ^bb298
    cf.br ^bb300
  ^bb300:  // pred: ^bb299
    %328 = arith.cmpi sgt, %245, %c127_i8 : i8
    cf.cond_br %328, ^bb301, ^bb302
  ^bb301:  // pred: ^bb300
    cf.br ^bb303(%c127_i8 : i8)
  ^bb302:  // pred: ^bb300
    cf.br ^bb303(%327 : i8)
  ^bb303(%329: i8):  // 2 preds: ^bb301, ^bb302
    cf.br ^bb304
  ^bb304:  // pred: ^bb303
    %330 = arith.cmpi slt, %259, %c-128_i8 : i8
    cf.cond_br %330, ^bb305, ^bb306
  ^bb305:  // pred: ^bb304
    cf.br ^bb307(%c-128_i8 : i8)
  ^bb306:  // pred: ^bb304
    cf.br ^bb307(%259 : i8)
  ^bb307(%331: i8):  // 2 preds: ^bb305, ^bb306
    cf.br ^bb308
  ^bb308:  // pred: ^bb307
    %332 = arith.cmpi sgt, %259, %c127_i8 : i8
    cf.cond_br %332, ^bb309, ^bb310
  ^bb309:  // pred: ^bb308
    cf.br ^bb311(%c127_i8 : i8)
  ^bb310:  // pred: ^bb308
    cf.br ^bb311(%331 : i8)
  ^bb311(%333: i8):  // 2 preds: ^bb309, ^bb310
    cf.br ^bb312
  ^bb312:  // pred: ^bb311
    %334 = arith.cmpi slt, %273, %c-128_i8 : i8
    cf.cond_br %334, ^bb313, ^bb314
  ^bb313:  // pred: ^bb312
    cf.br ^bb315(%c-128_i8 : i8)
  ^bb314:  // pred: ^bb312
    cf.br ^bb315(%273 : i8)
  ^bb315(%335: i8):  // 2 preds: ^bb313, ^bb314
    cf.br ^bb316
  ^bb316:  // pred: ^bb315
    %336 = arith.cmpi sgt, %273, %c127_i8 : i8
    cf.cond_br %336, ^bb317, ^bb318
  ^bb317:  // pred: ^bb316
    cf.br ^bb319(%c127_i8 : i8)
  ^bb318:  // pred: ^bb316
    cf.br ^bb319(%335 : i8)
  ^bb319(%337: i8):  // 2 preds: ^bb317, ^bb318
    cf.br ^bb320
  ^bb320:  // pred: ^bb319
    %338 = arith.extsi %277 : i8 to i32
    %339 = arith.subi %338, %c-128_i32 : i32
    %340 = arith.muli %339, %c-12_i32 : i32
    %341 = arith.addi %c0_i32, %340 : i32
    %342 = arith.extsi %281 : i8 to i32
    %343 = arith.subi %342, %c-128_i32 : i32
    %344 = arith.muli %343, %c26_i32 : i32
    %345 = arith.addi %341, %344 : i32
    %346 = arith.extsi %285 : i8 to i32
    %347 = arith.subi %346, %c-128_i32 : i32
    %348 = arith.muli %347, %c-19_i32 : i32
    %349 = arith.addi %345, %348 : i32
    %350 = arith.extsi %289 : i8 to i32
    %351 = arith.subi %350, %c-128_i32 : i32
    %352 = arith.muli %351, %c9_i32 : i32
    %353 = arith.addi %349, %352 : i32
    %354 = arith.extsi %293 : i8 to i32
    %355 = arith.subi %354, %c-128_i32 : i32
    %356 = arith.muli %355, %c25_i32 : i32
    %357 = arith.addi %353, %356 : i32
    %358 = arith.extsi %297 : i8 to i32
    %359 = arith.subi %358, %c-128_i32 : i32
    %360 = arith.muli %359, %c33_i32 : i32
    %361 = arith.addi %357, %360 : i32
    %362 = arith.extsi %301 : i8 to i32
    %363 = arith.subi %362, %c-128_i32 : i32
    %364 = arith.muli %363, %c-12_i32 : i32
    %365 = arith.addi %361, %364 : i32
    %366 = arith.extsi %305 : i8 to i32
    %367 = arith.subi %366, %c-128_i32 : i32
    %368 = arith.muli %367, %c36_i32 : i32
    %369 = arith.addi %365, %368 : i32
    %370 = arith.extsi %309 : i8 to i32
    %371 = arith.subi %370, %c-128_i32 : i32
    %372 = arith.muli %371, %c-32_i32 : i32
    %373 = arith.addi %369, %372 : i32
    %374 = arith.extsi %313 : i8 to i32
    %375 = arith.subi %374, %c-128_i32 : i32
    %376 = arith.muli %375, %c33_i32 : i32
    %377 = arith.addi %373, %376 : i32
    %378 = arith.extsi %317 : i8 to i32
    %379 = arith.subi %378, %c-128_i32 : i32
    %380 = arith.muli %379, %c-17_i32 : i32
    %381 = arith.addi %377, %380 : i32
    %382 = arith.extsi %321 : i8 to i32
    %383 = arith.subi %382, %c-128_i32 : i32
    %384 = arith.muli %383, %c-68_i32 : i32
    %385 = arith.addi %381, %384 : i32
    %386 = arith.extsi %325 : i8 to i32
    %387 = arith.subi %386, %c-128_i32 : i32
    %388 = arith.muli %387, %c-9_i32 : i32
    %389 = arith.addi %385, %388 : i32
    %390 = arith.extsi %329 : i8 to i32
    %391 = arith.subi %390, %c-128_i32 : i32
    %392 = arith.muli %391, %c-11_i32 : i32
    %393 = arith.addi %389, %392 : i32
    %394 = arith.extsi %333 : i8 to i32
    %395 = arith.subi %394, %c-128_i32 : i32
    %396 = arith.muli %395, %c-6_i32 : i32
    %397 = arith.addi %393, %396 : i32
    %398 = arith.extsi %337 : i8 to i32
    %399 = arith.subi %398, %c-128_i32 : i32
    %400 = arith.muli %399, %c25_i32 : i32
    %401 = arith.addi %397, %400 : i32
    %402 = arith.muli %339, %c3_i32 : i32
    %403 = arith.addi %c0_i32, %402 : i32
    %404 = arith.muli %343, %c-36_i32 : i32
    %405 = arith.addi %403, %404 : i32
    %406 = arith.muli %347, %c-46_i32 : i32
    %407 = arith.addi %405, %406 : i32
    %408 = arith.muli %351, %c2_i32 : i32
    %409 = arith.addi %407, %408 : i32
    %410 = arith.muli %355, %c6_i32 : i32
    %411 = arith.addi %409, %410 : i32
    %412 = arith.muli %359, %c-7_i32 : i32
    %413 = arith.addi %411, %412 : i32
    %414 = arith.addi %413, %364 : i32
    %415 = arith.muli %367, %c2_i32 : i32
    %416 = arith.addi %414, %415 : i32
    %417 = arith.muli %371, %c-1_i32 : i32
    %418 = arith.addi %416, %417 : i32
    %419 = arith.muli %375, %c-6_i32 : i32
    %420 = arith.addi %418, %419 : i32
    %421 = arith.addi %420, %380 : i32
    %422 = arith.muli %383, %c-15_i32 : i32
    %423 = arith.addi %421, %422 : i32
    %424 = arith.muli %387, %c-17_i32 : i32
    %425 = arith.addi %423, %424 : i32
    %426 = arith.muli %391, %c-45_i32 : i32
    %427 = arith.addi %425, %426 : i32
    %428 = arith.muli %395, %c39_i32 : i32
    %429 = arith.addi %427, %428 : i32
    %430 = arith.muli %399, %c-31_i32 : i32
    %431 = arith.addi %429, %430 : i32
    %432 = arith.muli %339, %c-5_i32 : i32
    %433 = arith.addi %c0_i32, %432 : i32
    %434 = arith.muli %343, %c39_i32 : i32
    %435 = arith.addi %433, %434 : i32
    %436 = arith.muli %347, %c-35_i32 : i32
    %437 = arith.addi %435, %436 : i32
    %438 = arith.muli %351, %c-21_i32 : i32
    %439 = arith.addi %437, %438 : i32
    %440 = arith.muli %355, %c-37_i32 : i32
    %441 = arith.addi %439, %440 : i32
    %442 = arith.muli %359, %c-28_i32 : i32
    %443 = arith.addi %441, %442 : i32
    %444 = arith.muli %363, %c5_i32 : i32
    %445 = arith.addi %443, %444 : i32
    %446 = arith.muli %367, %c26_i32 : i32
    %447 = arith.addi %445, %446 : i32
    %448 = arith.muli %371, %c23_i32 : i32
    %449 = arith.addi %447, %448 : i32
    %450 = arith.muli %375, %c-4_i32 : i32
    %451 = arith.addi %449, %450 : i32
    %452 = arith.muli %379, %c36_i32 : i32
    %453 = arith.addi %451, %452 : i32
    %454 = arith.muli %383, %c18_i32 : i32
    %455 = arith.addi %453, %454 : i32
    %456 = arith.muli %387, %c21_i32 : i32
    %457 = arith.addi %455, %456 : i32
    %458 = arith.muli %391, %c-17_i32 : i32
    %459 = arith.addi %457, %458 : i32
    %460 = arith.muli %395, %c30_i32 : i32
    %461 = arith.addi %459, %460 : i32
    %462 = arith.muli %399, %c-28_i32 : i32
    %463 = arith.addi %461, %462 : i32
    %464 = arith.muli %339, %c16_i32 : i32
    %465 = arith.addi %c0_i32, %464 : i32
    %466 = arith.muli %343, %c-2_i32 : i32
    %467 = arith.addi %465, %466 : i32
    %468 = arith.muli %347, %c20_i32 : i32
    %469 = arith.addi %467, %468 : i32
    %470 = arith.muli %351, %c-38_i32 : i32
    %471 = arith.addi %469, %470 : i32
    %472 = arith.muli %355, %c28_i32 : i32
    %473 = arith.addi %471, %472 : i32
    %474 = arith.muli %359, %c-8_i32 : i32
    %475 = arith.addi %473, %474 : i32
    %476 = arith.muli %363, %c-13_i32 : i32
    %477 = arith.addi %475, %476 : i32
    %478 = arith.muli %367, %c-15_i32 : i32
    %479 = arith.addi %477, %478 : i32
    %480 = arith.muli %371, %c-17_i32 : i32
    %481 = arith.addi %479, %480 : i32
    %482 = arith.muli %375, %c-30_i32 : i32
    %483 = arith.addi %481, %482 : i32
    %484 = arith.muli %379, %c-13_i32 : i32
    %485 = arith.addi %483, %484 : i32
    %486 = arith.muli %383, %c9_i32 : i32
    %487 = arith.addi %485, %486 : i32
    %488 = arith.muli %387, %c-29_i32 : i32
    %489 = arith.addi %487, %488 : i32
    %490 = arith.muli %391, %c-23_i32 : i32
    %491 = arith.addi %489, %490 : i32
    %492 = arith.muli %395, %c-19_i32 : i32
    %493 = arith.addi %491, %492 : i32
    %494 = arith.muli %399, %c-29_i32 : i32
    %495 = arith.addi %493, %494 : i32
    %496 = arith.muli %339, %c-28_i32 : i32
    %497 = arith.addi %c0_i32, %496 : i32
    %498 = arith.muli %343, %c21_i32 : i32
    %499 = arith.addi %497, %498 : i32
    %500 = arith.muli %347, %c7_i32 : i32
    %501 = arith.addi %499, %500 : i32
    %502 = arith.muli %351, %c11_i32 : i32
    %503 = arith.addi %501, %502 : i32
    %504 = arith.muli %355, %c4_i32 : i32
    %505 = arith.addi %503, %504 : i32
    %506 = arith.muli %359, %c27_i32 : i32
    %507 = arith.addi %505, %506 : i32
    %508 = arith.muli %363, %c26_i32 : i32
    %509 = arith.addi %507, %508 : i32
    %510 = arith.muli %367, %c-2_i32 : i32
    %511 = arith.addi %509, %510 : i32
    %512 = arith.muli %371, %c-21_i32 : i32
    %513 = arith.addi %511, %512 : i32
    %514 = arith.muli %375, %c1_i32 : i32
    %515 = arith.addi %513, %514 : i32
    %516 = arith.muli %379, %c-34_i32 : i32
    %517 = arith.addi %515, %516 : i32
    %518 = arith.muli %383, %c33_i32 : i32
    %519 = arith.addi %517, %518 : i32
    %520 = arith.muli %387, %c-26_i32 : i32
    %521 = arith.addi %519, %520 : i32
    %522 = arith.muli %391, %c11_i32 : i32
    %523 = arith.addi %521, %522 : i32
    %524 = arith.muli %395, %c-20_i32 : i32
    %525 = arith.addi %523, %524 : i32
    %526 = arith.muli %399, %c3_i32 : i32
    %527 = arith.addi %525, %526 : i32
    %528 = arith.muli %339, %c35_i32 : i32
    %529 = arith.addi %c0_i32, %528 : i32
    %530 = arith.muli %343, %c10_i32 : i32
    %531 = arith.addi %529, %530 : i32
    %532 = arith.muli %347, %c34_i32 : i32
    %533 = arith.addi %531, %532 : i32
    %534 = arith.muli %351, %c36_i32 : i32
    %535 = arith.addi %533, %534 : i32
    %536 = arith.muli %355, %c30_i32 : i32
    %537 = arith.addi %535, %536 : i32
    %538 = arith.muli %359, %c39_i32 : i32
    %539 = arith.addi %537, %538 : i32
    %540 = arith.muli %363, %c3_i32 : i32
    %541 = arith.addi %539, %540 : i32
    %542 = arith.muli %367, %c-26_i32 : i32
    %543 = arith.addi %541, %542 : i32
    %544 = arith.muli %371, %c3_i32 : i32
    %545 = arith.addi %543, %544 : i32
    %546 = arith.muli %375, %c36_i32 : i32
    %547 = arith.addi %545, %546 : i32
    %548 = arith.muli %379, %c-1_i32 : i32
    %549 = arith.addi %547, %548 : i32
    %550 = arith.muli %383, %c-64_i32 : i32
    %551 = arith.addi %549, %550 : i32
    %552 = arith.muli %387, %c17_i32 : i32
    %553 = arith.addi %551, %552 : i32
    %554 = arith.muli %391, %c-8_i32 : i32
    %555 = arith.addi %553, %554 : i32
    %556 = arith.muli %395, %c-4_i32 : i32
    %557 = arith.addi %555, %556 : i32
    %558 = arith.muli %399, %c-15_i32 : i32
    %559 = arith.addi %557, %558 : i32
    %560 = arith.muli %339, %c17_i32 : i32
    %561 = arith.addi %c0_i32, %560 : i32
    %562 = arith.muli %343, %c12_i32 : i32
    %563 = arith.addi %561, %562 : i32
    %564 = arith.muli %347, %c-11_i32 : i32
    %565 = arith.addi %563, %564 : i32
    %566 = arith.muli %351, %c-32_i32 : i32
    %567 = arith.addi %565, %566 : i32
    %568 = arith.muli %355, %c-13_i32 : i32
    %569 = arith.addi %567, %568 : i32
    %570 = arith.muli %359, %c7_i32 : i32
    %571 = arith.addi %569, %570 : i32
    %572 = arith.muli %363, %c23_i32 : i32
    %573 = arith.addi %571, %572 : i32
    %574 = arith.muli %367, %c-27_i32 : i32
    %575 = arith.addi %573, %574 : i32
    %576 = arith.muli %371, %c-24_i32 : i32
    %577 = arith.addi %575, %576 : i32
    %578 = arith.muli %375, %c-19_i32 : i32
    %579 = arith.addi %577, %578 : i32
    %580 = arith.muli %379, %c-6_i32 : i32
    %581 = arith.addi %579, %580 : i32
    %582 = arith.muli %383, %c-36_i32 : i32
    %583 = arith.addi %581, %582 : i32
    %584 = arith.muli %387, %c-24_i32 : i32
    %585 = arith.addi %583, %584 : i32
    %586 = arith.muli %391, %c35_i32 : i32
    %587 = arith.addi %585, %586 : i32
    %588 = arith.muli %395, %c-5_i32 : i32
    %589 = arith.addi %587, %588 : i32
    %590 = arith.muli %399, %c7_i32 : i32
    %591 = arith.addi %589, %590 : i32
    %592 = arith.muli %339, %c-35_i32 : i32
    %593 = arith.addi %c0_i32, %592 : i32
    %594 = arith.muli %343, %c-5_i32 : i32
    %595 = arith.addi %593, %594 : i32
    %596 = arith.muli %347, %c-3_i32 : i32
    %597 = arith.addi %595, %596 : i32
    %598 = arith.addi %597, %c0_i32 : i32
    %599 = arith.muli %355, %c20_i32 : i32
    %600 = arith.addi %598, %599 : i32
    %601 = arith.muli %359, %c38_i32 : i32
    %602 = arith.addi %600, %601 : i32
    %603 = arith.muli %363, %c17_i32 : i32
    %604 = arith.addi %602, %603 : i32
    %605 = arith.muli %367, %c23_i32 : i32
    %606 = arith.addi %604, %605 : i32
    %607 = arith.muli %371, %c-25_i32 : i32
    %608 = arith.addi %606, %607 : i32
    %609 = arith.muli %375, %c-15_i32 : i32
    %610 = arith.addi %608, %609 : i32
    %611 = arith.muli %379, %c17_i32 : i32
    %612 = arith.addi %610, %611 : i32
    %613 = arith.muli %383, %c-22_i32 : i32
    %614 = arith.addi %612, %613 : i32
    %615 = arith.muli %387, %c2_i32 : i32
    %616 = arith.addi %614, %615 : i32
    %617 = arith.muli %391, %c38_i32 : i32
    %618 = arith.addi %616, %617 : i32
    %619 = arith.muli %395, %c4_i32 : i32
    %620 = arith.addi %618, %619 : i32
    %621 = arith.muli %399, %c4_i32 : i32
    %622 = arith.addi %620, %621 : i32
    %623 = arith.muli %339, %c37_i32 : i32
    %624 = arith.addi %c0_i32, %623 : i32
    %625 = arith.muli %343, %c33_i32 : i32
    %626 = arith.addi %624, %625 : i32
    %627 = arith.muli %347, %c29_i32 : i32
    %628 = arith.addi %626, %627 : i32
    %629 = arith.muli %351, %c10_i32 : i32
    %630 = arith.addi %628, %629 : i32
    %631 = arith.addi %630, %440 : i32
    %632 = arith.muli %359, %c29_i32 : i32
    %633 = arith.addi %631, %632 : i32
    %634 = arith.muli %363, %c-36_i32 : i32
    %635 = arith.addi %633, %634 : i32
    %636 = arith.muli %367, %c32_i32 : i32
    %637 = arith.addi %635, %636 : i32
    %638 = arith.muli %371, %c1_i32 : i32
    %639 = arith.addi %637, %638 : i32
    %640 = arith.addi %639, %419 : i32
    %641 = arith.muli %379, %c-29_i32 : i32
    %642 = arith.addi %640, %641 : i32
    %643 = arith.muli %383, %c55_i32 : i32
    %644 = arith.addi %642, %643 : i32
    %645 = arith.muli %387, %c11_i32 : i32
    %646 = arith.addi %644, %645 : i32
    %647 = arith.muli %391, %c-15_i32 : i32
    %648 = arith.addi %646, %647 : i32
    %649 = arith.muli %395, %c26_i32 : i32
    %650 = arith.addi %648, %649 : i32
    %651 = arith.muli %399, %c22_i32 : i32
    %652 = arith.addi %650, %651 : i32
    %653 = arith.muli %339, %c-17_i32 : i32
    %654 = arith.addi %c0_i32, %653 : i32
    %655 = arith.muli %343, %c28_i32 : i32
    %656 = arith.addi %654, %655 : i32
    %657 = arith.muli %347, %c-25_i32 : i32
    %658 = arith.addi %656, %657 : i32
    %659 = arith.muli %351, %c3_i32 : i32
    %660 = arith.addi %658, %659 : i32
    %661 = arith.muli %355, %c-32_i32 : i32
    %662 = arith.addi %660, %661 : i32
    %663 = arith.muli %359, %c22_i32 : i32
    %664 = arith.addi %662, %663 : i32
    %665 = arith.muli %363, %c2_i32 : i32
    %666 = arith.addi %664, %665 : i32
    %667 = arith.muli %367, %c3_i32 : i32
    %668 = arith.addi %666, %667 : i32
    %669 = arith.muli %371, %c33_i32 : i32
    %670 = arith.addi %668, %669 : i32
    %671 = arith.muli %375, %c24_i32 : i32
    %672 = arith.addi %670, %671 : i32
    %673 = arith.muli %379, %c9_i32 : i32
    %674 = arith.addi %672, %673 : i32
    %675 = arith.muli %383, %c46_i32 : i32
    %676 = arith.addi %674, %675 : i32
    %677 = arith.muli %387, %c-39_i32 : i32
    %678 = arith.addi %676, %677 : i32
    %679 = arith.muli %391, %c-27_i32 : i32
    %680 = arith.addi %678, %679 : i32
    %681 = arith.muli %395, %c20_i32 : i32
    %682 = arith.addi %680, %681 : i32
    %683 = arith.muli %399, %c11_i32 : i32
    %684 = arith.addi %682, %683 : i32
    %685 = arith.muli %339, %c-22_i32 : i32
    %686 = arith.addi %c0_i32, %685 : i32
    %687 = arith.addi %686, %344 : i32
    %688 = arith.muli %347, %c-4_i32 : i32
    %689 = arith.addi %687, %688 : i32
    %690 = arith.muli %351, %c-40_i32 : i32
    %691 = arith.addi %689, %690 : i32
    %692 = arith.muli %355, %c19_i32 : i32
    %693 = arith.addi %691, %692 : i32
    %694 = arith.addi %693, %c0_i32 : i32
    %695 = arith.muli %363, %c-60_i32 : i32
    %696 = arith.addi %694, %695 : i32
    %697 = arith.muli %367, %c-40_i32 : i32
    %698 = arith.addi %696, %697 : i32
    %699 = arith.muli %371, %c-20_i32 : i32
    %700 = arith.addi %698, %699 : i32
    %701 = arith.muli %375, %c-39_i32 : i32
    %702 = arith.addi %700, %701 : i32
    %703 = arith.muli %379, %c-2_i32 : i32
    %704 = arith.addi %702, %703 : i32
    %705 = arith.muli %383, %c13_i32 : i32
    %706 = arith.addi %704, %705 : i32
    %707 = arith.muli %387, %c25_i32 : i32
    %708 = arith.addi %706, %707 : i32
    %709 = arith.muli %391, %c32_i32 : i32
    %710 = arith.addi %708, %709 : i32
    %711 = arith.muli %395, %c-40_i32 : i32
    %712 = arith.addi %710, %711 : i32
    %713 = arith.muli %399, %c-42_i32 : i32
    %714 = arith.addi %712, %713 : i32
    %715 = arith.muli %339, %c-30_i32 : i32
    %716 = arith.addi %c0_i32, %715 : i32
    %717 = arith.muli %343, %c31_i32 : i32
    %718 = arith.addi %716, %717 : i32
    %719 = arith.muli %347, %c-23_i32 : i32
    %720 = arith.addi %718, %719 : i32
    %721 = arith.muli %351, %c-41_i32 : i32
    %722 = arith.addi %720, %721 : i32
    %723 = arith.muli %355, %c-54_i32 : i32
    %724 = arith.addi %722, %723 : i32
    %725 = arith.muli %359, %c-30_i32 : i32
    %726 = arith.addi %724, %725 : i32
    %727 = arith.muli %363, %c-35_i32 : i32
    %728 = arith.addi %726, %727 : i32
    %729 = arith.muli %367, %c-58_i32 : i32
    %730 = arith.addi %728, %729 : i32
    %731 = arith.muli %371, %c19_i32 : i32
    %732 = arith.addi %730, %731 : i32
    %733 = arith.muli %375, %c-25_i32 : i32
    %734 = arith.addi %732, %733 : i32
    %735 = arith.muli %379, %c4_i32 : i32
    %736 = arith.addi %734, %735 : i32
    %737 = arith.muli %383, %c62_i32 : i32
    %738 = arith.addi %736, %737 : i32
    %739 = arith.addi %738, %c0_i32 : i32
    %740 = arith.muli %391, %c1_i32 : i32
    %741 = arith.addi %739, %740 : i32
    %742 = arith.addi %741, %681 : i32
    %743 = arith.muli %399, %c-57_i32 : i32
    %744 = arith.addi %742, %743 : i32
    %745 = arith.muli %339, %c-37_i32 : i32
    %746 = arith.addi %c0_i32, %745 : i32
    %747 = arith.muli %343, %c-25_i32 : i32
    %748 = arith.addi %746, %747 : i32
    %749 = arith.muli %347, %c21_i32 : i32
    %750 = arith.addi %748, %749 : i32
    %751 = arith.muli %351, %c21_i32 : i32
    %752 = arith.addi %750, %751 : i32
    %753 = arith.muli %355, %c-11_i32 : i32
    %754 = arith.addi %752, %753 : i32
    %755 = arith.muli %359, %c6_i32 : i32
    %756 = arith.addi %754, %755 : i32
    %757 = arith.muli %363, %c-42_i32 : i32
    %758 = arith.addi %756, %757 : i32
    %759 = arith.addi %758, %446 : i32
    %760 = arith.muli %371, %c-36_i32 : i32
    %761 = arith.addi %759, %760 : i32
    %762 = arith.muli %375, %c9_i32 : i32
    %763 = arith.addi %761, %762 : i32
    %764 = arith.muli %379, %c34_i32 : i32
    %765 = arith.addi %763, %764 : i32
    %766 = arith.muli %383, %c-2_i32 : i32
    %767 = arith.addi %765, %766 : i32
    %768 = arith.muli %387, %c8_i32 : i32
    %769 = arith.addi %767, %768 : i32
    %770 = arith.muli %391, %c2_i32 : i32
    %771 = arith.addi %769, %770 : i32
    %772 = arith.muli %395, %c19_i32 : i32
    %773 = arith.addi %771, %772 : i32
    %774 = arith.muli %399, %c-17_i32 : i32
    %775 = arith.addi %773, %774 : i32
    %776 = arith.muli %339, %c25_i32 : i32
    %777 = arith.addi %c0_i32, %776 : i32
    %778 = arith.muli %343, %c30_i32 : i32
    %779 = arith.addi %777, %778 : i32
    %780 = arith.muli %347, %c-30_i32 : i32
    %781 = arith.addi %779, %780 : i32
    %782 = arith.addi %781, %352 : i32
    %783 = arith.muli %355, %c-3_i32 : i32
    %784 = arith.addi %782, %783 : i32
    %785 = arith.muli %359, %c-13_i32 : i32
    %786 = arith.addi %784, %785 : i32
    %787 = arith.muli %363, %c20_i32 : i32
    %788 = arith.addi %786, %787 : i32
    %789 = arith.muli %367, %c-35_i32 : i32
    %790 = arith.addi %788, %789 : i32
    %791 = arith.muli %371, %c-38_i32 : i32
    %792 = arith.addi %790, %791 : i32
    %793 = arith.muli %375, %c32_i32 : i32
    %794 = arith.addi %792, %793 : i32
    %795 = arith.muli %379, %c-39_i32 : i32
    %796 = arith.addi %794, %795 : i32
    %797 = arith.muli %383, %c15_i32 : i32
    %798 = arith.addi %796, %797 : i32
    %799 = arith.addi %798, %488 : i32
    %800 = arith.muli %391, %c-7_i32 : i32
    %801 = arith.addi %799, %800 : i32
    %802 = arith.muli %395, %c-9_i32 : i32
    %803 = arith.addi %801, %802 : i32
    %804 = arith.muli %399, %c-18_i32 : i32
    %805 = arith.addi %803, %804 : i32
    %806 = arith.muli %339, %c-23_i32 : i32
    %807 = arith.addi %c0_i32, %806 : i32
    %808 = arith.muli %343, %c36_i32 : i32
    %809 = arith.addi %807, %808 : i32
    %810 = arith.muli %347, %c-26_i32 : i32
    %811 = arith.addi %809, %810 : i32
    %812 = arith.muli %351, %c41_i32 : i32
    %813 = arith.addi %811, %812 : i32
    %814 = arith.addi %813, %c0_i32 : i32
    %815 = arith.addi %814, %570 : i32
    %816 = arith.muli %363, %c22_i32 : i32
    %817 = arith.addi %815, %816 : i32
    %818 = arith.muli %367, %c-30_i32 : i32
    %819 = arith.addi %817, %818 : i32
    %820 = arith.muli %371, %c30_i32 : i32
    %821 = arith.addi %819, %820 : i32
    %822 = arith.muli %375, %c13_i32 : i32
    %823 = arith.addi %821, %822 : i32
    %824 = arith.muli %379, %c35_i32 : i32
    %825 = arith.addi %823, %824 : i32
    %826 = arith.muli %383, %c-45_i32 : i32
    %827 = arith.addi %825, %826 : i32
    %828 = arith.muli %387, %c-35_i32 : i32
    %829 = arith.addi %827, %828 : i32
    %830 = arith.muli %391, %c-9_i32 : i32
    %831 = arith.addi %829, %830 : i32
    %832 = arith.addi %831, %681 : i32
    %833 = arith.muli %399, %c-6_i32 : i32
    %834 = arith.addi %832, %833 : i32
    %835 = arith.muli %339, %c8_i32 : i32
    %836 = arith.addi %c0_i32, %835 : i32
    %837 = arith.muli %343, %c34_i32 : i32
    %838 = arith.addi %836, %837 : i32
    %839 = arith.muli %347, %c38_i32 : i32
    %840 = arith.addi %838, %839 : i32
    %841 = arith.muli %351, %c33_i32 : i32
    %842 = arith.addi %840, %841 : i32
    %843 = arith.muli %355, %c9_i32 : i32
    %844 = arith.addi %842, %843 : i32
    %845 = arith.muli %359, %c8_i32 : i32
    %846 = arith.addi %844, %845 : i32
    %847 = arith.muli %363, %c15_i32 : i32
    %848 = arith.addi %846, %847 : i32
    %849 = arith.muli %367, %c11_i32 : i32
    %850 = arith.addi %848, %849 : i32
    %851 = arith.addi %850, %372 : i32
    %852 = arith.muli %375, %c18_i32 : i32
    %853 = arith.addi %851, %852 : i32
    %854 = arith.muli %379, %c-12_i32 : i32
    %855 = arith.addi %853, %854 : i32
    %856 = arith.muli %383, %c127_i32 : i32
    %857 = arith.addi %855, %856 : i32
    %858 = arith.muli %387, %c-36_i32 : i32
    %859 = arith.addi %857, %858 : i32
    %860 = arith.muli %391, %c88_i32 : i32
    %861 = arith.addi %859, %860 : i32
    %862 = arith.muli %395, %c-27_i32 : i32
    %863 = arith.addi %861, %862 : i32
    %864 = arith.muli %399, %c38_i32 : i32
    %865 = arith.addi %863, %864 : i32
    %866 = arith.addi %c-729_i32, %401 : i32
    %867 = arith.addi %c1954_i32, %431 : i32
    %868 = arith.addi %c610_i32, %463 : i32
    %869 = arith.addi %c0_i32, %495 : i32
    %870 = arith.addi %c241_i32, %527 : i32
    %871 = arith.addi %c-471_i32, %559 : i32
    %872 = arith.addi %c-35_i32, %591 : i32
    %873 = arith.addi %c-867_i32, %622 : i32
    %874 = arith.addi %c571_i32, %652 : i32
    %875 = arith.addi %c581_i32, %684 : i32
    %876 = arith.addi %c4260_i32, %714 : i32
    %877 = arith.addi %c3943_i32, %744 : i32
    %878 = arith.addi %c591_i32, %775 : i32
    %879 = arith.addi %c0_i32, %805 : i32
    %880 = arith.addi %c-889_i32, %834 : i32
    %881 = arith.addi %c-5103_i32, %865 : i32
    %882 = arith.extsi %866 : i32 to i64
    %883 = arith.muli %882, %c1561796795_i64 : i64
    %884 = arith.addi %883, %c68719476736_i64 : i64
    %885 = arith.cmpi sge, %866, %c0_i32 : i32
    cf.cond_br %885, ^bb321, ^bb322
  ^bb321:  // pred: ^bb320
    cf.br ^bb323(%c1073741824_i64 : i64)
  ^bb322:  // pred: ^bb320
    cf.br ^bb323(%c-1073741824_i64 : i64)
  ^bb323(%886: i64):  // 2 preds: ^bb321, ^bb322
    cf.br ^bb324
  ^bb324:  // pred: ^bb323
    %887 = arith.addi %886, %884 : i64
    %888 = arith.shrsi %887, %c37_i64 : i64
    %889 = arith.trunci %888 : i64 to i32
    %890 = arith.addi %889, %c-128_i32 : i32
    %891 = arith.cmpi slt, %890, %c-128_i32 : i32
    cf.cond_br %891, ^bb325, ^bb326
  ^bb325:  // pred: ^bb324
    cf.br ^bb327(%c-128_i32 : i32)
  ^bb326:  // pred: ^bb324
    cf.br ^bb327(%890 : i32)
  ^bb327(%892: i32):  // 2 preds: ^bb325, ^bb326
    cf.br ^bb328
  ^bb328:  // pred: ^bb327
    %893 = arith.cmpi sgt, %890, %c127_i32 : i32
    cf.cond_br %893, ^bb329, ^bb330
  ^bb329:  // pred: ^bb328
    cf.br ^bb331(%c127_i32 : i32)
  ^bb330:  // pred: ^bb328
    cf.br ^bb331(%892 : i32)
  ^bb331(%894: i32):  // 2 preds: ^bb329, ^bb330
    cf.br ^bb332
  ^bb332:  // pred: ^bb331
    %895 = arith.trunci %894 : i32 to i8
    %896 = arith.extsi %867 : i32 to i64
    %897 = arith.muli %896, %c1561796795_i64 : i64
    %898 = arith.addi %897, %c68719476736_i64 : i64
    %899 = arith.cmpi sge, %867, %c0_i32 : i32
    cf.cond_br %899, ^bb333, ^bb334
  ^bb333:  // pred: ^bb332
    cf.br ^bb335(%c1073741824_i64 : i64)
  ^bb334:  // pred: ^bb332
    cf.br ^bb335(%c-1073741824_i64 : i64)
  ^bb335(%900: i64):  // 2 preds: ^bb333, ^bb334
    cf.br ^bb336
  ^bb336:  // pred: ^bb335
    %901 = arith.addi %900, %898 : i64
    %902 = arith.shrsi %901, %c37_i64 : i64
    %903 = arith.trunci %902 : i64 to i32
    %904 = arith.addi %903, %c-128_i32 : i32
    %905 = arith.cmpi slt, %904, %c-128_i32 : i32
    cf.cond_br %905, ^bb337, ^bb338
  ^bb337:  // pred: ^bb336
    cf.br ^bb339(%c-128_i32 : i32)
  ^bb338:  // pred: ^bb336
    cf.br ^bb339(%904 : i32)
  ^bb339(%906: i32):  // 2 preds: ^bb337, ^bb338
    cf.br ^bb340
  ^bb340:  // pred: ^bb339
    %907 = arith.cmpi sgt, %904, %c127_i32 : i32
    cf.cond_br %907, ^bb341, ^bb342
  ^bb341:  // pred: ^bb340
    cf.br ^bb343(%c127_i32 : i32)
  ^bb342:  // pred: ^bb340
    cf.br ^bb343(%906 : i32)
  ^bb343(%908: i32):  // 2 preds: ^bb341, ^bb342
    cf.br ^bb344
  ^bb344:  // pred: ^bb343
    %909 = arith.trunci %908 : i32 to i8
    %910 = arith.extsi %868 : i32 to i64
    %911 = arith.muli %910, %c1561796795_i64 : i64
    %912 = arith.addi %911, %c68719476736_i64 : i64
    %913 = arith.cmpi sge, %868, %c0_i32 : i32
    cf.cond_br %913, ^bb345, ^bb346
  ^bb345:  // pred: ^bb344
    cf.br ^bb347(%c1073741824_i64 : i64)
  ^bb346:  // pred: ^bb344
    cf.br ^bb347(%c-1073741824_i64 : i64)
  ^bb347(%914: i64):  // 2 preds: ^bb345, ^bb346
    cf.br ^bb348
  ^bb348:  // pred: ^bb347
    %915 = arith.addi %914, %912 : i64
    %916 = arith.shrsi %915, %c37_i64 : i64
    %917 = arith.trunci %916 : i64 to i32
    %918 = arith.addi %917, %c-128_i32 : i32
    %919 = arith.cmpi slt, %918, %c-128_i32 : i32
    cf.cond_br %919, ^bb349, ^bb350
  ^bb349:  // pred: ^bb348
    cf.br ^bb351(%c-128_i32 : i32)
  ^bb350:  // pred: ^bb348
    cf.br ^bb351(%918 : i32)
  ^bb351(%920: i32):  // 2 preds: ^bb349, ^bb350
    cf.br ^bb352
  ^bb352:  // pred: ^bb351
    %921 = arith.cmpi sgt, %918, %c127_i32 : i32
    cf.cond_br %921, ^bb353, ^bb354
  ^bb353:  // pred: ^bb352
    cf.br ^bb355(%c127_i32 : i32)
  ^bb354:  // pred: ^bb352
    cf.br ^bb355(%920 : i32)
  ^bb355(%922: i32):  // 2 preds: ^bb353, ^bb354
    cf.br ^bb356
  ^bb356:  // pred: ^bb355
    %923 = arith.trunci %922 : i32 to i8
    %924 = arith.extsi %869 : i32 to i64
    %925 = arith.muli %924, %c1561796795_i64 : i64
    %926 = arith.addi %925, %c68719476736_i64 : i64
    %927 = arith.cmpi sge, %869, %c0_i32 : i32
    cf.cond_br %927, ^bb357, ^bb358
  ^bb357:  // pred: ^bb356
    cf.br ^bb359(%c1073741824_i64 : i64)
  ^bb358:  // pred: ^bb356
    cf.br ^bb359(%c-1073741824_i64 : i64)
  ^bb359(%928: i64):  // 2 preds: ^bb357, ^bb358
    cf.br ^bb360
  ^bb360:  // pred: ^bb359
    %929 = arith.addi %928, %926 : i64
    %930 = arith.shrsi %929, %c37_i64 : i64
    %931 = arith.trunci %930 : i64 to i32
    %932 = arith.addi %931, %c-128_i32 : i32
    %933 = arith.cmpi slt, %932, %c-128_i32 : i32
    cf.cond_br %933, ^bb361, ^bb362
  ^bb361:  // pred: ^bb360
    cf.br ^bb363(%c-128_i32 : i32)
  ^bb362:  // pred: ^bb360
    cf.br ^bb363(%932 : i32)
  ^bb363(%934: i32):  // 2 preds: ^bb361, ^bb362
    cf.br ^bb364
  ^bb364:  // pred: ^bb363
    %935 = arith.cmpi sgt, %932, %c127_i32 : i32
    cf.cond_br %935, ^bb365, ^bb366
  ^bb365:  // pred: ^bb364
    cf.br ^bb367(%c127_i32 : i32)
  ^bb366:  // pred: ^bb364
    cf.br ^bb367(%934 : i32)
  ^bb367(%936: i32):  // 2 preds: ^bb365, ^bb366
    cf.br ^bb368
  ^bb368:  // pred: ^bb367
    %937 = arith.trunci %936 : i32 to i8
    %938 = arith.extsi %870 : i32 to i64
    %939 = arith.muli %938, %c1561796795_i64 : i64
    %940 = arith.addi %939, %c68719476736_i64 : i64
    %941 = arith.cmpi sge, %870, %c0_i32 : i32
    cf.cond_br %941, ^bb369, ^bb370
  ^bb369:  // pred: ^bb368
    cf.br ^bb371(%c1073741824_i64 : i64)
  ^bb370:  // pred: ^bb368
    cf.br ^bb371(%c-1073741824_i64 : i64)
  ^bb371(%942: i64):  // 2 preds: ^bb369, ^bb370
    cf.br ^bb372
  ^bb372:  // pred: ^bb371
    %943 = arith.addi %942, %940 : i64
    %944 = arith.shrsi %943, %c37_i64 : i64
    %945 = arith.trunci %944 : i64 to i32
    %946 = arith.addi %945, %c-128_i32 : i32
    %947 = arith.cmpi slt, %946, %c-128_i32 : i32
    cf.cond_br %947, ^bb373, ^bb374
  ^bb373:  // pred: ^bb372
    cf.br ^bb375(%c-128_i32 : i32)
  ^bb374:  // pred: ^bb372
    cf.br ^bb375(%946 : i32)
  ^bb375(%948: i32):  // 2 preds: ^bb373, ^bb374
    cf.br ^bb376
  ^bb376:  // pred: ^bb375
    %949 = arith.cmpi sgt, %946, %c127_i32 : i32
    cf.cond_br %949, ^bb377, ^bb378
  ^bb377:  // pred: ^bb376
    cf.br ^bb379(%c127_i32 : i32)
  ^bb378:  // pred: ^bb376
    cf.br ^bb379(%948 : i32)
  ^bb379(%950: i32):  // 2 preds: ^bb377, ^bb378
    cf.br ^bb380
  ^bb380:  // pred: ^bb379
    %951 = arith.trunci %950 : i32 to i8
    %952 = arith.extsi %871 : i32 to i64
    %953 = arith.muli %952, %c1561796795_i64 : i64
    %954 = arith.addi %953, %c68719476736_i64 : i64
    %955 = arith.cmpi sge, %871, %c0_i32 : i32
    cf.cond_br %955, ^bb381, ^bb382
  ^bb381:  // pred: ^bb380
    cf.br ^bb383(%c1073741824_i64 : i64)
  ^bb382:  // pred: ^bb380
    cf.br ^bb383(%c-1073741824_i64 : i64)
  ^bb383(%956: i64):  // 2 preds: ^bb381, ^bb382
    cf.br ^bb384
  ^bb384:  // pred: ^bb383
    %957 = arith.addi %956, %954 : i64
    %958 = arith.shrsi %957, %c37_i64 : i64
    %959 = arith.trunci %958 : i64 to i32
    %960 = arith.addi %959, %c-128_i32 : i32
    %961 = arith.cmpi slt, %960, %c-128_i32 : i32
    cf.cond_br %961, ^bb385, ^bb386
  ^bb385:  // pred: ^bb384
    cf.br ^bb387(%c-128_i32 : i32)
  ^bb386:  // pred: ^bb384
    cf.br ^bb387(%960 : i32)
  ^bb387(%962: i32):  // 2 preds: ^bb385, ^bb386
    cf.br ^bb388
  ^bb388:  // pred: ^bb387
    %963 = arith.cmpi sgt, %960, %c127_i32 : i32
    cf.cond_br %963, ^bb389, ^bb390
  ^bb389:  // pred: ^bb388
    cf.br ^bb391(%c127_i32 : i32)
  ^bb390:  // pred: ^bb388
    cf.br ^bb391(%962 : i32)
  ^bb391(%964: i32):  // 2 preds: ^bb389, ^bb390
    cf.br ^bb392
  ^bb392:  // pred: ^bb391
    %965 = arith.trunci %964 : i32 to i8
    %966 = arith.extsi %872 : i32 to i64
    %967 = arith.muli %966, %c1561796795_i64 : i64
    %968 = arith.addi %967, %c68719476736_i64 : i64
    %969 = arith.cmpi sge, %872, %c0_i32 : i32
    cf.cond_br %969, ^bb393, ^bb394
  ^bb393:  // pred: ^bb392
    cf.br ^bb395(%c1073741824_i64 : i64)
  ^bb394:  // pred: ^bb392
    cf.br ^bb395(%c-1073741824_i64 : i64)
  ^bb395(%970: i64):  // 2 preds: ^bb393, ^bb394
    cf.br ^bb396
  ^bb396:  // pred: ^bb395
    %971 = arith.addi %970, %968 : i64
    %972 = arith.shrsi %971, %c37_i64 : i64
    %973 = arith.trunci %972 : i64 to i32
    %974 = arith.addi %973, %c-128_i32 : i32
    %975 = arith.cmpi slt, %974, %c-128_i32 : i32
    cf.cond_br %975, ^bb397, ^bb398
  ^bb397:  // pred: ^bb396
    cf.br ^bb399(%c-128_i32 : i32)
  ^bb398:  // pred: ^bb396
    cf.br ^bb399(%974 : i32)
  ^bb399(%976: i32):  // 2 preds: ^bb397, ^bb398
    cf.br ^bb400
  ^bb400:  // pred: ^bb399
    %977 = arith.cmpi sgt, %974, %c127_i32 : i32
    cf.cond_br %977, ^bb401, ^bb402
  ^bb401:  // pred: ^bb400
    cf.br ^bb403(%c127_i32 : i32)
  ^bb402:  // pred: ^bb400
    cf.br ^bb403(%976 : i32)
  ^bb403(%978: i32):  // 2 preds: ^bb401, ^bb402
    cf.br ^bb404
  ^bb404:  // pred: ^bb403
    %979 = arith.trunci %978 : i32 to i8
    %980 = arith.extsi %873 : i32 to i64
    %981 = arith.muli %980, %c1561796795_i64 : i64
    %982 = arith.addi %981, %c68719476736_i64 : i64
    %983 = arith.cmpi sge, %873, %c0_i32 : i32
    cf.cond_br %983, ^bb405, ^bb406
  ^bb405:  // pred: ^bb404
    cf.br ^bb407(%c1073741824_i64 : i64)
  ^bb406:  // pred: ^bb404
    cf.br ^bb407(%c-1073741824_i64 : i64)
  ^bb407(%984: i64):  // 2 preds: ^bb405, ^bb406
    cf.br ^bb408
  ^bb408:  // pred: ^bb407
    %985 = arith.addi %984, %982 : i64
    %986 = arith.shrsi %985, %c37_i64 : i64
    %987 = arith.trunci %986 : i64 to i32
    %988 = arith.addi %987, %c-128_i32 : i32
    %989 = arith.cmpi slt, %988, %c-128_i32 : i32
    cf.cond_br %989, ^bb409, ^bb410
  ^bb409:  // pred: ^bb408
    cf.br ^bb411(%c-128_i32 : i32)
  ^bb410:  // pred: ^bb408
    cf.br ^bb411(%988 : i32)
  ^bb411(%990: i32):  // 2 preds: ^bb409, ^bb410
    cf.br ^bb412
  ^bb412:  // pred: ^bb411
    %991 = arith.cmpi sgt, %988, %c127_i32 : i32
    cf.cond_br %991, ^bb413, ^bb414
  ^bb413:  // pred: ^bb412
    cf.br ^bb415(%c127_i32 : i32)
  ^bb414:  // pred: ^bb412
    cf.br ^bb415(%990 : i32)
  ^bb415(%992: i32):  // 2 preds: ^bb413, ^bb414
    cf.br ^bb416
  ^bb416:  // pred: ^bb415
    %993 = arith.trunci %992 : i32 to i8
    %994 = arith.extsi %874 : i32 to i64
    %995 = arith.muli %994, %c1561796795_i64 : i64
    %996 = arith.addi %995, %c68719476736_i64 : i64
    %997 = arith.cmpi sge, %874, %c0_i32 : i32
    cf.cond_br %997, ^bb417, ^bb418
  ^bb417:  // pred: ^bb416
    cf.br ^bb419(%c1073741824_i64 : i64)
  ^bb418:  // pred: ^bb416
    cf.br ^bb419(%c-1073741824_i64 : i64)
  ^bb419(%998: i64):  // 2 preds: ^bb417, ^bb418
    cf.br ^bb420
  ^bb420:  // pred: ^bb419
    %999 = arith.addi %998, %996 : i64
    %1000 = arith.shrsi %999, %c37_i64 : i64
    %1001 = arith.trunci %1000 : i64 to i32
    %1002 = arith.addi %1001, %c-128_i32 : i32
    %1003 = arith.cmpi slt, %1002, %c-128_i32 : i32
    cf.cond_br %1003, ^bb421, ^bb422
  ^bb421:  // pred: ^bb420
    cf.br ^bb423(%c-128_i32 : i32)
  ^bb422:  // pred: ^bb420
    cf.br ^bb423(%1002 : i32)
  ^bb423(%1004: i32):  // 2 preds: ^bb421, ^bb422
    cf.br ^bb424
  ^bb424:  // pred: ^bb423
    %1005 = arith.cmpi sgt, %1002, %c127_i32 : i32
    cf.cond_br %1005, ^bb425, ^bb426
  ^bb425:  // pred: ^bb424
    cf.br ^bb427(%c127_i32 : i32)
  ^bb426:  // pred: ^bb424
    cf.br ^bb427(%1004 : i32)
  ^bb427(%1006: i32):  // 2 preds: ^bb425, ^bb426
    cf.br ^bb428
  ^bb428:  // pred: ^bb427
    %1007 = arith.trunci %1006 : i32 to i8
    %1008 = arith.extsi %875 : i32 to i64
    %1009 = arith.muli %1008, %c1561796795_i64 : i64
    %1010 = arith.addi %1009, %c68719476736_i64 : i64
    %1011 = arith.cmpi sge, %875, %c0_i32 : i32
    cf.cond_br %1011, ^bb429, ^bb430
  ^bb429:  // pred: ^bb428
    cf.br ^bb431(%c1073741824_i64 : i64)
  ^bb430:  // pred: ^bb428
    cf.br ^bb431(%c-1073741824_i64 : i64)
  ^bb431(%1012: i64):  // 2 preds: ^bb429, ^bb430
    cf.br ^bb432
  ^bb432:  // pred: ^bb431
    %1013 = arith.addi %1012, %1010 : i64
    %1014 = arith.shrsi %1013, %c37_i64 : i64
    %1015 = arith.trunci %1014 : i64 to i32
    %1016 = arith.addi %1015, %c-128_i32 : i32
    %1017 = arith.cmpi slt, %1016, %c-128_i32 : i32
    cf.cond_br %1017, ^bb433, ^bb434
  ^bb433:  // pred: ^bb432
    cf.br ^bb435(%c-128_i32 : i32)
  ^bb434:  // pred: ^bb432
    cf.br ^bb435(%1016 : i32)
  ^bb435(%1018: i32):  // 2 preds: ^bb433, ^bb434
    cf.br ^bb436
  ^bb436:  // pred: ^bb435
    %1019 = arith.cmpi sgt, %1016, %c127_i32 : i32
    cf.cond_br %1019, ^bb437, ^bb438
  ^bb437:  // pred: ^bb436
    cf.br ^bb439(%c127_i32 : i32)
  ^bb438:  // pred: ^bb436
    cf.br ^bb439(%1018 : i32)
  ^bb439(%1020: i32):  // 2 preds: ^bb437, ^bb438
    cf.br ^bb440
  ^bb440:  // pred: ^bb439
    %1021 = arith.trunci %1020 : i32 to i8
    %1022 = arith.extsi %876 : i32 to i64
    %1023 = arith.muli %1022, %c1561796795_i64 : i64
    %1024 = arith.addi %1023, %c68719476736_i64 : i64
    %1025 = arith.cmpi sge, %876, %c0_i32 : i32
    cf.cond_br %1025, ^bb441, ^bb442
  ^bb441:  // pred: ^bb440
    cf.br ^bb443(%c1073741824_i64 : i64)
  ^bb442:  // pred: ^bb440
    cf.br ^bb443(%c-1073741824_i64 : i64)
  ^bb443(%1026: i64):  // 2 preds: ^bb441, ^bb442
    cf.br ^bb444
  ^bb444:  // pred: ^bb443
    %1027 = arith.addi %1026, %1024 : i64
    %1028 = arith.shrsi %1027, %c37_i64 : i64
    %1029 = arith.trunci %1028 : i64 to i32
    %1030 = arith.addi %1029, %c-128_i32 : i32
    %1031 = arith.cmpi slt, %1030, %c-128_i32 : i32
    cf.cond_br %1031, ^bb445, ^bb446
  ^bb445:  // pred: ^bb444
    cf.br ^bb447(%c-128_i32 : i32)
  ^bb446:  // pred: ^bb444
    cf.br ^bb447(%1030 : i32)
  ^bb447(%1032: i32):  // 2 preds: ^bb445, ^bb446
    cf.br ^bb448
  ^bb448:  // pred: ^bb447
    %1033 = arith.cmpi sgt, %1030, %c127_i32 : i32
    cf.cond_br %1033, ^bb449, ^bb450
  ^bb449:  // pred: ^bb448
    cf.br ^bb451(%c127_i32 : i32)
  ^bb450:  // pred: ^bb448
    cf.br ^bb451(%1032 : i32)
  ^bb451(%1034: i32):  // 2 preds: ^bb449, ^bb450
    cf.br ^bb452
  ^bb452:  // pred: ^bb451
    %1035 = arith.trunci %1034 : i32 to i8
    %1036 = arith.extsi %877 : i32 to i64
    %1037 = arith.muli %1036, %c1561796795_i64 : i64
    %1038 = arith.addi %1037, %c68719476736_i64 : i64
    %1039 = arith.cmpi sge, %877, %c0_i32 : i32
    cf.cond_br %1039, ^bb453, ^bb454
  ^bb453:  // pred: ^bb452
    cf.br ^bb455(%c1073741824_i64 : i64)
  ^bb454:  // pred: ^bb452
    cf.br ^bb455(%c-1073741824_i64 : i64)
  ^bb455(%1040: i64):  // 2 preds: ^bb453, ^bb454
    cf.br ^bb456
  ^bb456:  // pred: ^bb455
    %1041 = arith.addi %1040, %1038 : i64
    %1042 = arith.shrsi %1041, %c37_i64 : i64
    %1043 = arith.trunci %1042 : i64 to i32
    %1044 = arith.addi %1043, %c-128_i32 : i32
    %1045 = arith.cmpi slt, %1044, %c-128_i32 : i32
    cf.cond_br %1045, ^bb457, ^bb458
  ^bb457:  // pred: ^bb456
    cf.br ^bb459(%c-128_i32 : i32)
  ^bb458:  // pred: ^bb456
    cf.br ^bb459(%1044 : i32)
  ^bb459(%1046: i32):  // 2 preds: ^bb457, ^bb458
    cf.br ^bb460
  ^bb460:  // pred: ^bb459
    %1047 = arith.cmpi sgt, %1044, %c127_i32 : i32
    cf.cond_br %1047, ^bb461, ^bb462
  ^bb461:  // pred: ^bb460
    cf.br ^bb463(%c127_i32 : i32)
  ^bb462:  // pred: ^bb460
    cf.br ^bb463(%1046 : i32)
  ^bb463(%1048: i32):  // 2 preds: ^bb461, ^bb462
    cf.br ^bb464
  ^bb464:  // pred: ^bb463
    %1049 = arith.trunci %1048 : i32 to i8
    %1050 = arith.extsi %878 : i32 to i64
    %1051 = arith.muli %1050, %c1561796795_i64 : i64
    %1052 = arith.addi %1051, %c68719476736_i64 : i64
    %1053 = arith.cmpi sge, %878, %c0_i32 : i32
    cf.cond_br %1053, ^bb465, ^bb466
  ^bb465:  // pred: ^bb464
    cf.br ^bb467(%c1073741824_i64 : i64)
  ^bb466:  // pred: ^bb464
    cf.br ^bb467(%c-1073741824_i64 : i64)
  ^bb467(%1054: i64):  // 2 preds: ^bb465, ^bb466
    cf.br ^bb468
  ^bb468:  // pred: ^bb467
    %1055 = arith.addi %1054, %1052 : i64
    %1056 = arith.shrsi %1055, %c37_i64 : i64
    %1057 = arith.trunci %1056 : i64 to i32
    %1058 = arith.addi %1057, %c-128_i32 : i32
    %1059 = arith.cmpi slt, %1058, %c-128_i32 : i32
    cf.cond_br %1059, ^bb469, ^bb470
  ^bb469:  // pred: ^bb468
    cf.br ^bb471(%c-128_i32 : i32)
  ^bb470:  // pred: ^bb468
    cf.br ^bb471(%1058 : i32)
  ^bb471(%1060: i32):  // 2 preds: ^bb469, ^bb470
    cf.br ^bb472
  ^bb472:  // pred: ^bb471
    %1061 = arith.cmpi sgt, %1058, %c127_i32 : i32
    cf.cond_br %1061, ^bb473, ^bb474
  ^bb473:  // pred: ^bb472
    cf.br ^bb475(%c127_i32 : i32)
  ^bb474:  // pred: ^bb472
    cf.br ^bb475(%1060 : i32)
  ^bb475(%1062: i32):  // 2 preds: ^bb473, ^bb474
    cf.br ^bb476
  ^bb476:  // pred: ^bb475
    %1063 = arith.trunci %1062 : i32 to i8
    %1064 = arith.extsi %879 : i32 to i64
    %1065 = arith.muli %1064, %c1561796795_i64 : i64
    %1066 = arith.addi %1065, %c68719476736_i64 : i64
    %1067 = arith.cmpi sge, %879, %c0_i32 : i32
    cf.cond_br %1067, ^bb477, ^bb478
  ^bb477:  // pred: ^bb476
    cf.br ^bb479(%c1073741824_i64 : i64)
  ^bb478:  // pred: ^bb476
    cf.br ^bb479(%c-1073741824_i64 : i64)
  ^bb479(%1068: i64):  // 2 preds: ^bb477, ^bb478
    cf.br ^bb480
  ^bb480:  // pred: ^bb479
    %1069 = arith.addi %1068, %1066 : i64
    %1070 = arith.shrsi %1069, %c37_i64 : i64
    %1071 = arith.trunci %1070 : i64 to i32
    %1072 = arith.addi %1071, %c-128_i32 : i32
    %1073 = arith.cmpi slt, %1072, %c-128_i32 : i32
    cf.cond_br %1073, ^bb481, ^bb482
  ^bb481:  // pred: ^bb480
    cf.br ^bb483(%c-128_i32 : i32)
  ^bb482:  // pred: ^bb480
    cf.br ^bb483(%1072 : i32)
  ^bb483(%1074: i32):  // 2 preds: ^bb481, ^bb482
    cf.br ^bb484
  ^bb484:  // pred: ^bb483
    %1075 = arith.cmpi sgt, %1072, %c127_i32 : i32
    cf.cond_br %1075, ^bb485, ^bb486
  ^bb485:  // pred: ^bb484
    cf.br ^bb487(%c127_i32 : i32)
  ^bb486:  // pred: ^bb484
    cf.br ^bb487(%1074 : i32)
  ^bb487(%1076: i32):  // 2 preds: ^bb485, ^bb486
    cf.br ^bb488
  ^bb488:  // pred: ^bb487
    %1077 = arith.trunci %1076 : i32 to i8
    %1078 = arith.extsi %880 : i32 to i64
    %1079 = arith.muli %1078, %c1561796795_i64 : i64
    %1080 = arith.addi %1079, %c68719476736_i64 : i64
    %1081 = arith.cmpi sge, %880, %c0_i32 : i32
    cf.cond_br %1081, ^bb489, ^bb490
  ^bb489:  // pred: ^bb488
    cf.br ^bb491(%c1073741824_i64 : i64)
  ^bb490:  // pred: ^bb488
    cf.br ^bb491(%c-1073741824_i64 : i64)
  ^bb491(%1082: i64):  // 2 preds: ^bb489, ^bb490
    cf.br ^bb492
  ^bb492:  // pred: ^bb491
    %1083 = arith.addi %1082, %1080 : i64
    %1084 = arith.shrsi %1083, %c37_i64 : i64
    %1085 = arith.trunci %1084 : i64 to i32
    %1086 = arith.addi %1085, %c-128_i32 : i32
    %1087 = arith.cmpi slt, %1086, %c-128_i32 : i32
    cf.cond_br %1087, ^bb493, ^bb494
  ^bb493:  // pred: ^bb492
    cf.br ^bb495(%c-128_i32 : i32)
  ^bb494:  // pred: ^bb492
    cf.br ^bb495(%1086 : i32)
  ^bb495(%1088: i32):  // 2 preds: ^bb493, ^bb494
    cf.br ^bb496
  ^bb496:  // pred: ^bb495
    %1089 = arith.cmpi sgt, %1086, %c127_i32 : i32
    cf.cond_br %1089, ^bb497, ^bb498
  ^bb497:  // pred: ^bb496
    cf.br ^bb499(%c127_i32 : i32)
  ^bb498:  // pred: ^bb496
    cf.br ^bb499(%1088 : i32)
  ^bb499(%1090: i32):  // 2 preds: ^bb497, ^bb498
    cf.br ^bb500
  ^bb500:  // pred: ^bb499
    %1091 = arith.trunci %1090 : i32 to i8
    %1092 = arith.extsi %881 : i32 to i64
    %1093 = arith.muli %1092, %c1561796795_i64 : i64
    %1094 = arith.addi %1093, %c68719476736_i64 : i64
    %1095 = arith.cmpi sge, %881, %c0_i32 : i32
    cf.cond_br %1095, ^bb501, ^bb502
  ^bb501:  // pred: ^bb500
    cf.br ^bb503(%c1073741824_i64 : i64)
  ^bb502:  // pred: ^bb500
    cf.br ^bb503(%c-1073741824_i64 : i64)
  ^bb503(%1096: i64):  // 2 preds: ^bb501, ^bb502
    cf.br ^bb504
  ^bb504:  // pred: ^bb503
    %1097 = arith.addi %1096, %1094 : i64
    %1098 = arith.shrsi %1097, %c37_i64 : i64
    %1099 = arith.trunci %1098 : i64 to i32
    %1100 = arith.addi %1099, %c-128_i32 : i32
    %1101 = arith.cmpi slt, %1100, %c-128_i32 : i32
    cf.cond_br %1101, ^bb505, ^bb506
  ^bb505:  // pred: ^bb504
    cf.br ^bb507(%c-128_i32 : i32)
  ^bb506:  // pred: ^bb504
    cf.br ^bb507(%1100 : i32)
  ^bb507(%1102: i32):  // 2 preds: ^bb505, ^bb506
    cf.br ^bb508
  ^bb508:  // pred: ^bb507
    %1103 = arith.cmpi sgt, %1100, %c127_i32 : i32
    cf.cond_br %1103, ^bb509, ^bb510
  ^bb509:  // pred: ^bb508
    cf.br ^bb511(%c127_i32 : i32)
  ^bb510:  // pred: ^bb508
    cf.br ^bb511(%1102 : i32)
  ^bb511(%1104: i32):  // 2 preds: ^bb509, ^bb510
    cf.br ^bb512
  ^bb512:  // pred: ^bb511
    %1105 = arith.trunci %1104 : i32 to i8
    %1106 = arith.cmpi slt, %895, %c-128_i8 : i8
    cf.cond_br %1106, ^bb513, ^bb514
  ^bb513:  // pred: ^bb512
    cf.br ^bb515(%c-128_i8 : i8)
  ^bb514:  // pred: ^bb512
    cf.br ^bb515(%895 : i8)
  ^bb515(%1107: i8):  // 2 preds: ^bb513, ^bb514
    cf.br ^bb516
  ^bb516:  // pred: ^bb515
    %1108 = arith.cmpi sgt, %895, %c127_i8 : i8
    cf.cond_br %1108, ^bb517, ^bb518
  ^bb517:  // pred: ^bb516
    cf.br ^bb519(%c127_i8 : i8)
  ^bb518:  // pred: ^bb516
    cf.br ^bb519(%1107 : i8)
  ^bb519(%1109: i8):  // 2 preds: ^bb517, ^bb518
    cf.br ^bb520
  ^bb520:  // pred: ^bb519
    %1110 = arith.cmpi slt, %909, %c-128_i8 : i8
    cf.cond_br %1110, ^bb521, ^bb522
  ^bb521:  // pred: ^bb520
    cf.br ^bb523(%c-128_i8 : i8)
  ^bb522:  // pred: ^bb520
    cf.br ^bb523(%909 : i8)
  ^bb523(%1111: i8):  // 2 preds: ^bb521, ^bb522
    cf.br ^bb524
  ^bb524:  // pred: ^bb523
    %1112 = arith.cmpi sgt, %909, %c127_i8 : i8
    cf.cond_br %1112, ^bb525, ^bb526
  ^bb525:  // pred: ^bb524
    cf.br ^bb527(%c127_i8 : i8)
  ^bb526:  // pred: ^bb524
    cf.br ^bb527(%1111 : i8)
  ^bb527(%1113: i8):  // 2 preds: ^bb525, ^bb526
    cf.br ^bb528
  ^bb528:  // pred: ^bb527
    %1114 = arith.cmpi slt, %923, %c-128_i8 : i8
    cf.cond_br %1114, ^bb529, ^bb530
  ^bb529:  // pred: ^bb528
    cf.br ^bb531(%c-128_i8 : i8)
  ^bb530:  // pred: ^bb528
    cf.br ^bb531(%923 : i8)
  ^bb531(%1115: i8):  // 2 preds: ^bb529, ^bb530
    cf.br ^bb532
  ^bb532:  // pred: ^bb531
    %1116 = arith.cmpi sgt, %923, %c127_i8 : i8
    cf.cond_br %1116, ^bb533, ^bb534
  ^bb533:  // pred: ^bb532
    cf.br ^bb535(%c127_i8 : i8)
  ^bb534:  // pred: ^bb532
    cf.br ^bb535(%1115 : i8)
  ^bb535(%1117: i8):  // 2 preds: ^bb533, ^bb534
    cf.br ^bb536
  ^bb536:  // pred: ^bb535
    %1118 = arith.cmpi slt, %937, %c-128_i8 : i8
    cf.cond_br %1118, ^bb537, ^bb538
  ^bb537:  // pred: ^bb536
    cf.br ^bb539(%c-128_i8 : i8)
  ^bb538:  // pred: ^bb536
    cf.br ^bb539(%937 : i8)
  ^bb539(%1119: i8):  // 2 preds: ^bb537, ^bb538
    cf.br ^bb540
  ^bb540:  // pred: ^bb539
    %1120 = arith.cmpi sgt, %937, %c127_i8 : i8
    cf.cond_br %1120, ^bb541, ^bb542
  ^bb541:  // pred: ^bb540
    cf.br ^bb543(%c127_i8 : i8)
  ^bb542:  // pred: ^bb540
    cf.br ^bb543(%1119 : i8)
  ^bb543(%1121: i8):  // 2 preds: ^bb541, ^bb542
    cf.br ^bb544
  ^bb544:  // pred: ^bb543
    %1122 = arith.cmpi slt, %951, %c-128_i8 : i8
    cf.cond_br %1122, ^bb545, ^bb546
  ^bb545:  // pred: ^bb544
    cf.br ^bb547(%c-128_i8 : i8)
  ^bb546:  // pred: ^bb544
    cf.br ^bb547(%951 : i8)
  ^bb547(%1123: i8):  // 2 preds: ^bb545, ^bb546
    cf.br ^bb548
  ^bb548:  // pred: ^bb547
    %1124 = arith.cmpi sgt, %951, %c127_i8 : i8
    cf.cond_br %1124, ^bb549, ^bb550
  ^bb549:  // pred: ^bb548
    cf.br ^bb551(%c127_i8 : i8)
  ^bb550:  // pred: ^bb548
    cf.br ^bb551(%1123 : i8)
  ^bb551(%1125: i8):  // 2 preds: ^bb549, ^bb550
    cf.br ^bb552
  ^bb552:  // pred: ^bb551
    %1126 = arith.cmpi slt, %965, %c-128_i8 : i8
    cf.cond_br %1126, ^bb553, ^bb554
  ^bb553:  // pred: ^bb552
    cf.br ^bb555(%c-128_i8 : i8)
  ^bb554:  // pred: ^bb552
    cf.br ^bb555(%965 : i8)
  ^bb555(%1127: i8):  // 2 preds: ^bb553, ^bb554
    cf.br ^bb556
  ^bb556:  // pred: ^bb555
    %1128 = arith.cmpi sgt, %965, %c127_i8 : i8
    cf.cond_br %1128, ^bb557, ^bb558
  ^bb557:  // pred: ^bb556
    cf.br ^bb559(%c127_i8 : i8)
  ^bb558:  // pred: ^bb556
    cf.br ^bb559(%1127 : i8)
  ^bb559(%1129: i8):  // 2 preds: ^bb557, ^bb558
    cf.br ^bb560
  ^bb560:  // pred: ^bb559
    %1130 = arith.cmpi slt, %979, %c-128_i8 : i8
    cf.cond_br %1130, ^bb561, ^bb562
  ^bb561:  // pred: ^bb560
    cf.br ^bb563(%c-128_i8 : i8)
  ^bb562:  // pred: ^bb560
    cf.br ^bb563(%979 : i8)
  ^bb563(%1131: i8):  // 2 preds: ^bb561, ^bb562
    cf.br ^bb564
  ^bb564:  // pred: ^bb563
    %1132 = arith.cmpi sgt, %979, %c127_i8 : i8
    cf.cond_br %1132, ^bb565, ^bb566
  ^bb565:  // pred: ^bb564
    cf.br ^bb567(%c127_i8 : i8)
  ^bb566:  // pred: ^bb564
    cf.br ^bb567(%1131 : i8)
  ^bb567(%1133: i8):  // 2 preds: ^bb565, ^bb566
    cf.br ^bb568
  ^bb568:  // pred: ^bb567
    %1134 = arith.cmpi slt, %993, %c-128_i8 : i8
    cf.cond_br %1134, ^bb569, ^bb570
  ^bb569:  // pred: ^bb568
    cf.br ^bb571(%c-128_i8 : i8)
  ^bb570:  // pred: ^bb568
    cf.br ^bb571(%993 : i8)
  ^bb571(%1135: i8):  // 2 preds: ^bb569, ^bb570
    cf.br ^bb572
  ^bb572:  // pred: ^bb571
    %1136 = arith.cmpi sgt, %993, %c127_i8 : i8
    cf.cond_br %1136, ^bb573, ^bb574
  ^bb573:  // pred: ^bb572
    cf.br ^bb575(%c127_i8 : i8)
  ^bb574:  // pred: ^bb572
    cf.br ^bb575(%1135 : i8)
  ^bb575(%1137: i8):  // 2 preds: ^bb573, ^bb574
    cf.br ^bb576
  ^bb576:  // pred: ^bb575
    %1138 = arith.cmpi slt, %1007, %c-128_i8 : i8
    cf.cond_br %1138, ^bb577, ^bb578
  ^bb577:  // pred: ^bb576
    cf.br ^bb579(%c-128_i8 : i8)
  ^bb578:  // pred: ^bb576
    cf.br ^bb579(%1007 : i8)
  ^bb579(%1139: i8):  // 2 preds: ^bb577, ^bb578
    cf.br ^bb580
  ^bb580:  // pred: ^bb579
    %1140 = arith.cmpi sgt, %1007, %c127_i8 : i8
    cf.cond_br %1140, ^bb581, ^bb582
  ^bb581:  // pred: ^bb580
    cf.br ^bb583(%c127_i8 : i8)
  ^bb582:  // pred: ^bb580
    cf.br ^bb583(%1139 : i8)
  ^bb583(%1141: i8):  // 2 preds: ^bb581, ^bb582
    cf.br ^bb584
  ^bb584:  // pred: ^bb583
    %1142 = arith.cmpi slt, %1021, %c-128_i8 : i8
    cf.cond_br %1142, ^bb585, ^bb586
  ^bb585:  // pred: ^bb584
    cf.br ^bb587(%c-128_i8 : i8)
  ^bb586:  // pred: ^bb584
    cf.br ^bb587(%1021 : i8)
  ^bb587(%1143: i8):  // 2 preds: ^bb585, ^bb586
    cf.br ^bb588
  ^bb588:  // pred: ^bb587
    %1144 = arith.cmpi sgt, %1021, %c127_i8 : i8
    cf.cond_br %1144, ^bb589, ^bb590
  ^bb589:  // pred: ^bb588
    cf.br ^bb591(%c127_i8 : i8)
  ^bb590:  // pred: ^bb588
    cf.br ^bb591(%1143 : i8)
  ^bb591(%1145: i8):  // 2 preds: ^bb589, ^bb590
    cf.br ^bb592
  ^bb592:  // pred: ^bb591
    %1146 = arith.cmpi slt, %1035, %c-128_i8 : i8
    cf.cond_br %1146, ^bb593, ^bb594
  ^bb593:  // pred: ^bb592
    cf.br ^bb595(%c-128_i8 : i8)
  ^bb594:  // pred: ^bb592
    cf.br ^bb595(%1035 : i8)
  ^bb595(%1147: i8):  // 2 preds: ^bb593, ^bb594
    cf.br ^bb596
  ^bb596:  // pred: ^bb595
    %1148 = arith.cmpi sgt, %1035, %c127_i8 : i8
    cf.cond_br %1148, ^bb597, ^bb598
  ^bb597:  // pred: ^bb596
    cf.br ^bb599(%c127_i8 : i8)
  ^bb598:  // pred: ^bb596
    cf.br ^bb599(%1147 : i8)
  ^bb599(%1149: i8):  // 2 preds: ^bb597, ^bb598
    cf.br ^bb600
  ^bb600:  // pred: ^bb599
    %1150 = arith.cmpi slt, %1049, %c-128_i8 : i8
    cf.cond_br %1150, ^bb601, ^bb602
  ^bb601:  // pred: ^bb600
    cf.br ^bb603(%c-128_i8 : i8)
  ^bb602:  // pred: ^bb600
    cf.br ^bb603(%1049 : i8)
  ^bb603(%1151: i8):  // 2 preds: ^bb601, ^bb602
    cf.br ^bb604
  ^bb604:  // pred: ^bb603
    %1152 = arith.cmpi sgt, %1049, %c127_i8 : i8
    cf.cond_br %1152, ^bb605, ^bb606
  ^bb605:  // pred: ^bb604
    cf.br ^bb607(%c127_i8 : i8)
  ^bb606:  // pred: ^bb604
    cf.br ^bb607(%1151 : i8)
  ^bb607(%1153: i8):  // 2 preds: ^bb605, ^bb606
    cf.br ^bb608
  ^bb608:  // pred: ^bb607
    %1154 = arith.cmpi slt, %1063, %c-128_i8 : i8
    cf.cond_br %1154, ^bb609, ^bb610
  ^bb609:  // pred: ^bb608
    cf.br ^bb611(%c-128_i8 : i8)
  ^bb610:  // pred: ^bb608
    cf.br ^bb611(%1063 : i8)
  ^bb611(%1155: i8):  // 2 preds: ^bb609, ^bb610
    cf.br ^bb612
  ^bb612:  // pred: ^bb611
    %1156 = arith.cmpi sgt, %1063, %c127_i8 : i8
    cf.cond_br %1156, ^bb613, ^bb614
  ^bb613:  // pred: ^bb612
    cf.br ^bb615(%c127_i8 : i8)
  ^bb614:  // pred: ^bb612
    cf.br ^bb615(%1155 : i8)
  ^bb615(%1157: i8):  // 2 preds: ^bb613, ^bb614
    cf.br ^bb616
  ^bb616:  // pred: ^bb615
    %1158 = arith.cmpi slt, %1077, %c-128_i8 : i8
    cf.cond_br %1158, ^bb617, ^bb618
  ^bb617:  // pred: ^bb616
    cf.br ^bb619(%c-128_i8 : i8)
  ^bb618:  // pred: ^bb616
    cf.br ^bb619(%1077 : i8)
  ^bb619(%1159: i8):  // 2 preds: ^bb617, ^bb618
    cf.br ^bb620
  ^bb620:  // pred: ^bb619
    %1160 = arith.cmpi sgt, %1077, %c127_i8 : i8
    cf.cond_br %1160, ^bb621, ^bb622
  ^bb621:  // pred: ^bb620
    cf.br ^bb623(%c127_i8 : i8)
  ^bb622:  // pred: ^bb620
    cf.br ^bb623(%1159 : i8)
  ^bb623(%1161: i8):  // 2 preds: ^bb621, ^bb622
    cf.br ^bb624
  ^bb624:  // pred: ^bb623
    %1162 = arith.cmpi slt, %1091, %c-128_i8 : i8
    cf.cond_br %1162, ^bb625, ^bb626
  ^bb625:  // pred: ^bb624
    cf.br ^bb627(%c-128_i8 : i8)
  ^bb626:  // pred: ^bb624
    cf.br ^bb627(%1091 : i8)
  ^bb627(%1163: i8):  // 2 preds: ^bb625, ^bb626
    cf.br ^bb628
  ^bb628:  // pred: ^bb627
    %1164 = arith.cmpi sgt, %1091, %c127_i8 : i8
    cf.cond_br %1164, ^bb629, ^bb630
  ^bb629:  // pred: ^bb628
    cf.br ^bb631(%c127_i8 : i8)
  ^bb630:  // pred: ^bb628
    cf.br ^bb631(%1163 : i8)
  ^bb631(%1165: i8):  // 2 preds: ^bb629, ^bb630
    cf.br ^bb632
  ^bb632:  // pred: ^bb631
    %1166 = arith.cmpi slt, %1105, %c-128_i8 : i8
    cf.cond_br %1166, ^bb633, ^bb634
  ^bb633:  // pred: ^bb632
    cf.br ^bb635(%c-128_i8 : i8)
  ^bb634:  // pred: ^bb632
    cf.br ^bb635(%1105 : i8)
  ^bb635(%1167: i8):  // 2 preds: ^bb633, ^bb634
    cf.br ^bb636
  ^bb636:  // pred: ^bb635
    %1168 = arith.cmpi sgt, %1105, %c127_i8 : i8
    cf.cond_br %1168, ^bb637, ^bb638
  ^bb637:  // pred: ^bb636
    cf.br ^bb639(%c127_i8 : i8)
  ^bb638:  // pred: ^bb636
    cf.br ^bb639(%1167 : i8)
  ^bb639(%1169: i8):  // 2 preds: ^bb637, ^bb638
    cf.br ^bb640
  ^bb640:  // pred: ^bb639
    %1170 = arith.extsi %1109 : i8 to i32
    %1171 = arith.subi %1170, %c-128_i32 : i32
    %1172 = arith.muli %1171, %c-39_i32 : i32
    %1173 = arith.addi %c0_i32, %1172 : i32
    %1174 = arith.extsi %1113 : i8 to i32
    %1175 = arith.subi %1174, %c-128_i32 : i32
    %1176 = arith.muli %1175, %c59_i32 : i32
    %1177 = arith.addi %1173, %1176 : i32
    %1178 = arith.extsi %1117 : i8 to i32
    %1179 = arith.subi %1178, %c-128_i32 : i32
    %1180 = arith.muli %1179, %c39_i32 : i32
    %1181 = arith.addi %1177, %1180 : i32
    %1182 = arith.extsi %1121 : i8 to i32
    %1183 = arith.subi %1182, %c-128_i32 : i32
    %1184 = arith.muli %1183, %c21_i32 : i32
    %1185 = arith.addi %1181, %1184 : i32
    %1186 = arith.extsi %1125 : i8 to i32
    %1187 = arith.subi %1186, %c-128_i32 : i32
    %1188 = arith.muli %1187, %c28_i32 : i32
    %1189 = arith.addi %1185, %1188 : i32
    %1190 = arith.extsi %1129 : i8 to i32
    %1191 = arith.subi %1190, %c-128_i32 : i32
    %1192 = arith.muli %1191, %c-32_i32 : i32
    %1193 = arith.addi %1189, %1192 : i32
    %1194 = arith.extsi %1133 : i8 to i32
    %1195 = arith.subi %1194, %c-128_i32 : i32
    %1196 = arith.muli %1195, %c-34_i32 : i32
    %1197 = arith.addi %1193, %1196 : i32
    %1198 = arith.extsi %1137 : i8 to i32
    %1199 = arith.subi %1198, %c-128_i32 : i32
    %1200 = arith.muli %1199, %c-35_i32 : i32
    %1201 = arith.addi %1197, %1200 : i32
    %1202 = arith.extsi %1141 : i8 to i32
    %1203 = arith.subi %1202, %c-128_i32 : i32
    %1204 = arith.muli %1203, %c15_i32 : i32
    %1205 = arith.addi %1201, %1204 : i32
    %1206 = arith.extsi %1145 : i8 to i32
    %1207 = arith.subi %1206, %c-128_i32 : i32
    %1208 = arith.muli %1207, %c27_i32 : i32
    %1209 = arith.addi %1205, %1208 : i32
    %1210 = arith.extsi %1149 : i8 to i32
    %1211 = arith.subi %1210, %c-128_i32 : i32
    %1212 = arith.muli %1211, %c-59_i32 : i32
    %1213 = arith.addi %1209, %1212 : i32
    %1214 = arith.extsi %1153 : i8 to i32
    %1215 = arith.subi %1214, %c-128_i32 : i32
    %1216 = arith.muli %1215, %c-41_i32 : i32
    %1217 = arith.addi %1213, %1216 : i32
    %1218 = arith.extsi %1157 : i8 to i32
    %1219 = arith.subi %1218, %c-128_i32 : i32
    %1220 = arith.muli %1219, %c18_i32 : i32
    %1221 = arith.addi %1217, %1220 : i32
    %1222 = arith.extsi %1161 : i8 to i32
    %1223 = arith.subi %1222, %c-128_i32 : i32
    %1224 = arith.muli %1223, %c-35_i32 : i32
    %1225 = arith.addi %1221, %1224 : i32
    %1226 = arith.extsi %1165 : i8 to i32
    %1227 = arith.subi %1226, %c-128_i32 : i32
    %1228 = arith.muli %1227, %c-7_i32 : i32
    %1229 = arith.addi %1225, %1228 : i32
    %1230 = arith.extsi %1169 : i8 to i32
    %1231 = arith.subi %1230, %c-128_i32 : i32
    %1232 = arith.muli %1231, %c127_i32 : i32
    %1233 = arith.addi %1229, %1232 : i32
    %1234 = arith.addi %1233, %c429_i32 : i32
    %1235 = arith.extsi %1234 : i32 to i64
    %1236 = arith.muli %1235, %c1630361836_i64 : i64
    %1237 = arith.addi %1236, %c34359738368_i64 : i64
    %1238 = arith.cmpi sge, %1234, %c0_i32 : i32
    cf.cond_br %1238, ^bb641, ^bb642
  ^bb641:  // pred: ^bb640
    cf.br ^bb643(%c1073741824_i64 : i64)
  ^bb642:  // pred: ^bb640
    cf.br ^bb643(%c-1073741824_i64 : i64)
  ^bb643(%1239: i64):  // 2 preds: ^bb641, ^bb642
    cf.br ^bb644
  ^bb644:  // pred: ^bb643
    %1240 = arith.addi %1239, %1237 : i64
    %1241 = arith.shrsi %1240, %c36_i64 : i64
    %1242 = arith.trunci %1241 : i64 to i32
    %1243 = arith.addi %1242, %c5_i32 : i32
    %1244 = arith.cmpi slt, %1243, %c-128_i32 : i32
    cf.cond_br %1244, ^bb645, ^bb646
  ^bb645:  // pred: ^bb644
    cf.br ^bb647(%c-128_i32 : i32)
  ^bb646:  // pred: ^bb644
    cf.br ^bb647(%1243 : i32)
  ^bb647(%1245: i32):  // 2 preds: ^bb645, ^bb646
    cf.br ^bb648
  ^bb648:  // pred: ^bb647
    %1246 = arith.cmpi sgt, %1243, %c127_i32 : i32
    cf.cond_br %1246, ^bb649, ^bb650
  ^bb649:  // pred: ^bb648
    cf.br ^bb651(%c127_i32 : i32)
  ^bb650:  // pred: ^bb648
    cf.br ^bb651(%1245 : i32)
  ^bb651(%1247: i32):  // 2 preds: ^bb649, ^bb650
    cf.br ^bb652
  ^bb652:  // pred: ^bb651
    %1248 = arith.trunci %1247 : i32 to i8
    return %1248 : i8
  }
}

