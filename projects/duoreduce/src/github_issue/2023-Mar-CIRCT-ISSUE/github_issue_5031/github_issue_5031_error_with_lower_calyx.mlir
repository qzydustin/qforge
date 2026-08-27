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
    %1022 = arith.extsi %12 : i32 to i64
    %1023 = arith.muli %1022, %1022 : i64
    %1024 = arith.addi %1023, %1022 : i64
    %1025 = arith.cmpi sge, %2, %4 : i32
    cf.cond_br %1025, ^bb441, ^bb442
  ^bb441:  // pred: ^bb440
    cf.br ^bb443(%1022 : i64)
  ^bb442:  // pred: ^bb440
    cf.br ^bb443(%1023 : i64)
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
    %1036 = arith.extsi %1034 : i32 to i64
    %1037 = arith.muli %1036, %c1561796795_i64 : i64
    %1038 = arith.addi %1037, %c68719476736_i64 : i64
    %1039 = arith.cmpi sge, %2, %c0_i32 : i32
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
    %1050 = arith.extsi %1048 : i32 to i64
    %1051 = arith.muli %1050, %c1561796795_i64 : i64
    %1052 = arith.addi %1051, %c68719476736_i64 : i64
    %1053 = arith.cmpi sge, %2, %c0_i32 : i32
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
    %1064 = arith.extsi %1062 : i32 to i64
    %1065 = arith.muli %1064, %c1561796795_i64 : i64
    %1066 = arith.addi %1065, %c68719476736_i64 : i64
    %1067 = arith.cmpi sge, %2, %c0_i32 : i32
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
    %1078 = arith.extsi %1074 : i32 to i64
    %1079 = arith.muli %1078, %c1561796795_i64 : i64
    %1080 = arith.addi %1079, %c68719476736_i64 : i64
    %1081 = arith.cmpi sge, %2, %c0_i32 : i32
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
    %1092 = arith.extsi %1090 : i32 to i64
    %1093 = arith.muli %1092, %c1561796795_i64 : i64
    %1094 = arith.addi %1093, %c68719476736_i64 : i64
    %1095 = arith.cmpi sge, %2, %c0_i32 : i32
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
    %1106 = arith.cmpi slt, %c-128_i8, %c-128_i8 : i8
    cf.cond_br %1106, ^bb513, ^bb514
  ^bb513:  // pred: ^bb512
    cf.br ^bb515(%c-128_i8 : i8)
  ^bb514:  // pred: ^bb512
    cf.br ^bb515(%c-128_i8 : i8)
  ^bb515(%1107: i8):  // 2 preds: ^bb513, ^bb514
    cf.br ^bb516
  ^bb516:  // pred: ^bb515
    %1108 = arith.cmpi sgt, %c-128_i8, %c127_i8 : i8
    cf.cond_br %1108, ^bb517, ^bb518
  ^bb517:  // pred: ^bb516
    cf.br ^bb519(%c127_i8 : i8)
  ^bb518:  // pred: ^bb516
    cf.br ^bb519(%1107 : i8)
  ^bb519(%1109: i8):  // 2 preds: ^bb517, ^bb518
    cf.br ^bb520
  ^bb520:  // pred: ^bb519
    %1110 = arith.cmpi slt, %c-128_i8, %c-128_i8 : i8
    cf.cond_br %1110, ^bb521, ^bb522
  ^bb521:  // pred: ^bb520
    cf.br ^bb523(%c-128_i8 : i8)
  ^bb522:  // pred: ^bb520
    cf.br ^bb523(%c-128_i8 : i8)
  ^bb523(%1111: i8):  // 2 preds: ^bb521, ^bb522
    cf.br ^bb524
  ^bb524:  // pred: ^bb523
    %1112 = arith.cmpi sgt, %c-128_i8, %c127_i8 : i8
    cf.cond_br %1112, ^bb525, ^bb526
  ^bb525:  // pred: ^bb524
    cf.br ^bb527(%c127_i8 : i8)
  ^bb526:  // pred: ^bb524
    cf.br ^bb527(%1111 : i8)
  ^bb527(%1113: i8):  // 2 preds: ^bb525, ^bb526
    cf.br ^bb528
  ^bb528:  // pred: ^bb527
    %1114 = arith.cmpi slt, %c-128_i8, %c-128_i8 : i8
    cf.cond_br %1114, ^bb529, ^bb530
  ^bb529:  // pred: ^bb528
    cf.br ^bb531(%c-128_i8 : i8)
  ^bb530:  // pred: ^bb528
    cf.br ^bb531(%c-128_i8 : i8)
  ^bb531(%1115: i8):  // 2 preds: ^bb529, ^bb530
    cf.br ^bb532
  ^bb532:  // pred: ^bb531
    %1116 = arith.cmpi sgt, %c-128_i8, %c127_i8 : i8
    cf.cond_br %1116, ^bb533, ^bb534
  ^bb533:  // pred: ^bb532
    cf.br ^bb535(%c127_i8 : i8)
  ^bb534:  // pred: ^bb532
    cf.br ^bb535(%1115 : i8)
  ^bb535(%1117: i8):  // 2 preds: ^bb533, ^bb534
    cf.br ^bb536
  ^bb536:  // pred: ^bb535
    %1118 = arith.cmpi slt, %c-128_i8, %c-128_i8 : i8
    cf.cond_br %1118, ^bb537, ^bb538
  ^bb537:  // pred: ^bb536
    cf.br ^bb539(%c-128_i8 : i8)
  ^bb538:  // pred: ^bb536
    cf.br ^bb539(%c-128_i8 : i8)
  ^bb539(%1119: i8):  // 2 preds: ^bb537, ^bb538
    cf.br ^bb540
  ^bb540:  // pred: ^bb539
    %1120 = arith.cmpi sgt, %c-128_i8, %c127_i8 : i8
    cf.cond_br %1120, ^bb541, ^bb542
  ^bb541:  // pred: ^bb540
    cf.br ^bb543(%c127_i8 : i8)
  ^bb542:  // pred: ^bb540
    cf.br ^bb543(%1119 : i8)
  ^bb543(%1121: i8):  // 2 preds: ^bb541, ^bb542
    cf.br ^bb544
  ^bb544:  // pred: ^bb543
    %1122 = arith.cmpi slt, %c-128_i8, %c-128_i8 : i8
    cf.cond_br %1122, ^bb545, ^bb546
  ^bb545:  // pred: ^bb544
    cf.br ^bb547(%c-128_i8 : i8)
  ^bb546:  // pred: ^bb544
    cf.br ^bb547(%c-128_i8 : i8)
  ^bb547(%1123: i8):  // 2 preds: ^bb545, ^bb546
    cf.br ^bb548
  ^bb548:  // pred: ^bb547
    %1124 = arith.cmpi sgt, %c-128_i8, %c127_i8 : i8
    cf.cond_br %1124, ^bb549, ^bb550
  ^bb549:  // pred: ^bb548
    cf.br ^bb551(%c127_i8 : i8)
  ^bb550:  // pred: ^bb548
    cf.br ^bb551(%1123 : i8)
  ^bb551(%1125: i8):  // 2 preds: ^bb549, ^bb550
    cf.br ^bb552
  ^bb552:  // pred: ^bb551
    %1126 = arith.cmpi slt, %c-128_i8, %c-128_i8 : i8
    cf.cond_br %1126, ^bb553, ^bb554
  ^bb553:  // pred: ^bb552
    cf.br ^bb555(%c-128_i8 : i8)
  ^bb554:  // pred: ^bb552
    cf.br ^bb555(%c-128_i8 : i8)
  ^bb555(%1127: i8):  // 2 preds: ^bb553, ^bb554
    cf.br ^bb556
  ^bb556:  // pred: ^bb555
    %1128 = arith.cmpi sgt, %c-128_i8, %c127_i8 : i8
    cf.cond_br %1128, ^bb557, ^bb558
  ^bb557:  // pred: ^bb556
    cf.br ^bb559(%c127_i8 : i8)
  ^bb558:  // pred: ^bb556
    cf.br ^bb559(%1127 : i8)
  ^bb559(%1129: i8):  // 2 preds: ^bb557, ^bb558
    cf.br ^bb560
  ^bb560:  // pred: ^bb559
    %1130 = arith.cmpi slt, %c-128_i8, %c-128_i8 : i8
    cf.cond_br %1130, ^bb561, ^bb562
  ^bb561:  // pred: ^bb560
    cf.br ^bb563(%c-128_i8 : i8)
  ^bb562:  // pred: ^bb560
    cf.br ^bb563(%c-128_i8 : i8)
  ^bb563(%1131: i8):  // 2 preds: ^bb561, ^bb562
    cf.br ^bb564
  ^bb564:  // pred: ^bb563
    %1132 = arith.cmpi sgt, %c-128_i8, %c127_i8 : i8
    cf.cond_br %1132, ^bb565, ^bb566
  ^bb565:  // pred: ^bb564
    cf.br ^bb567(%c127_i8 : i8)
  ^bb566:  // pred: ^bb564
    cf.br ^bb567(%1131 : i8)
  ^bb567(%1133: i8):  // 2 preds: ^bb565, ^bb566
    cf.br ^bb568
  ^bb568:  // pred: ^bb567
    %1134 = arith.cmpi slt, %c-128_i8, %c-128_i8 : i8
    cf.cond_br %1134, ^bb569, ^bb570
  ^bb569:  // pred: ^bb568
    cf.br ^bb571(%c-128_i8 : i8)
  ^bb570:  // pred: ^bb568
    cf.br ^bb571(%c-128_i8 : i8)
  ^bb571(%1135: i8):  // 2 preds: ^bb569, ^bb570
    cf.br ^bb572
  ^bb572:  // pred: ^bb571
    %1136 = arith.cmpi sgt, %c-128_i8, %c127_i8 : i8
    cf.cond_br %1136, ^bb573, ^bb574
  ^bb573:  // pred: ^bb572
    cf.br ^bb575(%c127_i8 : i8)
  ^bb574:  // pred: ^bb572
    cf.br ^bb575(%1135 : i8)
  ^bb575(%1137: i8):  // 2 preds: ^bb573, ^bb574
    cf.br ^bb576
  ^bb576:  // pred: ^bb575
    %1138 = arith.cmpi slt, %c-128_i8, %c-128_i8 : i8
    cf.cond_br %1138, ^bb577, ^bb578
  ^bb577:  // pred: ^bb576
    cf.br ^bb579(%c-128_i8 : i8)
  ^bb578:  // pred: ^bb576
    cf.br ^bb579(%c-128_i8 : i8)
  ^bb579(%1139: i8):  // 2 preds: ^bb577, ^bb578
    cf.br ^bb580
  ^bb580:  // pred: ^bb579
    %1140 = arith.cmpi sgt, %c-128_i8, %c127_i8 : i8
    cf.cond_br %1140, ^bb581, ^bb582
  ^bb581:  // pred: ^bb580
    cf.br ^bb583(%c127_i8 : i8)
  ^bb582:  // pred: ^bb580
    cf.br ^bb583(%1139 : i8)
  ^bb583(%1141: i8):  // 2 preds: ^bb581, ^bb582
    cf.br ^bb584
  ^bb584:  // pred: ^bb583
    %1142 = arith.cmpi slt, %c-128_i8, %c-128_i8 : i8
    cf.cond_br %1142, ^bb585, ^bb586
  ^bb585:  // pred: ^bb584
    cf.br ^bb587(%c-128_i8 : i8)
  ^bb586:  // pred: ^bb584
    cf.br ^bb587(%c-128_i8 : i8)
  ^bb587(%1143: i8):  // 2 preds: ^bb585, ^bb586
    cf.br ^bb588
  ^bb588:  // pred: ^bb587
    %1144 = arith.cmpi sgt, %c-128_i8, %c127_i8 : i8
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

