module {
  func.func @main() {
    %true = arith.constant true
    %c941507673_i32 = arith.constant 941507673 : i32
    %false = arith.constant false
    %c1683202192_i32 = arith.constant 1683202192 : i32
    %c1126504254_i32 = arith.constant 1126504254 : i32
    %c1523482504_i32 = arith.constant 1523482504 : i32
    %cst = arith.constant 1.57152333E+9 : f32
    %cst_0 = arith.constant 0x4D8BF6A6 : f32
    %cst_1 = arith.constant 1.95751206E+9 : f32
    %cst_2 = arith.constant 1.71997427E+9 : f32
    %0 = tensor.empty() : tensor<4xf32>
    %1 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} outs(%0 : tensor<4xf32>) {
    ^bb0(%out: f32):
      %cst_24 = arith.constant 1.000000e+00 : f32
      linalg.yield %cst_24 : f32
    } -> tensor<4xf32>
    %2 = tensor.empty() : tensor<4xi1>
    %3 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} outs(%2 : tensor<4xi1>) {
    ^bb0(%out: i1):
      linalg.yield %true : i1
    } -> tensor<4xi1>
    %4 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} outs(%2 : tensor<4xi1>) {
    ^bb0(%out: i1):
      linalg.yield %true : i1
    } -> tensor<4xi1>
    %5 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} outs(%0 : tensor<4xf32>) {
    ^bb0(%out: f32):
      %cst_24 = arith.constant 1.000000e+00 : f32
      linalg.yield %cst_24 : f32
    } -> tensor<4xf32>
    %6 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} outs(%0 : tensor<4xf32>) {
    ^bb0(%out: f32):
      %cst_24 = arith.constant 1.000000e+00 : f32
      linalg.yield %cst_24 : f32
    } -> tensor<4xf32>
    %7 = tensor.empty() : tensor<4x4xi32>
    %8 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%7 : tensor<4x4xi32>) {
    ^bb0(%out: i32):
      %c1_i32_24 = arith.constant 1 : i32
      linalg.yield %c1_i32_24 : i32
    } -> tensor<4x4xi32>
    %9 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} outs(%0 : tensor<4xf32>) {
    ^bb0(%out: f32):
      %cst_24 = arith.constant 1.000000e+00 : f32
      linalg.yield %cst_24 : f32
    } -> tensor<4xf32>
    %10 = tensor.empty() : tensor<4x4xf32>
    %11 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%10 : tensor<4x4xf32>) {
    ^bb0(%out: f32):
      %cst_24 = arith.constant 1.000000e+00 : f32
      linalg.yield %cst_24 : f32
    } -> tensor<4x4xf32>
    %12 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%7 : tensor<4x4xi32>) {
    ^bb0(%out: i32):
      %c1_i32_24 = arith.constant 1 : i32
      linalg.yield %c1_i32_24 : i32
    } -> tensor<4x4xi32>
    %13 = tensor.empty() : tensor<4x4xi1>
    %14 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%13 : tensor<4x4xi1>) {
    ^bb0(%out: i1):
      linalg.yield %true : i1
    } -> tensor<4x4xi1>
    %15 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} outs(%0 : tensor<4xf32>) {
    ^bb0(%out: f32):
      %cst_24 = arith.constant 1.000000e+00 : f32
      linalg.yield %cst_24 : f32
    } -> tensor<4xf32>
    %16 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} outs(%0 : tensor<4xf32>) {
    ^bb0(%out: f32):
      %cst_24 = arith.constant 1.000000e+00 : f32
      linalg.yield %cst_24 : f32
    } -> tensor<4xf32>
    %17 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} outs(%2 : tensor<4xi1>) {
    ^bb0(%out: i1):
      linalg.yield %true : i1
    } -> tensor<4xi1>
    %18 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%7 : tensor<4x4xi32>) {
    ^bb0(%out: i32):
      %c1_i32_24 = arith.constant 1 : i32
      linalg.yield %c1_i32_24 : i32
    } -> tensor<4x4xi32>
    %19 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%7 : tensor<4x4xi32>) {
    ^bb0(%out: i32):
      %c1_i32_24 = arith.constant 1 : i32
      linalg.yield %c1_i32_24 : i32
    } -> tensor<4x4xi32>
    %20 = tensor.empty() : tensor<4xi32>
    %21 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} outs(%20 : tensor<4xi32>) {
    ^bb0(%out: i32):
      %c1_i32_24 = arith.constant 1 : i32
      linalg.yield %c1_i32_24 : i32
    } -> tensor<4xi32>
    %c0 = arith.constant 0 : index
    %c1 = arith.constant 1 : index
    %c2 = arith.constant 2 : index
    %c3 = arith.constant 3 : index
    %alloc = memref.alloc() : memref<4xi32>
    %c1_i32 = arith.constant 1 : i32
    affine.store %c1_i32, %alloc[%c0] : memref<4xi32>
    affine.store %c1_i32, %alloc[%c1] : memref<4xi32>
    affine.store %c1_i32, %alloc[%c2] : memref<4xi32>
    affine.store %c1_i32, %alloc[%c3] : memref<4xi32>
    %alloc_3 = memref.alloc() : memref<4xi1>
    affine.store %true, %alloc_3[%c0] : memref<4xi1>
    affine.store %true, %alloc_3[%c1] : memref<4xi1>
    affine.store %true, %alloc_3[%c2] : memref<4xi1>
    affine.store %true, %alloc_3[%c3] : memref<4xi1>
    %alloc_4 = memref.alloc() : memref<4xi32>
    affine.store %c1_i32, %alloc_4[%c0] : memref<4xi32>
    affine.store %c1_i32, %alloc_4[%c1] : memref<4xi32>
    affine.store %c1_i32, %alloc_4[%c2] : memref<4xi32>
    affine.store %c1_i32, %alloc_4[%c3] : memref<4xi32>
    %alloc_5 = memref.alloc() : memref<4xf32>
    %cst_6 = arith.constant 1.000000e+00 : f32
    affine.store %cst_6, %alloc_5[%c0] : memref<4xf32>
    affine.store %cst_6, %alloc_5[%c1] : memref<4xf32>
    affine.store %cst_6, %alloc_5[%c2] : memref<4xf32>
    affine.store %cst_6, %alloc_5[%c3] : memref<4xf32>
    %alloc_7 = memref.alloc() : memref<4xf32>
    affine.store %cst_6, %alloc_7[%c0] : memref<4xf32>
    affine.store %cst_6, %alloc_7[%c1] : memref<4xf32>
    affine.store %cst_6, %alloc_7[%c2] : memref<4xf32>
    affine.store %cst_6, %alloc_7[%c3] : memref<4xf32>
    %alloc_8 = memref.alloc() : memref<4xf32>
    affine.store %cst_6, %alloc_8[%c0] : memref<4xf32>
    affine.store %cst_6, %alloc_8[%c1] : memref<4xf32>
    affine.store %cst_6, %alloc_8[%c2] : memref<4xf32>
    affine.store %cst_6, %alloc_8[%c3] : memref<4xf32>
    %alloc_9 = memref.alloc() : memref<4xf32>
    affine.store %cst_6, %alloc_9[%c0] : memref<4xf32>
    affine.store %cst_6, %alloc_9[%c1] : memref<4xf32>
    affine.store %cst_6, %alloc_9[%c2] : memref<4xf32>
    affine.store %cst_6, %alloc_9[%c3] : memref<4xf32>
    %alloc_10 = memref.alloc() : memref<4x4xf32>
    affine.store %cst_6, %alloc_10[%c0, %c0] : memref<4x4xf32>
    affine.store %cst_6, %alloc_10[%c0, %c1] : memref<4x4xf32>
    affine.store %cst_6, %alloc_10[%c0, %c2] : memref<4x4xf32>
    affine.store %cst_6, %alloc_10[%c0, %c3] : memref<4x4xf32>
    affine.store %cst_6, %alloc_10[%c1, %c0] : memref<4x4xf32>
    affine.store %cst_6, %alloc_10[%c1, %c1] : memref<4x4xf32>
    affine.store %cst_6, %alloc_10[%c1, %c2] : memref<4x4xf32>
    affine.store %cst_6, %alloc_10[%c1, %c3] : memref<4x4xf32>
    affine.store %cst_6, %alloc_10[%c2, %c0] : memref<4x4xf32>
    affine.store %cst_6, %alloc_10[%c2, %c1] : memref<4x4xf32>
    affine.store %cst_6, %alloc_10[%c2, %c2] : memref<4x4xf32>
    affine.store %cst_6, %alloc_10[%c2, %c3] : memref<4x4xf32>
    affine.store %cst_6, %alloc_10[%c3, %c0] : memref<4x4xf32>
    affine.store %cst_6, %alloc_10[%c3, %c1] : memref<4x4xf32>
    affine.store %cst_6, %alloc_10[%c3, %c2] : memref<4x4xf32>
    affine.store %cst_6, %alloc_10[%c3, %c3] : memref<4x4xf32>
    %alloc_11 = memref.alloc() : memref<4x4xi1>
    affine.store %true, %alloc_11[%c0, %c0] : memref<4x4xi1>
    affine.store %true, %alloc_11[%c0, %c1] : memref<4x4xi1>
    affine.store %true, %alloc_11[%c0, %c2] : memref<4x4xi1>
    affine.store %true, %alloc_11[%c0, %c3] : memref<4x4xi1>
    affine.store %true, %alloc_11[%c1, %c0] : memref<4x4xi1>
    affine.store %true, %alloc_11[%c1, %c1] : memref<4x4xi1>
    affine.store %true, %alloc_11[%c1, %c2] : memref<4x4xi1>
    affine.store %true, %alloc_11[%c1, %c3] : memref<4x4xi1>
    affine.store %true, %alloc_11[%c2, %c0] : memref<4x4xi1>
    affine.store %true, %alloc_11[%c2, %c1] : memref<4x4xi1>
    affine.store %true, %alloc_11[%c2, %c2] : memref<4x4xi1>
    affine.store %true, %alloc_11[%c2, %c3] : memref<4x4xi1>
    affine.store %true, %alloc_11[%c3, %c0] : memref<4x4xi1>
    affine.store %true, %alloc_11[%c3, %c1] : memref<4x4xi1>
    affine.store %true, %alloc_11[%c3, %c2] : memref<4x4xi1>
    affine.store %true, %alloc_11[%c3, %c3] : memref<4x4xi1>
    %alloc_12 = memref.alloc() : memref<4xf32>
    affine.store %cst_6, %alloc_12[%c0] : memref<4xf32>
    affine.store %cst_6, %alloc_12[%c1] : memref<4xf32>
    affine.store %cst_6, %alloc_12[%c2] : memref<4xf32>
    affine.store %cst_6, %alloc_12[%c3] : memref<4xf32>
    %alloc_13 = memref.alloc() : memref<4xi1>
    affine.store %true, %alloc_13[%c0] : memref<4xi1>
    affine.store %true, %alloc_13[%c1] : memref<4xi1>
    affine.store %true, %alloc_13[%c2] : memref<4xi1>
    affine.store %true, %alloc_13[%c3] : memref<4xi1>
    %alloc_14 = memref.alloc() : memref<4xi1>
    affine.store %true, %alloc_14[%c0] : memref<4xi1>
    affine.store %true, %alloc_14[%c1] : memref<4xi1>
    affine.store %true, %alloc_14[%c2] : memref<4xi1>
    affine.store %true, %alloc_14[%c3] : memref<4xi1>
    %alloc_15 = memref.alloc() : memref<4xi32>
    affine.store %c1_i32, %alloc_15[%c0] : memref<4xi32>
    affine.store %c1_i32, %alloc_15[%c1] : memref<4xi32>
    affine.store %c1_i32, %alloc_15[%c2] : memref<4xi32>
    affine.store %c1_i32, %alloc_15[%c3] : memref<4xi32>
    %alloc_16 = memref.alloc() : memref<4x4xf32>
    affine.store %cst_6, %alloc_16[%c0, %c0] : memref<4x4xf32>
    affine.store %cst_6, %alloc_16[%c0, %c1] : memref<4x4xf32>
    affine.store %cst_6, %alloc_16[%c0, %c2] : memref<4x4xf32>
    affine.store %cst_6, %alloc_16[%c0, %c3] : memref<4x4xf32>
    affine.store %cst_6, %alloc_16[%c1, %c0] : memref<4x4xf32>
    affine.store %cst_6, %alloc_16[%c1, %c1] : memref<4x4xf32>
    affine.store %cst_6, %alloc_16[%c1, %c2] : memref<4x4xf32>
    affine.store %cst_6, %alloc_16[%c1, %c3] : memref<4x4xf32>
    affine.store %cst_6, %alloc_16[%c2, %c0] : memref<4x4xf32>
    affine.store %cst_6, %alloc_16[%c2, %c1] : memref<4x4xf32>
    affine.store %cst_6, %alloc_16[%c2, %c2] : memref<4x4xf32>
    affine.store %cst_6, %alloc_16[%c2, %c3] : memref<4x4xf32>
    affine.store %cst_6, %alloc_16[%c3, %c0] : memref<4x4xf32>
    affine.store %cst_6, %alloc_16[%c3, %c1] : memref<4x4xf32>
    affine.store %cst_6, %alloc_16[%c3, %c2] : memref<4x4xf32>
    affine.store %cst_6, %alloc_16[%c3, %c3] : memref<4x4xf32>
    %alloc_17 = memref.alloc() : memref<4xi1>
    affine.store %true, %alloc_17[%c0] : memref<4xi1>
    affine.store %true, %alloc_17[%c1] : memref<4xi1>
    affine.store %true, %alloc_17[%c2] : memref<4xi1>
    affine.store %true, %alloc_17[%c3] : memref<4xi1>
    %alloc_18 = memref.alloc() : memref<4xi32>
    affine.store %c1_i32, %alloc_18[%c0] : memref<4xi32>
    affine.store %c1_i32, %alloc_18[%c1] : memref<4xi32>
    affine.store %c1_i32, %alloc_18[%c2] : memref<4xi32>
    affine.store %c1_i32, %alloc_18[%c3] : memref<4xi32>
    %22 = arith.addi %true, %false : i1
    %23 = arith.mulf %cst_2, %cst_1 : f32
    %24 = arith.divsi %c1126504254_i32, %c1126504254_i32 : i32
    %25 = arith.minimumf %23, %cst_2 : f32
    %26 = arith.cmpf ult, %23, %25 : f32
    %27 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%alloc_4 : memref<4xi32>) outs(%19 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %out: i32):
      %683 = arith.xori %out, %out : i32
      %684 = arith.shrsi %in, %out : i32
      %685 = arith.minsi %684, %out : i32
      %686 = arith.ceildivui %in, %683 : i32
      %687 = arith.muli %686, %685 : i32
      %688 = arith.shli %in, %686 : i32
      %689 = arith.minsi %in, %out : i32
      %690 = arith.shli %687, %687 : i32
      %691 = arith.minui %688, %in : i32
      linalg.yield %691 : i32
    } -> tensor<4x4xi32>
    %28 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%12, %12 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    memref.store %cst_1, %alloc_12[%c1] : memref<4xf32>
    %29 = memref.load %alloc_17[%c2] : memref<4xi1>
    %30 = arith.cmpi ne, %true, %22 : i1
    memref.store %c1683202192_i32, %alloc_18[%c0] : memref<4xi32>
    %31 = arith.remui %29, %false : i1
    memref.store %cst, %alloc_7[%c2] : memref<4xf32>
    %32 = arith.remui %true, %29 : i1
    %33 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%15, %alloc_8 : tensor<4xf32>, memref<4xf32>) outs(%0 : tensor<4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4xf32>
    %34 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%12, %21 : tensor<4x4xi32>, tensor<4xi32>) outs(%8 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.divsi %out, %in : i32
      %c2076951318_i32 = arith.constant 2076951318 : i32
      %684 = arith.divui %in, %in_24 : i32
      %685 = arith.ceildivsi %out, %c2076951318_i32 : i32
      %686 = arith.shli %in_24, %685 : i32
      %687 = arith.remui %in, %685 : i32
      %688 = arith.divsi %684, %in_24 : i32
      %689 = arith.cmpi sge, %out, %687 : i32
      %690 = arith.remui %in, %c2076951318_i32 : i32
      %691 = arith.cmpi ule, %out, %686 : i32
      linalg.yield %in_24 : i32
    } -> tensor<4x4xi32>
    memref.store %true, %alloc_11[%c2, %c1] : memref<4x4xi1>
    %35 = memref.load %alloc_18[%c0] : memref<4xi32>
    %36 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%alloc_7, %alloc_7 : memref<4xf32>, memref<4xf32>) outs(%0 : tensor<4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4xf32>
    %37 = memref.load %alloc_12[%c3] : memref<4xf32>
    %38 = arith.maxui %29, %32 : i1
    %39 = linalg.matmul ins(%11, %11 : tensor<4x4xf32>, tensor<4x4xf32>) outs(%10 : tensor<4x4xf32>) -> tensor<4x4xf32>
    %40 = arith.remf %cst, %cst_0 : f32
    %41 = memref.load %alloc_4[%c2] : memref<4xi32>
    %42 = arith.remf %cst_0, %23 : f32
    memref.store %cst, %alloc_10[%c2, %c3] : memref<4x4xf32>
    %43 = linalg.matmul ins(%27, %12 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %44 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%8, %28 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %45 = linalg.matmul ins(%14, %14 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) -> tensor<4x4xi1>
    %46 = arith.minui %c1523482504_i32, %c1126504254_i32 : i32
    %47 = arith.remf %cst, %23 : f32
    memref.copy %alloc_9, %alloc_8 : memref<4xf32> to memref<4xf32>
    %48 = memref.load %alloc_12[%c3] : memref<4xf32>
    %49 = arith.maxsi %true, %true : i1
    %50 = linalg.matmul ins(%19, %8 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.copy %alloc_12, %alloc_8 : memref<4xf32> to memref<4xf32>
    %51 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%11, %39 : tensor<4x4xf32>, tensor<4x4xf32>) outs(%10 : tensor<4x4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4x4xf32>
    %52 = arith.minsi %c1523482504_i32, %c1126504254_i32 : i32
    %53 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%36 : tensor<4xf32>) outs(%39 : tensor<4x4xf32>) {
    ^bb0(%in: f32, %out: f32):
      %683 = arith.minimumf %in, %in : f32
      %684 = arith.mulf %out, %out : f32
      %685 = arith.mulf %683, %in : f32
      %686 = arith.negf %in : f32
      %687 = arith.minimumf %out, %in : f32
      %688 = arith.remf %686, %686 : f32
      %689 = arith.divf %688, %688 : f32
      %690 = arith.remf %687, %688 : f32
      %691 = arith.remf %685, %683 : f32
      %692 = arith.minimumf %690, %689 : f32
      %693 = arith.remf %in, %684 : f32
      linalg.yield %693 : f32
    } -> tensor<4x4xf32>
    %54 = arith.minimumf %47, %23 : f32
    %55 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%44, %18 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %56 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%alloc_5, %alloc_7 : memref<4xf32>, memref<4xf32>) outs(%0 : tensor<4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4xf32>
    %57 = arith.muli %38, %32 : i1
    memref.store %cst, %alloc_9[%c2] : memref<4xf32>
    memref.store %true, %alloc_14[%c3] : memref<4xi1>
    %58 = memref.load %alloc_12[%c1] : memref<4xf32>
    %59 = arith.mulf %54, %42 : f32
    memref.copy %alloc_12, %alloc_9 : memref<4xf32> to memref<4xf32>
    %60 = arith.maximumf %cst, %25 : f32
    %61 = linalg.matmul ins(%27, %8 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %alloc_19 = memref.alloc() : memref<4x4xi1>
    memref.copy %alloc_11, %alloc_19 : memref<4x4xi1> to memref<4x4xi1>
    %62 = linalg.matmul ins(%14, %14 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) -> tensor<4x4xi1>
    %63 = linalg.matmul ins(%14, %62 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) -> tensor<4x4xi1>
    memref.store %true, %alloc_13[%c3] : memref<4xi1>
    %64 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%alloc_10, %alloc_10 : memref<4x4xf32>, memref<4x4xf32>) outs(%10 : tensor<4x4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4x4xf32>
    %65 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%6, %56 : tensor<4xf32>, tensor<4xf32>) outs(%0 : tensor<4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4xf32>
    %66 = linalg.matmul ins(%50, %43 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %67 = arith.shrui %46, %c1683202192_i32 : i32
    %68 = memref.load %alloc_14[%c1] : memref<4xi1>
    %69 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%61 : tensor<4x4xi32>) {
    ^bb0(%out: i32):
      %683 = arith.ceildivui %out, %out : i32
      %684 = arith.andi %683, %683 : i32
      %685 = arith.xori %683, %684 : i32
      %686 = arith.minui %out, %685 : i32
      %687 = arith.minsi %683, %685 : i32
      %688 = arith.maxsi %686, %685 : i32
      %689 = arith.maxsi %687, %686 : i32
      %690 = arith.minsi %out, %686 : i32
      %691 = arith.shrui %687, %685 : i32
      %692 = arith.xori %685, %684 : i32
      %693 = arith.remsi %688, %686 : i32
      linalg.yield %693 : i32
    } -> tensor<4x4xi32>
    %70 = arith.maximumf %54, %58 : f32
    %71 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%12 : tensor<4x4xi32>) {
    ^bb0(%out: i32):
      %683 = arith.shrui %out, %out : i32
      %684 = arith.shli %683, %out : i32
      %685 = arith.maxui %out, %out : i32
      %686 = arith.maxui %685, %684 : i32
      %687 = arith.xori %685, %684 : i32
      %688 = arith.ceildivsi %687, %683 : i32
      %689 = arith.divui %686, %686 : i32
      %690 = arith.subi %685, %686 : i32
      linalg.yield %686 : i32
    } -> tensor<4x4xi32>
    %72 = arith.ori %24, %c1523482504_i32 : i32
    %73 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1, d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%44 : tensor<4x4xi32>) outs(%43 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %out: i32):
      %683 = arith.divui %out, %in : i32
      %684 = arith.maxsi %out, %in : i32
      %685 = arith.andi %684, %683 : i32
      %686 = arith.divsi %out, %out : i32
      %687 = arith.cmpi ugt, %685, %684 : i32
      %688 = arith.shrui %686, %683 : i32
      %689 = arith.ceildivsi %688, %688 : i32
      %690 = arith.floordivsi %in, %685 : i32
      %691 = arith.shrui %690, %in : i32
      %692 = arith.addi %in, %689 : i32
      linalg.yield %692 : i32
    } -> tensor<4x4xi32>
    %74 = arith.minsi %c1523482504_i32, %c941507673_i32 : i32
    %75 = linalg.matmul ins(%43, %27 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.copy %alloc_14, %alloc_3 : memref<4xi1> to memref<4xi1>
    %76 = arith.mulf %25, %cst_1 : f32
    %77 = arith.divsi %c1126504254_i32, %74 : i32
    %78 = arith.cmpi eq, %30, %true : i1
    %79 = arith.shrui %true, %true : i1
    %80 = arith.floordivsi %29, %79 : i1
    memref.store %46, %alloc[%c1] : memref<4xi32>
    memref.store %37, %alloc_10[%c1, %c2] : memref<4x4xf32>
    %81 = arith.divui %22, %true : i1
    %82 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%44, %12 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %83 = memref.load %alloc[%c1] : memref<4xi32>
    %84 = arith.mulf %70, %37 : f32
    %85 = linalg.matmul ins(%69, %44 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %86 = arith.minsi %c941507673_i32, %72 : i32
    %87 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%alloc, %alloc_18 : memref<4xi32>, memref<4xi32>) outs(%20 : tensor<4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4xi32>
    %88 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%19 : tensor<4x4xi32>) outs(%69 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %out: i32):
      %683 = arith.divui %in, %in : i32
      %684 = arith.andi %683, %out : i32
      %685 = arith.divui %false, %false : i1
      %686 = arith.remsi %false, %685 : i1
      %687 = arith.addi %out, %out : i32
      %688 = arith.divsi %684, %684 : i32
      %689 = arith.minui %false, %false : i1
      linalg.yield %687 : i32
    } -> tensor<4x4xi32>
    %89 = linalg.matmul ins(%45, %14 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) -> tensor<4x4xi1>
    %90 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%61 : tensor<4x4xi32>) {
    ^bb0(%out: i32):
      %683 = arith.cmpi sge, %out, %out : i32
      %684 = arith.maxsi %683, %683 : i1
      %c1795266629_i32 = arith.constant 1795266629 : i32
      %685 = arith.andi %684, %683 : i1
      %686 = arith.remsi %685, %683 : i1
      %687 = arith.cmpi ugt, %686, %684 : i1
      %688 = arith.shrsi %c1795266629_i32, %out : i32
      %689 = arith.minsi %683, %683 : i1
      %c846388670_i32 = arith.constant 846388670 : i32
      linalg.yield %c846388670_i32 : i32
    } -> tensor<4x4xi32>
    memref.copy %alloc_7, %alloc_5 : memref<4xf32> to memref<4xf32>
    %91 = linalg.matmul ins(%82, %75 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %92 = linalg.matmul ins(%8, %12 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.store %true, %alloc_19[%c3, %c1] : memref<4x4xi1>
    %93 = arith.shli %57, %31 : i1
    %94 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%15, %6, %alloc_10 : tensor<4xf32>, tensor<4xf32>, memref<4x4xf32>) outs(%64 : tensor<4x4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %in_25: f32, %out: f32):
      %683 = arith.divf %out, %out : f32
      %684 = arith.mulf %in, %in_24 : f32
      %685 = arith.remf %in_24, %in_25 : f32
      %686 = arith.remf %in, %in : f32
      %687 = arith.mulf %in_25, %out : f32
      %688 = arith.addf %in_24, %in : f32
      %689 = arith.negf %684 : f32
      %690 = arith.maximumf %685, %685 : f32
      %691 = arith.mulf %685, %683 : f32
      linalg.yield %691 : f32
    } -> tensor<4x4xf32>
    %95 = memref.load %alloc_14[%c0] : memref<4xi1>
    memref.copy %alloc_18, %alloc : memref<4xi32> to memref<4xi32>
    %96 = arith.divf %48, %cst_1 : f32
    %97 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%alloc_3, %alloc_17 : memref<4xi1>, memref<4xi1>) outs(%2 : tensor<4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %out: i1):
      %683 = arith.muli %in, %in_24 : i1
      linalg.yield %683 : i1
    } -> tensor<4xi1>
    %98 = linalg.matmul ins(%92, %8 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %99 = memref.load %alloc_5[%c3] : memref<4xf32>
    memref.store %60, %alloc_9[%c1] : memref<4xf32>
    memref.copy %alloc_8, %alloc_5 : memref<4xf32> to memref<4xf32>
    %100 = arith.divui %31, %78 : i1
    memref.copy %alloc_14, %alloc_3 : memref<4xi1> to memref<4xi1>
    %c92588919_i32 = arith.constant 92588919 : i32
    memref.copy %alloc_19, %alloc_11 : memref<4x4xi1> to memref<4x4xi1>
    %101 = linalg.matmul ins(%55, %8 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %102 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1, d0)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d1, d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%alloc_10, %alloc_8, %11 : memref<4x4xf32>, memref<4xf32>, tensor<4x4xf32>) outs(%11 : tensor<4x4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %in_25: f32, %out: f32):
      %683 = arith.remf %out, %in : f32
      %684 = arith.negf %683 : f32
      %685 = arith.maximumf %in_25, %684 : f32
      %686 = arith.minimumf %in_25, %in : f32
      %687 = arith.mulf %686, %684 : f32
      %688 = arith.divf %685, %in_24 : f32
      %689 = arith.addf %685, %685 : f32
      %690 = arith.maximumf %686, %684 : f32
      %691 = arith.mulf %690, %685 : f32
      %692 = arith.remf %687, %686 : f32
      linalg.yield %688 : f32
    } -> tensor<4x4xf32>
    %103 = arith.minimumf %96, %25 : f32
    %104 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%82 : tensor<4x4xi32>) {
    ^bb0(%out: i32):
      %683 = arith.shrsi %out, %out : i32
      %684 = arith.remui %683, %683 : i32
      %685 = arith.muli %684, %683 : i32
      %686 = arith.minui %out, %684 : i32
      %687 = arith.ceildivsi %686, %683 : i32
      %688 = arith.minsi %685, %out : i32
      %689 = arith.shrui %683, %683 : i32
      %690 = arith.maxsi %684, %685 : i32
      %691 = arith.minsi %687, %686 : i32
      %692 = arith.minui %684, %689 : i32
      %693 = arith.remui %689, %out : i32
      %694 = arith.addi %692, %693 : i32
      linalg.yield %688 : i32
    } -> tensor<4x4xi32>
    %105 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%alloc_18, %alloc_18, %87 : memref<4xi32>, memref<4xi32>, tensor<4xi32>) outs(%104 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %in_25: i32, %out: i32):
      %683 = arith.ceildivui %in_24, %in : i32
      %684 = arith.remui %in, %in_24 : i32
      %685 = arith.maxsi %out, %683 : i32
      %686 = arith.divui %684, %in : i32
      %687 = arith.shrui %686, %683 : i32
      %688 = arith.floordivsi %in_24, %in : i32
      %689 = arith.ceildivsi %688, %683 : i32
      %690 = arith.subi %out, %in_24 : i32
      linalg.yield %685 : i32
    } -> tensor<4x4xi32>
    %106 = arith.divui %c941507673_i32, %c1126504254_i32 : i32
    memref.store %c1683202192_i32, %alloc_4[%c1] : memref<4xi32>
    %107 = arith.xori %29, %true : i1
    %108 = arith.remui %41, %52 : i32
    %109 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%4, %97 : tensor<4xi1>, tensor<4xi1>) outs(%2 : tensor<4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %out: i1):
      %683 = arith.muli %in, %in_24 : i1
      linalg.yield %683 : i1
    } -> tensor<4xi1>
    %110 = arith.andi %80, %true : i1
    %111 = memref.load %alloc_7[%c0] : memref<4xf32>
    %112 = arith.maximumf %42, %48 : f32
    %113 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%alloc_14, %alloc_14 : memref<4xi1>, memref<4xi1>) outs(%2 : tensor<4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %out: i1):
      %683 = arith.muli %in, %in_24 : i1
      linalg.yield %683 : i1
    } -> tensor<4xi1>
    %114 = arith.muli %46, %83 : i32
    %115 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%45, %45 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %out: i1):
      %683 = arith.muli %in, %in_24 : i1
      linalg.yield %683 : i1
    } -> tensor<4x4xi1>
    %116 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%104, %73 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %117 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%71, %18 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    memref.store %23, %alloc_16[%c0, %c2] : memref<4x4xf32>
    %118 = memref.load %alloc_13[%c1] : memref<4xi1>
    %119 = linalg.matmul ins(%75, %19 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %120 = arith.shli %107, %32 : i1
    memref.copy %alloc_19, %alloc_11 : memref<4x4xi1> to memref<4x4xi1>
    %121 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%19, %44 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %122 = memref.load %alloc_18[%c3] : memref<4xi32>
    %123 = memref.load %alloc_7[%c1] : memref<4xf32>
    %124 = linalg.matmul ins(%18, %75 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %125 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%alloc_12, %16 : memref<4xf32>, tensor<4xf32>) outs(%0 : tensor<4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4xf32>
    memref.copy %alloc_17, %alloc_13 : memref<4xi1> to memref<4xi1>
    %126 = linalg.matmul ins(%101, %61 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %127 = arith.ori %120, %107 : i1
    %128 = arith.divui %false, %true : i1
    %129 = memref.load %alloc_7[%c3] : memref<4xf32>
    %130 = arith.minimumf %59, %60 : f32
    %131 = linalg.matmul ins(%105, %124 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %132 = linalg.matmul ins(%18, %85 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.copy %alloc_11, %alloc_19 : memref<4x4xi1> to memref<4x4xi1>
    %133 = linalg.matmul ins(%105, %19 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %134 = arith.addf %123, %48 : f32
    memref.store %129, %alloc_7[%c1] : memref<4xf32>
    %135 = arith.addi %83, %35 : i32
    %136 = arith.floordivsi %46, %86 : i32
    %137 = arith.addi %72, %74 : i32
    %138 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d1, d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%alloc_3, %alloc_3, %alloc_11 : memref<4xi1>, memref<4xi1>, memref<4x4xi1>) outs(%62 : tensor<4x4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %in_25: i1, %out: i1):
      %683 = arith.floordivsi %out, %in_25 : i1
      %684 = arith.subi %683, %in_25 : i1
      %685 = arith.divui %684, %in_25 : i1
      %686 = arith.minsi %out, %684 : i1
      %687 = arith.maxsi %in, %in_25 : i1
      %688 = arith.minui %out, %out : i1
      %689 = arith.maxui %683, %688 : i1
      %690 = arith.minui %683, %689 : i1
      %691 = arith.divsi %684, %687 : i1
      %692 = arith.floordivsi %689, %685 : i1
      linalg.yield %686 : i1
    } -> tensor<4x4xi1>
    %139 = arith.andi %true, %49 : i1
    %140 = memref.load %alloc[%c0] : memref<4xi32>
    %141 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%63, %138 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %out: i1):
      %683 = arith.muli %in, %in_24 : i1
      linalg.yield %683 : i1
    } -> tensor<4x4xi1>
    %142 = memref.load %alloc_10[%c1, %c3] : memref<4x4xf32>
    %143 = arith.muli %81, %120 : i1
    %144 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%116, %131 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %145 = memref.load %alloc_15[%c2] : memref<4xi32>
    %146 = linalg.matmul ins(%124, %91 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %147 = memref.load %alloc_14[%c3] : memref<4xi1>
    %148 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%126, %34 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %149 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%5, %33 : tensor<4xf32>, tensor<4xf32>) outs(%0 : tensor<4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4xf32>
    %150 = arith.xori %true, %127 : i1
    %151 = arith.muli %128, %93 : i1
    %152 = arith.maxsi %118, %29 : i1
    %153 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%87, %alloc_15, %69 : tensor<4xi32>, memref<4xi32>, tensor<4x4xi32>) outs(%144 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %in_25: i32, %out: i32):
      %683 = arith.addi %in, %out : i32
      %684 = arith.remui %683, %out : i32
      %685 = arith.shli %in_25, %684 : i32
      %686 = arith.divsi %out, %684 : i32
      %687 = arith.andi %683, %in : i32
      %688 = arith.shrsi %686, %685 : i32
      %689 = arith.ceildivui %684, %in : i32
      %690 = arith.shrui %in_25, %in : i32
      linalg.yield %685 : i32
    } -> tensor<4x4xi32>
    %154 = arith.minimumf %cst_0, %103 : f32
    memref.store %cst_2, %alloc_10[%c1, %c1] : memref<4x4xf32>
    %155 = arith.addi %true, %49 : i1
    %156 = linalg.matmul ins(%89, %14 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) -> tensor<4x4xi1>
    %157 = arith.mulf %48, %76 : f32
    %158 = arith.divsi %30, %139 : i1
    %159 = arith.maxui %80, %true : i1
    %160 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%alloc_7, %149 : memref<4xf32>, tensor<4xf32>) outs(%0 : tensor<4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4xf32>
    memref.store %154, %alloc_10[%c1, %c0] : memref<4x4xf32>
    memref.store %60, %alloc_5[%c1] : memref<4xf32>
    %161 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%109 : tensor<4xi1>) outs(%138 : tensor<4x4xi1>) {
    ^bb0(%in: i1, %out: i1):
      %683 = arith.xori %out, %out : i1
      %684 = arith.ceildivui %683, %in : i1
      %685 = arith.cmpi ugt, %683, %684 : i1
      %686 = arith.maxsi %685, %in : i1
      %687 = arith.shrsi %out, %685 : i1
      %688 = arith.shrui %683, %true : i1
      %689 = arith.ceildivsi %true, %687 : i1
      %690 = arith.addi %684, %in : i1
      %691 = arith.addi %688, %687 : i1
      linalg.yield %688 : i1
    } -> tensor<4x4xi1>
    %162 = arith.remf %59, %37 : f32
    memref.copy %alloc_8, %alloc_9 : memref<4xf32> to memref<4xf32>
    %163 = linalg.matmul ins(%51, %39 : tensor<4x4xf32>, tensor<4x4xf32>) outs(%10 : tensor<4x4xf32>) -> tensor<4x4xf32>
    %164 = memref.load %alloc_8[%c0] : memref<4xf32>
    %cst_20 = arith.constant 1.7573719E+9 : f32
    %165 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%69 : tensor<4x4xi32>) {
    ^bb0(%out: i32):
      %683 = arith.maxui %out, %out : i32
      %684 = arith.maxsi %683, %out : i32
      %685 = arith.minsi %684, %684 : i32
      %686 = arith.floordivsi %684, %out : i32
      %687 = arith.shrsi %out, %686 : i32
      %688 = arith.remsi %687, %685 : i32
      %689 = arith.floordivsi %683, %687 : i32
      %690 = arith.andi %683, %687 : i32
      %691 = arith.maxui %687, %687 : i32
      %692 = arith.maxsi %688, %689 : i32
      %693 = arith.andi %690, %687 : i32
      linalg.yield %692 : i32
    } -> tensor<4x4xi32>
    memref.store %123, %alloc_12[%c3] : memref<4xf32>
    %166 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%73, %82 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %167 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%alloc_15, %alloc_4 : memref<4xi32>, memref<4xi32>) outs(%20 : tensor<4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4xi32>
    memref.store %129, %alloc_12[%c3] : memref<4xf32>
    %168 = arith.shli %143, %127 : i1
    memref.store %c1126504254_i32, %alloc_15[%c1] : memref<4xi32>
    %169 = memref.load %alloc_10[%c2, %c2] : memref<4x4xf32>
    %170 = arith.muli %30, %false : i1
    %171 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%16, %1 : tensor<4xf32>, tensor<4xf32>) outs(%94 : tensor<4x4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.maximumf %out, %in : f32
      %684 = arith.mulf %out, %in : f32
      %685 = arith.maximumf %in_24, %in_24 : f32
      %686 = arith.divf %685, %685 : f32
      %687 = arith.addf %out, %683 : f32
      %cst_25 = arith.constant 1.05646566E+9 : f32
      linalg.yield %685 : f32
    } -> tensor<4x4xf32>
    %172 = linalg.matmul ins(%14, %89 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) -> tensor<4x4xi1>
    %173 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%3, %3, %97 : tensor<4xi1>, tensor<4xi1>, tensor<4xi1>) outs(%141 : tensor<4x4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %in_25: i1, %out: i1):
      %683 = arith.shrui %in_24, %in_25 : i1
      %684 = arith.divui %in, %in_25 : i1
      %685 = arith.ceildivsi %683, %in_24 : i1
      %686 = arith.minui %in_24, %in_25 : i1
      %687 = arith.shli %685, %in_25 : i1
      %688 = arith.remsi %in_24, %686 : i1
      %689 = arith.maxui %in, %688 : i1
      %690 = arith.maxsi %687, %out : i1
      %691 = arith.remui %in_24, %683 : i1
      %692 = arith.muli %690, %688 : i1
      %693 = arith.divui %683, %in : i1
      linalg.yield %693 : i1
    } -> tensor<4x4xi1>
    %174 = memref.load %alloc_11[%c1, %c3] : memref<4x4xi1>
    %175 = arith.remsi %108, %41 : i32
    memref.store %25, %alloc_10[%c1, %c0] : memref<4x4xf32>
    memref.store %151, %alloc_3[%c0] : memref<4xi1>
    %176 = arith.divui %false, %78 : i1
    %177 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%19, %28 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    memref.store %84, %alloc_9[%c3] : memref<4xf32>
    %178 = memref.load %alloc_13[%c0] : memref<4xi1>
    memref.copy %alloc_8, %alloc_5 : memref<4xf32> to memref<4xf32>
    %179 = arith.minsi %81, %false : i1
    %180 = arith.subi %170, %110 : i1
    memref.store %129, %alloc_9[%c2] : memref<4xf32>
    %181 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%63, %89 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %out: i1):
      %683 = arith.muli %in, %in_24 : i1
      linalg.yield %683 : i1
    } -> tensor<4x4xi1>
    %182 = linalg.matmul ins(%43, %88 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %183 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%69, %177 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %184 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%alloc_15, %21 : memref<4xi32>, tensor<4xi32>) outs(%20 : tensor<4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4xi32>
    %185 = memref.load %alloc_8[%c0] : memref<4xf32>
    %186 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%alloc_4 : memref<4xi32>) outs(%146 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %out: i32):
      %683 = arith.shrsi %out, %in : i32
      %684 = arith.maxui %683, %in : i32
      %685 = arith.ceildivui %out, %out : i32
      %686 = arith.minsi %out, %in : i32
      %687 = arith.muli %684, %686 : i32
      %688 = arith.cmpi eq, %687, %685 : i32
      %689 = arith.xori %688, %688 : i1
      %690 = arith.muli %false, %688 : i1
      %691 = arith.maxsi %false, %689 : i1
      linalg.yield %686 : i32
    } -> tensor<4x4xi32>
    memref.copy %alloc_16, %alloc_10 : memref<4x4xf32> to memref<4x4xf32>
    %187 = linalg.matmul ins(%61, %165 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %188 = memref.load %alloc_10[%c0, %c0] : memref<4x4xf32>
    %189 = arith.remf %123, %42 : f32
    memref.copy %alloc_17, %alloc_3 : memref<4xi1> to memref<4xi1>
    %190 = memref.load %alloc_12[%c2] : memref<4xf32>
    %191 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%161, %156 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %out: i1):
      %683 = arith.muli %in, %in_24 : i1
      linalg.yield %683 : i1
    } -> tensor<4x4xi1>
    %192 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%alloc_13, %4 : memref<4xi1>, tensor<4xi1>) outs(%2 : tensor<4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %out: i1):
      %683 = arith.muli %in, %in_24 : i1
      linalg.yield %683 : i1
    } -> tensor<4xi1>
    memref.store %54, %alloc_9[%c1] : memref<4xf32>
    %193 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%12, %19 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    memref.copy %alloc_9, %alloc_5 : memref<4xf32> to memref<4xf32>
    %194 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%171 : tensor<4x4xf32>) {
    ^bb0(%out: f32):
      %683 = arith.divf %out, %out : f32
      %684 = arith.addf %683, %out : f32
      %685 = arith.mulf %683, %out : f32
      %686 = arith.remf %684, %685 : f32
      %687 = arith.maximumf %out, %685 : f32
      %688 = arith.divf %683, %686 : f32
      %689 = arith.minimumf %687, %684 : f32
      %690 = arith.addf %686, %684 : f32
      %691 = arith.negf %685 : f32
      linalg.yield %691 : f32
    } -> tensor<4x4xf32>
    memref.store %49, %alloc_14[%c1] : memref<4xi1>
    %195 = arith.remf %99, %cst_1 : f32
    %196 = memref.load %alloc_17[%c2] : memref<4xi1>
    %197 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%117 : tensor<4x4xi32>) {
    ^bb0(%out: i32):
      %683 = arith.ceildivui %out, %out : i32
      %684 = arith.cmpi sge, %out, %out : i32
      %685 = arith.remui %684, %684 : i1
      %686 = arith.ceildivsi %685, %685 : i1
      %c1066375642_i32 = arith.constant 1066375642 : i32
      %687 = arith.minsi %685, %684 : i1
      %688 = arith.divsi %684, %685 : i1
      %689 = arith.remui %684, %685 : i1
      %690 = arith.andi %687, %685 : i1
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %198 = arith.minui %122, %35 : i32
    %199 = arith.maximumf %cst_2, %188 : f32
    %200 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%alloc_4, %alloc, %alloc_4 : memref<4xi32>, memref<4xi32>, memref<4xi32>) outs(%92 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %in_25: i32, %out: i32):
      %683 = arith.subi %in_24, %in_24 : i32
      %684 = arith.ceildivui %out, %out : i32
      %685 = arith.ceildivui %in_25, %683 : i32
      %686 = arith.remsi %in, %685 : i32
      %687 = arith.remui %in_25, %685 : i32
      %688 = arith.floordivsi %out, %686 : i32
      %689 = arith.ceildivui %683, %687 : i32
      %690 = arith.maxsi %684, %684 : i32
      %691 = arith.divui %690, %688 : i32
      linalg.yield %out : i32
    } -> tensor<4x4xi32>
    %201 = arith.shrui %false, %95 : i1
    %202 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%alloc_16, %39 : memref<4x4xf32>, tensor<4x4xf32>) outs(%10 : tensor<4x4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4x4xf32>
    %203 = arith.remui %26, %159 : i1
    %204 = linalg.matmul ins(%148, %146 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %205 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%39 : tensor<4x4xf32>) {
    ^bb0(%out: f32):
      %683 = arith.negf %out : f32
      %684 = arith.divf %683, %out : f32
      %685 = arith.remf %out, %683 : f32
      %686 = arith.addf %out, %out : f32
      %687 = arith.mulf %685, %684 : f32
      %688 = arith.mulf %685, %687 : f32
      %689 = arith.mulf %out, %688 : f32
      %690 = arith.remf %out, %out : f32
      %691 = arith.remf %685, %690 : f32
      %692 = arith.remf %688, %686 : f32
      linalg.yield %691 : f32
    } -> tensor<4x4xf32>
    %206 = linalg.matmul ins(%53, %39 : tensor<4x4xf32>, tensor<4x4xf32>) outs(%10 : tensor<4x4xf32>) -> tensor<4x4xf32>
    %207 = linalg.matmul ins(%92, %144 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %208 = memref.load %alloc_16[%c2, %c2] : memref<4x4xf32>
    memref.store %198, %alloc_4[%c0] : memref<4xi32>
    memref.store %157, %alloc_7[%c3] : memref<4xf32>
    %209 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%132 : tensor<4x4xi32>) outs(%69 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %out: i32):
      %683 = arith.divui %in, %in : i32
      %684 = arith.muli %683, %out : i32
      %685 = arith.ceildivsi %683, %in : i32
      %686 = arith.remui %683, %685 : i32
      %687 = arith.cmpi eq, %out, %out : i32
      %688 = arith.addi %684, %683 : i32
      %689 = arith.xori %out, %688 : i32
      %690 = arith.cmpi ne, %684, %685 : i32
      %691 = arith.shrsi %690, %687 : i1
      linalg.yield %686 : i32
    } -> tensor<4x4xi32>
    %210 = arith.xori %true, %78 : i1
    %211 = memref.load %alloc_8[%c3] : memref<4xf32>
    memref.store %true, %alloc_14[%c1] : memref<4xi1>
    %212 = arith.minui %180, %93 : i1
    memref.copy %alloc_9, %alloc_5 : memref<4xf32> to memref<4xf32>
    %213 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%119 : tensor<4x4xi32>) {
    ^bb0(%out: i32):
      %683 = arith.divui %out, %out : i32
      %684 = arith.maxsi %683, %683 : i32
      %c1310578280_i32 = arith.constant 1310578280 : i32
      %685 = arith.xori %683, %683 : i32
      %686 = arith.shrsi %683, %685 : i32
      %687 = arith.subi %684, %683 : i32
      %688 = arith.remsi %685, %c1310578280_i32 : i32
      %689 = arith.muli %685, %688 : i32
      %690 = arith.xori %687, %683 : i32
      %691 = arith.andi %687, %684 : i32
      %692 = arith.remui %c1310578280_i32, %690 : i32
      linalg.yield %out : i32
    } -> tensor<4x4xi32>
    %214 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%184, %167 : tensor<4xi32>, tensor<4xi32>) outs(%213 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.divsi %out, %in_24 : i32
      %684 = arith.minsi %683, %683 : i32
      %685 = arith.remui %out, %in : i32
      %686 = arith.floordivsi %684, %683 : i32
      %687 = arith.maxui %out, %684 : i32
      %688 = arith.divui %683, %in_24 : i32
      %689 = arith.subi %683, %686 : i32
      linalg.yield %687 : i32
    } -> tensor<4x4xi32>
    %215 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%17, %109 : tensor<4xi1>, tensor<4xi1>) outs(%2 : tensor<4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %out: i1):
      %683 = arith.muli %in, %in_24 : i1
      linalg.yield %683 : i1
    } -> tensor<4xi1>
    %216 = arith.remf %199, %25 : f32
    %217 = arith.ori %77, %137 : i32
    %218 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%197 : tensor<4x4xi32>) outs(%186 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %out: i32):
      %683 = arith.maxui %out, %in : i32
      %684 = arith.minsi %683, %683 : i32
      %685 = arith.floordivsi %in, %683 : i32
      %686 = arith.shli %683, %685 : i32
      %687 = arith.subi %out, %in : i32
      %688 = arith.maxsi %683, %684 : i32
      %689 = arith.cmpi uge, %in, %688 : i32
      %690 = arith.muli %689, %689 : i1
      %691 = arith.maxsi %out, %686 : i32
      %692 = arith.subi %687, %691 : i32
      linalg.yield %692 : i32
    } -> tensor<4x4xi32>
    %219 = linalg.matmul ins(%90, %177 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %220 = memref.load %alloc_5[%c3] : memref<4xf32>
    memref.store %152, %alloc_11[%c1, %c3] : memref<4x4xi1>
    %221 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%214, %187 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %222 = memref.load %alloc_4[%c2] : memref<4xi32>
    %223 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%177, %66 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %224 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%alloc_14, %alloc_13 : memref<4xi1>, memref<4xi1>) outs(%2 : tensor<4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %out: i1):
      %683 = arith.muli %in, %in_24 : i1
      linalg.yield %683 : i1
    } -> tensor<4xi1>
    %225 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%200 : tensor<4x4xi32>) {
    ^bb0(%out: i32):
      %683 = arith.muli %out, %out : i32
      %c1718975672_i32 = arith.constant 1718975672 : i32
      %684 = arith.shli %c1718975672_i32, %c1718975672_i32 : i32
      %685 = arith.shrsi %out, %684 : i32
      %686 = arith.addi %out, %684 : i32
      %687 = arith.shrui %c1718975672_i32, %685 : i32
      %688 = arith.addi %684, %687 : i32
      %689 = arith.divsi %c1718975672_i32, %683 : i32
      %690 = arith.ceildivui %689, %686 : i32
      linalg.yield %690 : i32
    } -> tensor<4x4xi32>
    %226 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%3, %192 : tensor<4xi1>, tensor<4xi1>) outs(%2 : tensor<4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %out: i1):
      %683 = arith.muli %in, %in_24 : i1
      linalg.yield %683 : i1
    } -> tensor<4xi1>
    %227 = arith.remf %54, %40 : f32
    memref.copy %alloc_18, %alloc : memref<4xi32> to memref<4xi32>
    %228 = memref.load %alloc_3[%c0] : memref<4xi1>
    memref.copy %alloc_14, %alloc_17 : memref<4xi1> to memref<4xi1>
    %229 = memref.load %alloc_4[%c0] : memref<4xi32>
    memref.copy %alloc_13, %alloc_3 : memref<4xi1> to memref<4xi1>
    %230 = memref.load %alloc_17[%c1] : memref<4xi1>
    %231 = arith.shrsi %false, %210 : i1
    memref.store %189, %alloc_8[%c1] : memref<4xf32>
    %232 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%205, %205 : tensor<4x4xf32>, tensor<4x4xf32>) outs(%10 : tensor<4x4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4x4xf32>
    memref.copy %alloc_13, %alloc_14 : memref<4xi1> to memref<4xi1>
    %233 = arith.xori %86, %72 : i32
    memref.copy %alloc_10, %alloc_16 : memref<4x4xf32> to memref<4x4xf32>
    %234 = linalg.matmul ins(%105, %98 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %235 = arith.negf %162 : f32
    %236 = memref.load %alloc_10[%c0, %c0] : memref<4x4xf32>
    %237 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d1, d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%alloc_4, %21, %92 : memref<4xi32>, tensor<4xi32>, tensor<4x4xi32>) outs(%85 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %in_25: i32, %out: i32):
      %683 = arith.maxui %out, %in : i32
      %684 = arith.floordivsi %in, %683 : i32
      %685 = arith.minui %in_24, %in_25 : i32
      %686 = arith.ceildivsi %684, %684 : i32
      %687 = arith.addi %in_25, %in_24 : i32
      %688 = arith.subi %in_25, %684 : i32
      %689 = arith.minsi %in, %688 : i32
      %690 = arith.subi %685, %687 : i32
      %691 = arith.maxsi %689, %688 : i32
      linalg.yield %691 : i32
    } -> tensor<4x4xi32>
    %238 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%alloc_18, %21 : memref<4xi32>, tensor<4xi32>) outs(%20 : tensor<4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4xi32>
    %239 = arith.shli %137, %86 : i32
    %240 = arith.maxsi %c1683202192_i32, %140 : i32
    %241 = arith.shrsi %120, %80 : i1
    memref.store %201, %alloc_19[%c0, %c3] : memref<4x4xi1>
    %242 = linalg.matmul ins(%8, %153 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.store %159, %alloc_19[%c1, %c0] : memref<4x4xi1>
    %243 = arith.remui %77, %136 : i32
    %244 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%5, %9, %232 : tensor<4xf32>, tensor<4xf32>, tensor<4x4xf32>) outs(%94 : tensor<4x4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %in_25: f32, %out: f32):
      %683 = arith.addf %out, %in_24 : f32
      %684 = arith.negf %in_24 : f32
      %685 = arith.remf %684, %683 : f32
      %686 = arith.negf %684 : f32
      %687 = arith.mulf %686, %in : f32
      linalg.yield %687 : f32
    } -> tensor<4x4xf32>
    %245 = memref.load %alloc_8[%c3] : memref<4xf32>
    %246 = arith.shrui %78, %true : i1
    %247 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%113, %192 : tensor<4xi1>, tensor<4xi1>) outs(%2 : tensor<4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %out: i1):
      %683 = arith.muli %in, %in_24 : i1
      linalg.yield %683 : i1
    } -> tensor<4xi1>
    %248 = memref.load %alloc_14[%c2] : memref<4xi1>
    %249 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%244 : tensor<4x4xf32>) {
    ^bb0(%out: f32):
      %683 = arith.maximumf %out, %out : f32
      %684 =arith.maximumf %683, %683 : f32
      %685 = arith.remf %683, %684 : f32
      %686 = arith.minimumf %685, %685 : f32
      %687 = arith.divf %685, %686 : f32
      %688 = arith.divf %687, %out : f32
      %689 = arith.minimumf %683, %686 : f32
      %690 = arith.remf %out, %688 : f32
      %691 = arith.maximumf %684, %688 : f32
      %692 = arith.maximumf %689, %684 : f32
      %693 = arith.remf %685, %686 : f32
      linalg.yield %691 : f32
    } -> tensor<4x4xf32>
    memref.copy %alloc_13, %alloc_17 : memref<4xi1> to memref<4xi1>
    memref.store %158, %alloc_3[%c3] : memref<4xi1>
    %250 = memref.load %alloc_13[%c1] : memref<4xi1>
    %251 = linalg.matmul ins(%28, %92 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %252 = linalg.matmul ins(%177, %133 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %253 = linalg.matmul ins(%117, %18 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.store %74, %alloc_15[%c3] : memref<4xi32>
    memref.copy %alloc_15, %alloc_18 : memref<4xi32> to memref<4xi32>
    %254 = arith.divf %216, %162 : f32
    %255 = memref.load %alloc_16[%c2, %c2] : memref<4x4xf32>
    %256 = arith.shli %210, %true : i1
    %257 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%249, %163 : tensor<4x4xf32>, tensor<4x4xf32>) outs(%10 : tensor<4x4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4x4xf32>
    %258 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%125, %15 : tensor<4xf32>, tensor<4xf32>) outs(%0 : tensor<4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4xf32>
    %259 = linalg.matmul ins(%19, %200 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %260 = arith.shli %239, %86 : i32
    %261 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%187, %55 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %262 = linalg.matmul ins(%225, %104 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %263 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%alloc_8, %6 : memref<4xf32>, tensor<4xf32>) outs(%0 : tensor<4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4xf32>
    %264 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%alloc_18, %alloc_4 : memref<4xi32>, memref<4xi32>) outs(%20 : tensor<4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4xi32>
    %265 = arith.addi %95, %true : i1
    %266 = linalg.matmul ins(%53, %205 : tensor<4x4xf32>, tensor<4x4xf32>) outs(%10 : tensor<4x4xf32>) -> tensor<4x4xf32>
    %267 = memref.load %alloc_18[%c2] : memref<4xi32>
    %268 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1, d0)>, affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%92, %21 : tensor<4x4xi32>, tensor<4xi32>) outs(%225 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.shli %out, %in_24 : i32
      %684 = arith.maxui %683, %in_24 : i32
      %685 = arith.ceildivui %out, %684 : i32
      %686 = arith.maxui %in, %out : i32
      %687 = arith.cmpi slt, %in, %684 : i32
      %688 = arith.maxui %683, %685 : i32
      %689 = arith.minui %out, %688 : i32
      %690 = arith.maxui %in, %684 : i32
      %691 = arith.shli %689, %683 : i32
      linalg.yield %691 : i32
    } -> tensor<4x4xi32>
    memref.copy %alloc_13, %alloc_17 : memref<4xi1> to memref<4xi1>
    %269 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%alloc, %21 : memref<4xi32>, tensor<4xi32>) outs(%193 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.maxui %out, %in : i32
      %684 = arith.divui %683, %out : i32
      %685 = arith.xori %684, %in : i32
      %686 = arith.minsi %684, %out : i32
      %687 = arith.remsi %683, %in : i32
      %688 = arith.andi %687, %683 : i32
      %689 = arith.muli %683, %684 : i32
      linalg.yield %685 : i32
    } -> tensor<4x4xi32>
    %270 = arith.remf %59, %185 : f32
    memref.copy %alloc_12, %alloc_7 : memref<4xf32> to memref<4xf32>
    %271 = memref.load %alloc_18[%c3] : memref<4xi32>
    %272 = arith.addf %190, %60 : f32
    %273 = arith.minimumf %199, %70 : f32
    %274 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%alloc : memref<4xi32>) outs(%98 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %out: i32):
      %683 = arith.subi %out, %in : i32
      %684 = arith.remsi %in, %in : i32
      %685 = arith.cmpi ult, %683, %out : i32
      %686 = arith.ceildivsi %out, %684 : i32
      %687 = arith.remsi %686, %out : i32
      %688 = arith.cmpi uge, %out, %686 : i32
      %689 = arith.minui %in, %686 : i32
      %690 = arith.cmpi uge, %683, %in : i32
      %691 = arith.maxui %688, %685 : i1
      linalg.yield %684 : i32
    } -> tensor<4x4xi32>
    %275 = arith.ori %93, %true : i1
    memref.store %188, %alloc_10[%c3, %c3] : memref<4x4xf32>
    %276 = arith.minsi %203, %212 : i1
    %277 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%264 : tensor<4xi32>) outs(%177 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %out: i32):
      %683 = arith.minui %out, %in : i32
      %684 = arith.shrui %683, %in : i32
      %685 = arith.maxsi %out, %in : i32
      %686 = arith.andi %683, %683 : i32
      %687 = arith.muli %out, %684 : i32
      %688 = arith.ceildivsi %686, %685 : i32
      %689 = arith.shrui %688, %685 : i32
      %690 = arith.shrsi %687, %688 : i32
      %691 = arith.floordivsi %686, %in : i32
      %692 = arith.muli %691, %690 : i32
      linalg.yield %692 : i32
    } -> tensor<4x4xi32>
    %278 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%15, %16 : tensor<4xf32>, tensor<4xf32>) outs(%0 : tensor<4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4xf32>
    %279 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%121 : tensor<4x4xi32>) {
    ^bb0(%out: i32):
      %683 = arith.remsi %out, %out : i32
      %684 = arith.floordivsi %683, %683 : i32
      %685 = arith.remsi %683, %683 : i32
      %686 = arith.shrsi %683, %out : i32
      %687 = arith.minsi %685, %683 : i32
      %688 = arith.ceildivui %686, %out : i32
      %689 = arith.andi %688, %684 : i32
      %c1919076778_i32 = arith.constant 1919076778 : i32
      %690 = arith.floordivsi %683, %685 : i32
      linalg.yield %c1919076778_i32 : i32
    } -> tensor<4x4xi32>
    %280 = linalg.matmul ins(%237, %28 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %281 = linalg.matmul ins(%153, %126 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %282 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%alloc_15, %264 : memref<4xi32>, tensor<4xi32>) outs(%207 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.shli %out, %out : i32
      %684 = arith.xori %in_24, %out : i32
      %685 = arith.andi %683, %out : i32
      %686 = arith.addi %685, %out : i32
      %687 = arith.ceildivui %684, %in_24 : i32
      %688 = arith.divsi %out, %in : i32
      %689 = arith.cmpi eq, %out, %in : i32
      %690 = arith.subi %686, %686 : i32
      %691 = arith.xori %683, %683 : i32
      %692 = arith.divui %685, %out : i32
      %693 = arith.remui %690, %686 : i32
      %694 = arith.ceildivsi %689, %689 : i1
      linalg.yield %693 : i32
    } -> tensor<4x4xi32>
    %283 = memref.load %alloc_8[%c1] : memref<4xf32>
    memref.copy %alloc_10, %alloc_16 : memref<4x4xf32> to memref<4x4xf32>
    %284 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%16, %258 : tensor<4xf32>, tensor<4xf32>) outs(%0 : tensor<4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4xf32>
    %285 = linalg.matmul ins(%115, %45 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) -> tensor<4x4xi1>
    %286 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%149, %16 : tensor<4xf32>, tensor<4xf32>) outs(%0 : tensor<4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4xf32>
    memref.store %178, %alloc_17[%c2] : memref<4xi1>
    %287 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%50, %144 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%182 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.cmpi sge, %out, %in_24 : i32
      %684 = arith.divsi %683, %683 : i1
      %685 = arith.subi %in_24, %out : i32
      %686 = arith.subi %in_24, %in : i32
      %687 = arith.andi %685, %out : i32
      %688 = arith.xori %687, %in : i32
      %689 = arith.maxui %683, %683 : i1
      %690 = arith.maxsi %in_24, %688 : i32
      linalg.yield %690 : i32
    } -> tensor<4x4xi32>
    memref.store %231, %alloc_13[%c0] : memref<4xi1>
    memref.store %129, %alloc_16[%c1, %c0] : memref<4x4xf32>
    memref.copy %alloc_4, %alloc : memref<4xi32> to memref<4xi32>
    %288 = arith.cmpi ugt, %false, %true : i1
    %cst_21 = arith.constant 0x4DCF2FF2 : f32
    %289 = arith.maxsi %239, %140 : i32
    memref.copy %alloc_5, %alloc_7 : memref<4xf32> to memref<4xf32>
    %290 = memref.load %alloc_7[%c3] : memref<4xf32>
    %291 = arith.minimumf %129, %cst_1 : f32
    memref.store %cst_2, %alloc_10[%c0, %c2] : memref<4x4xf32>
    %292 = arith.remui %231, %176 : i1
    %293 = memref.load %alloc_15[%c1] : memref<4xi32>
    memref.copy %alloc_8, %alloc_7 : memref<4xf32> to memref<4xf32>
    %294 = arith.cmpf false, %236, %48 : f32
    memref.store %142, %alloc_12[%c0] : memref<4xf32>
    %295 = arith.maxui %false, %147 : i1
    %296 = memref.load %alloc_14[%c0] : memref<4xi1>
    %297 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%19, %148 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %298 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%181 : tensor<4x4xi1>) {
    ^bb0(%out: i1):
      %683 = arith.minsi %out, %out : i1
      %c1887156750_i32 = arith.constant 1887156750 : i32
      %c974020018_i32 = arith.constant 974020018 : i32
      %684 = arith.maxui %683, %683 : i1
      %685 = arith.ceildivsi %c974020018_i32, %c974020018_i32 : i32
      %686 = arith.divsi %c974020018_i32, %c974020018_i32 : i32
      %687 = arith.shrui %685, %c1887156750_i32 : i32
      %688 = arith.minui %c1887156750_i32, %687 : i32
      linalg.yield %683 : i1
    } -> tensor<4x4xi1>
    memref.store %130, %alloc_10[%c3, %c1] : memref<4x4xf32>
    %299 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%19, %166 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %300 = arith.muli %79, %246 : i1
    %301 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%156 : tensor<4x4xi1>) {
    ^bb0(%out: i1):
      %683 = arith.shrsi %out, %out : i1
      %684 = arith.shli %683, %out : i1
      %685 = arith.remui %683, %out : i1
      %686 = arith.addi %out, %out : i1
      %687 = arith.ceildivui %684, %686 : i1
      %c1812393145_i32 = arith.constant 1812393145 : i32
      %688 = arith.maxui %685, %685 : i1
      %689 = arith.shrsi %c1812393145_i32, %c1812393145_i32 : i32
      %690 = arith.remsi %688, %687 : i1
      linalg.yield %684 : i1
    } -> tensor<4x4xi1>
    memref.store %38, %alloc_17[%c1] : memref<4xi1>
    %302 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1, d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%206 : tensor<4x4xf32>) outs(%39 : tensor<4x4xf32>) {
    ^bb0(%in: f32, %out: f32):
      %683 = arith.remf %out, %in : f32
      %684 = arith.addf %out, %out : f32
      %685 = arith.maximumf %683, %in : f32
      %686 = arith.remf %685, %685 : f32
      %687 = arith.divf %684, %out : f32
      %688 = arith.minimumf %in, %683 : f32
      %689 = arith.remf %688, %688 : f32
      %690 = arith.maximumf %685, %683 : f32
      %cst_24 = arith.constant 1.43072717E+9 : f32
      linalg.yield %in : f32
    } -> tensor<4x4xf32>
    %303 = linalg.matmul ins(%98, %98 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.store %81, %alloc_11[%c1, %c2] : memref<4x4xi1>
    %304 = linalg.matmul ins(%8, %98 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %305 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%65 : tensor<4xf32>) outs(%232 : tensor<4x4xf32>) {
    ^bb0(%in: f32, %out: f32):
      %683 = arith.mulf %in, %out : f32
      %684 = arith.divf %683, %out : f32
      %685 = arith.remf %684, %in : f32
      %686 = arith.maximumf %683, %out : f32
      %cst_24 = arith.constant 1.98489024E+9 : f32
      %687 = arith.negf %684 : f32
      %688 = arith.minimumf %cst_24, %in : f32
      linalg.yield %685 : f32
    } -> tensor<4x4xf32>
    %306 = arith.ori %175, %137 : i32
    %307 = arith.minimumf %189, %236 : f32
    memref.store %22, %alloc_19[%c2, %c0] : memref<4x4xi1>
    memref.copy %alloc_19, %alloc_11 : memref<4x4xi1> to memref<4x4xi1>
    %308 = arith.shli %49, %78 : i1
    %309 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%238, %207 : tensor<4xi32>, tensor<4x4xi32>) outs(%219 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.maxsi %in, %out : i32
      %684 = arith.remsi %in_24, %in_24 : i32
      %685 = arith.xori %in, %684 : i32
      %686 = arith.ceildivsi %684, %in_24 : i32
      %687 = arith.ceildivui %684, %684 : i32
      %688 = arith.muli %687, %in : i32
      %689 = arith.divsi %688, %out : i32
      %690 = arith.muli %685, %689 : i32
      %691 = arith.cmpi slt, %688, %683 : i32
      %692 = arith.ceildivsi %691, %691 : i1
      %693 = arith.subi %688, %686 : i32
      linalg.yield %in : i32
    } -> tensor<4x4xi32>
    %310 = arith.maxsi %239, %267 : i32
    %311 = arith.minui %122, %217 : i32
    %312 = memref.load %alloc_13[%c3] : memref<4xi1>
    %313 = arith.shrsi %241, %110 : i1
    %314 = linalg.matmul ins(%186, %126 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %315 = arith.cmpf uge, %60, %227 : f32
    %316 = arith.divf %129, %272 : f32
    %317 = arith.addi %false, %212 : i1
    %318 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%160 : tensor<4xf32>) outs(%171 : tensor<4x4xf32>) {
    ^bb0(%in: f32, %out: f32):
      %683 = arith.minimumf %in, %out : f32
      %684 = arith.minimumf %683, %out : f32
      %685 = arith.negf %684 : f32
      %686 = arith.divf %683, %683 : f32
      %687 = arith.addf %683, %in : f32
      %688 = arith.minimumf %685, %686 : f32
      %689 = arith.remf %685, %685 : f32
      %690 = arith.maximumf %684, %out : f32
      linalg.yield %687 : f32
    } -> tensor<4x4xf32>
    memref.store %201, %alloc_13[%c0] : memref<4xi1>
    %319 = arith.divui %228, %276 : i1
    %320 = linalg.matmul ins(%225, %177 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %321 = linalg.matmul ins(%285, %191 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) -> tensor<4x4xi1>
    memref.copy %alloc_9, %alloc_5 : memref<4xf32> to memref<4xf32>
    %322 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1, d0)>, affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%61, %alloc_4, %264 : tensor<4x4xi32>, memref<4xi32>, tensor<4xi32>) outs(%34 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %in_25: i32, %out: i32):
      %683 = arith.shrsi %in, %in : i32
      %684 = arith.addi %in, %683 : i32
      %685 = arith.ceildivsi %out, %in_25 : i32
      %686 = arith.maxsi %in_24, %683 : i32
      %687 = arith.remui %in_24, %in : i32
      %688 = arith.muli %683, %out : i32
      %689 = arith.minui %685, %in_24 : i32
      %690 = arith.ceildivui %685, %689 : i32
      %691 = arith.shrsi %689, %688 : i32
      %692 = arith.shrui %in_24, %687 : i32
      linalg.yield %690 : i32
    } -> tensor<4x4xi32>
    %323 = linalg.matmul ins(%237, %225 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %324 = arith.remf %185, %48 : f32
    %325 = arith.remsi %315, %203 : i1
    memref.store %129, %alloc_9[%c2] : memref<4xf32>
    %326 = linalg.matmul ins(%28, %177 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %327 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%156, %62 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %out: i1):
      %683 = arith.muli %in, %in_24 : i1
      linalg.yield %683 : i1
    } -> tensor<4x4xi1>
    %328 = arith.andi %100, %313 : i1
    %329 = linalg.matmul ins(%218, %146 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %330 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%167 : tensor<4xi32>) outs(%27 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %out: i32):
      %683 = arith.divsi %in, %out : i32
      %684 = arith.shli %in, %out : i32
      %685 = arith.addi %out, %684 : i32
      %686 = arith.ceildivui %in, %out : i32
      %687 = arith.subi %684, %out : i32
      %688 = arith.ceildivui %683, %685 : i32
      %689 = arith.shrui %688, %out : i32
      %690 = arith.shli %683, %684 : i32
      %691 = arith.shli %687, %690 : i32
      %692 = arith.shli %686, %in : i32
      linalg.yield %692 : i32
    } -> tensor<4x4xi32>
    %331 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%187 : tensor<4x4xi32>) outs(%287 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %out: i32):
      %683 = arith.xori %out, %in : i32
      %684 = arith.shrui %out, %in : i32
      %685 = arith.andi %out, %683 : i32
      %686 = arith.divui %683, %out : i32
      %687 = arith.subi %686, %683 : i32
      %688 = arith.ceildivui %685, %685 : i32
      %689 = arith.shrui %688, %out : i32
      %690 = arith.maxsi %out, %out : i32
      %691 = arith.andi %683, %688 : i32
      linalg.yield %688 : i32
    } -> tensor<4x4xi32>
    %332 = arith.maxui %41, %35 : i32
    memref.copy %alloc_4, %alloc : memref<4xi32> to memref<4xi32>
    %333 = linalg.matmul ins(%279, %124 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.store %29, %alloc_13[%c3] : memref<4xi1>
    %334 = arith.andi %295, %313 : i1
    memref.store %142, %alloc_9[%c2] : memref<4xf32>
    memref.copy %alloc_5, %alloc_12 : memref<4xf32> to memref<4xf32>
    %335 = arith.remui %136, %198 : i32
    memref.copy %alloc_16, %alloc_10 : memref<4x4xf32> to memref<4x4xf32>
    %336 = linalg.matmul ins(%61, %261 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.store %306, %alloc[%c2] : memref<4xi32>
    %337 = memref.load %alloc_7[%c1] : memref<4xf32>
    %338 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%263, %36 : tensor<4xf32>, tensor<4xf32>) outs(%0 : tensor<4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4xf32>
    %339 = memref.load %alloc_9[%c2] : memref<4xf32>
    %340 = arith.shrui %293, %136 : i32
    memref.store %false, %alloc_13[%c0] : memref<4xi1>
    memref.copy %alloc_11, %alloc_19 : memref<4x4xi1> to memref<4x4xi1>
    %341 = linalg.matmul ins(%237, %331 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.copy %alloc_14, %alloc_13 : memref<4xi1> to memref<4xi1>
    %342 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%alloc, %264, %167 : memref<4xi32>, tensor<4xi32>, tensor<4xi32>) outs(%126 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %in_25: i32, %out: i32):
      %683 = arith.xori %in_25, %in_25 : i32
      %684 = arith.xori %out, %in_25 : i32
      %685 = arith.remui %in_24, %out : i32
      %686 = arith.subi %out, %out : i32
      %687 = arith.maxsi %685, %684 : i32
      %688 = arith.ceildivui %in_24, %out : i32
      %689 = arith.shrsi %683, %in : i32
      %690 = arith.muli %688, %688 : i32
      %691 = arith.divui %690, %in : i32
      %692 = arith.shli %687, %691 : i32
      linalg.yield %685 : i32
    } -> tensor<4x4xi32>
    %343 = arith.addf %36, %263 : tensor<4xf32>
    %344 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%18, %252 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %345 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%64, %11 : tensor<4x4xf32>, tensor<4x4xf32>) outs(%10 : tensor<4x4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4x4xf32>
    %346 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%alloc_18, %184, %71 : memref<4xi32>, tensor<4xi32>, tensor<4x4xi32>) outs(%251 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %in_25: i32, %out: i32):
      %683 = arith.addi %out, %in : i32
      %684 = arith.andi %in, %out : i32
      %685 = arith.addi %in_24, %684 : i32
      %686 = arith.divui %in_25, %685 : i32
      %687 = arith.xori %in_25, %in_25 : i32
      %688 = arith.muli %684, %683 : i32
      %689 = arith.minui %in_25, %out : i32
      %690 = arith.shrsi %in, %685 : i32
      %691 = arith.minsi %689, %689 : i32
      %692 = arith.maxui %688, %686 : i32
      linalg.yield %691 : i32
    } -> tensor<4x4xi32>
    %347 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%161, %14 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %out: i1):
      %683 = arith.muli %in, %in_24 : i1
      linalg.yield %683 : i1
    } -> tensor<4x4xi1>
    %348 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%15, %343 : tensor<4xf32>, tensor<4xf32>) outs(%0 : tensor<4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4xf32>
    memref.store %198, %alloc_15[%c3] : memref<4xi32>
    %349 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%163, %318 : tensor<4x4xf32>, tensor<4x4xf32>) outs(%10 : tensor<4x4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4x4xf32>
    %350 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%280, %331 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %cst_22 = arith.constant 0x4C9B46A3 : f32
    %351 = memref.load %alloc_3[%c2] : memref<4xi1>
    %352 = linalg.matmul ins(%282, %309 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.copy %alloc_14, %alloc_17 : memref<4xi1> to memref<4xi1>
    %353 = linalg.matmul ins(%274, %55 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.copy %alloc_5, %alloc_7 : memref<4xf32> to memref<4xf32>
    %354 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%184, %342 : tensor<4xi32>, tensor<4x4xi32>) outs(%186 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.remui %in_24, %in : i32
      %684 = arith.ceildivsi %683, %out : i32
      %685 = arith.shrui %in, %in_24 : i32
      %686 = arith.xori %684, %685 : i32
      %687 = arith.muli %685, %686 : i32
      %688 = arith.maxsi %687, %685 : i32
      %689 = arith.minui %687, %685 : i32
      %690 = arith.remui %689, %out : i32
      %691 = arith.divui %688, %in_24 : i32
      %692 = arith.andi %691, %in : i32
      linalg.yield %684 : i32
    } -> tensor<4x4xi32>
    memref.copy %alloc_5, %alloc_8 : memref<4xf32> to memref<4xf32>
    %355 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%alloc_5, %65 : memref<4xf32>, tensor<4xf32>) outs(%0 : tensor<4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4xf32>
    %356 = linalg.matmul ins(%14, %141 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) -> tensor<4x4xi1>
    %357 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%207 : tensor<4x4xi32>) {
    ^bb0(%out: i32):
      %683 = arith.ceildivui %out, %out : i32
      %684 = arith.minsi %683, %out : i32
      %c790935524_i32 = arith.constant 790935524 : i32
      %685 = arith.ceildivui %684, %684 : i32
      %686 = arith.floordivsi %684, %c790935524_i32 : i32
      %687 = arith.ceildivsi %686, %684 : i32
      %688 = arith.ceildivui %683, %684 : i32
      %689 = arith.xori %c790935524_i32, %688 : i32
      %690 = arith.ceildivui %687, %683 : i32
      %691 = arith.muli %687, %684 : i32
      %692 = arith.divui %687, %690 : i32
      linalg.yield %689 : i32
    } -> tensor<4x4xi32>
    %358 = arith.shrui %267, %240 : i32
    %359 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%94 : tensor<4x4xf32>) {
    ^bb0(%out: f32):
      %683 = arith.negf %out : f32
      %684 = arith.divf %out, %out : f32
      %685 = arith.mulf %683, %684 : f32
      %686 = arith.negf %684 : f32
      %687 = arith.negf %685 : f32
      %688 = arith.addf %685, %685 : f32
      %689 = arith.minimumf %684, %685 : f32
      %690 = arith.remf %688, %689 : f32
      %cst_24 = arith.constant 0x4E23EC8B : f32
      %691 = arith.mulf %685, %689 : f32
      linalg.yield %cst_24 : f32
    } -> tensor<4x4xf32>
    %360 = arith.remf %316, %254 : f32
    memref.store %129, %alloc_16[%c1, %c3] : memref<4x4xf32>
    memref.copy %alloc_9, %alloc_12 : memref<4xf32> to memref<4xf32>
    %361 = arith.maxui %239, %233 : i32
    %362 = arith.shli %174, %265 : i1
    %363 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%321, %62 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %out: i1):
      %683 = arith.muli %in, %in_24 : i1
      linalg.yield %683 : i1
    } -> tensor<4x4xi1>
    memref.copy %alloc_3, %alloc_14 : memref<4xi1> to memref<4xi1>
    %364 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%55, %alloc, %223 : tensor<4x4xi32>, memref<4xi32>, tensor<4x4xi32>) outs(%75 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %in_25: i32, %out: i32):
      %683 = arith.remui %in_24, %in_25 : i32
      %684 = arith.shrsi %in_24, %in_25 : i32
      %685 = arith.floordivsi %684, %in : i32
      %686 = arith.minsi %out, %out : i32
      %687 = arith.subi %in, %684 : i32
      %688 = arith.cmpi slt, %in_24, %687 : i32
      %689 = arith.shrsi %in, %out : i32
      %690 = arith.cmpi uge, %685, %686 : i32
      %691 = arith.cmpi ne, %690, %688 : i1
      %692 = arith.muli %688, %690 : i1
      %693 = arith.maxsi %683, %684 : i32
      %694 = arith.ceildivui %687, %693 : i32
      linalg.yield %689 : i32
    } -> tensor<4x4xi32>
    memref.store %293, %alloc[%c0] : memref<4xi32>
    memref.store %337, %alloc_10[%c3, %c1] : memref<4x4xf32>
    %365 = linalg.matmul ins(%281, %82 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %366 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d1, d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%1, %56, %171 : tensor<4xf32>, tensor<4xf32>, tensor<4x4xf32>) outs(%94 : tensor<4x4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %in_25: f32, %out: f32):
      %683 = arith.negf %out : f32
      %684 = arith.minimumf %in_24, %out : f32
      %685 = arith.addf %in_25, %684 : f32
      %686 = arith.mulf %684, %in_25 : f32
      %687 = arith.negf %685 : f32
      %688 = arith.mulf %in_25, %685 : f32
      %689 = arith.remf %688, %683 : f32
      linalg.yield %684 : f32
    } -> tensor<4x4xf32>
    memref.copy %alloc_5, %alloc_8 : memref<4xf32> to memref<4xf32>
    %367 = arith.maxsi %203, %143 : i1
    %368 = arith.remui %201, %174 : i1
    %369 = arith.remf %291, %162 : f32
    memref.store %255, %alloc_10[%c2, %c0] : memref<4x4xf32>
    %370 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%alloc_3, %4, %192 : memref<4xi1>, tensor<4xi1>, tensor<4xi1>) outs(%285 : tensor<4x4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %in_25: i1, %out: i1):
      %683 = arith.ceildivui %in_25, %in_25 : i1
      %684 = arith.andi %683, %in : i1
      %685 = arith.maxui %in_25, %out : i1
      %686 = arith.addi %in_25, %684 : i1
      %687 = arith.shrsi %684, %685 : i1
      %688 = arith.remsi %out, %in_24 : i1
      %689 = arith.subi %688, %in_25 : i1
      %690 = arith.remsi %684, %688 : i1
      linalg.yield %in : i1
    } -> tensor<4x4xi1>
    memref.store %cst_21, %alloc_12[%c2] : memref<4xf32>
    %371 = arith.ceildivsi %328, %81 : i1
    %372 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%alloc_9, %258 : memref<4xf32>, tensor<4xf32>) outs(%0 : tensor<4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4xf32>
    %373 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d1, d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%238, %21, %251 : tensor<4xi32>, tensor<4xi32>, tensor<4x4xi32>) outs(%44 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %in_25: i32, %out: i32):
      %683 = arith.andi %out, %in : i32
      %684 = arith.addi %in_24, %in_25 : i32
      %685 = arith.ceildivui %in, %out : i32
      %686 = arith.maxui %684, %684 : i32
      %c410049103_i32 = arith.constant 410049103 : i32
      %687 = arith.ceildivui %true, %true : i1
      %688 = arith.floordivsi %c410049103_i32, %683 : i32
      %689 = arith.muli %684, %c410049103_i32 : i32
      linalg.yield %689 : i32
    } -> tensor<4x4xi32>
    %374 = linalg.matmul ins(%223, %71 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %375 = memref.load %alloc_10[%c3, %c1] : memref<4x4xf32>
    memref.store %351, %alloc_17[%c3] : memref<4xi1>
    %376 = arith.minimumf %235, %37 : f32
    %377 = linalg.matmul ins(%364, %350 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %378 = linalg.matmul ins(%302, %345 : tensor<4x4xf32>, tensor<4x4xf32>) outs(%10 : tensor<4x4xf32>) -> tensor<4x4xf32>
    %379 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%alloc_4, %alloc_4 : memref<4xi32>, memref<4xi32>) outs(%287 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.ceildivui %in, %in_24 : i32
      %684 = arith.remui %in_24, %in : i32
      %685 = arith.muli %683, %in : i32
      %c1586294529_i32 = arith.constant 1586294529 : i32
      %686 = arith.shli %684, %c1586294529_i32 : i32
      %687 = arith.minui %683, %684 : i32
      %c1618635674_i32 = arith.constant 1618635674 : i32
      %688 = arith.divui %in, %684 : i32
      linalg.yield %688 : i32
    } -> tensor<4x4xi32>
    %380 = arith.cmpi sge, %328, %false : i1
    memref.copy %alloc_7, %alloc_12 : memref<4xf32> to memref<4xf32>
    %381 = arith.remui %288, %147 : i1
    %382 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%50, %333 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    memref.copy %alloc, %alloc_4 : memref<4xi32> to memref<4xi32>
    %383 = arith.shrui %325, %95 : i1
    %384 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%alloc_18, %alloc_4 : memref<4xi32>, memref<4xi32>) outs(%326 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in_24, %in : i32
      %684 = arith.divsi %in_24, %in : i32
      %685 = arith.divsi %in, %684 : i32
      %686 = arith.cmpi sle, %in_24, %in : i32
      %687 = arith.addi %out, %in_24 : i32
      %688 = arith.xori %685, %in_24 : i32
      %689 = arith.remsi %688, %683 : i32
      %690 = arith.divsi %683, %684 : i32
      %691 = arith.cmpi ult, %688, %689 : i32
      %692 = arith.floordivsi %683, %687 : i32
      %693 = arith.ceildivui %690, %685 : i32
      linalg.yield %685 : i32
    } -> tensor<4x4xi32>
    memref.store %368, %alloc_11[%c0, %c3] : memref<4x4xi1>
    %385 = linalg.matmul ins(%352, %354 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %386 = arith.divsi %243, %243 : i32
    memref.copy %alloc_17, %alloc_14 : memref<4xi1> to memref<4xi1>
    %387 = linalg.generic {indexing_maps = [affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>, affine_map<(d0) -> (d0)>], iterator_types = ["parallel"]} ins(%6, %348 : tensor<4xf32>, tensor<4xf32>) outs(%0 : tensor<4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4xf32>
    memref.store %145, %alloc_15[%c0] : memref<4xi32>
    %388 = linalg.matmul ins(%207, %279 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %389 = arith.subi %315, %107 : i1
    %390 = arith.cmpi sge, %110, %true : i1
    %391 = linalg.matmul ins(%298, %327 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) -> tensor<4x4xi1>
    %392 = arith.remui %true, %228 : i1
    %393 = arith.mulf %283, %84 : f32
    memref.store %true, %alloc_3[%c3] : memref<4xi1>
    %394 = bufferization.to_memref %1 : memref<4xf32>
    %395 = bufferization.to_memref %4 : memref<4xi1>
    %396 = bufferization.to_memref %5 : memref<4xf32>
    %397 = bufferization.to_memref %6 : memref<4xf32>
    %398 = bufferization.to_memref %11 : memref<4x4xf32>
    %399 = bufferization.to_memref %14 : memref<4x4xi1>
    %400 = bufferization.to_memref %15 : memref<4xf32>
    %401 = bufferization.to_memref %16 : memref<4xf32>
    %402 = bufferization.to_memref %17 : memref<4xi1>
    %403 = bufferization.to_memref %18 : memref<4x4xi32>
    %404 = bufferization.to_memref %19 : memref<4x4xi32>
    %405 = bufferization.to_memref %21 : memref<4xi32>
    %406 = bufferization.to_memref %27 : memref<4x4xi32>
    %407 = bufferization.to_memref %28 : memref<4x4xi32>
    %408 = bufferization.to_memref %34 : memref<4x4xi32>
    %409 = bufferization.to_memref %39 : memref<4x4xf32>
    %410 = bufferization.to_memref %43 : memref<4x4xi32>
    %411 = bufferization.to_memref %44 : memref<4x4xi32>
    %412 = bufferization.to_memref %45 : memref<4x4xi1>
    %413 = bufferization.to_memref %50 : memref<4x4xi32>
    %414 = bufferization.to_memref %51 : memref<4x4xf32>
    %415 = bufferization.to_memref %55 : memref<4x4xi32>
    %416 = bufferization.to_memref %56 : memref<4xf32>
    %417 = bufferization.to_memref %61 : memref<4x4xi32>
    %418 = bufferization.to_memref %63 : memref<4x4xi1>
    %419 = bufferization.to_memref %65 : memref<4xf32>
    %420 = bufferization.to_memref %66 : memref<4x4xi32>
    %421 = bufferization.to_memref %69 : memref<4x4xi32>
    %422 = bufferization.to_memref %73 : memref<4x4xi32>
    %423 = bufferization.to_memref %75 : memref<4x4xi32>
    %424 = bufferization.to_memref %82 : memref<4x4xi32>
    %425 = bufferization.to_memref %85 : memref<4x4xi32>
    %426 = bufferization.to_memref %87 : memref<4xi32>
    %427 = bufferization.to_memref %88 : memref<4x4xi32>
    %428 = bufferization.to_memref %90 : memref<4x4xi32>
    %429 = bufferization.to_memref %91 : memref<4x4xi32>
    %430 = bufferization.to_memref %92 : memref<4x4xi32>
    %431 = bufferization.to_memref %97 : memref<4xi1>
    %432 = bufferization.to_memref %98 : memref<4x4xi32>
    %433 = bufferization.to_memref %101 : memref<4x4xi32>
    %434 = bufferization.to_memref %102 : memref<4x4xf32>
    %435 = bufferization.to_memref %104 : memref<4x4xi32>
    %436 = bufferization.to_memref %109 : memref<4xi1>
    %437 = bufferization.to_memref %113 : memref<4xi1>
    %438 = bufferization.to_memref %115 : memref<4x4xi1>
    %439 = bufferization.to_memref %116 : memref<4x4xi32>
    %440 = bufferization.to_memref %117 : memref<4x4xi32>
    %441 = bufferization.to_memref %119 : memref<4x4xi32>
    %442 = bufferization.to_memref %125 : memref<4xf32>
    %443 = bufferization.to_memref %131 : memref<4x4xi32>
    %444 = bufferization.to_memref %132 : memref<4x4xi32>
    %445 = bufferization.to_memref %133 : memref<4x4xi32>
    %446 = bufferization.to_memref %138 : memref<4x4xi1>
    %447 = bufferization.to_memref %144 : memref<4x4xi32>
    %448 = bufferization.to_memref %146 : memref<4x4xi32>
    %449 = bufferization.to_memref %148 : memref<4x4xi32>
    %450 = bufferization.to_memref %149 : memref<4xf32>
    %451 = bufferization.to_memref %153 : memref<4x4xi32>
    %452 = bufferization.to_memref %156 : memref<4x4xi1>
    %453 = bufferization.to_memref %160 : memref<4xf32>
    %454 = bufferization.to_memref %161 : memref<4x4xi1>
    %455 = bufferization.to_memref %165 : memref<4x4xi32>
    %456 = bufferization.to_memref %166 : memref<4x4xi32>
    %457 = bufferization.to_memref %167 : memref<4xi32>
    %458 = bufferization.to_memref %171 : memref<4x4xf32>
    %459 = bufferization.to_memref %172 : memref<4x4xi1>
    %460 = bufferization.to_memref %173 : memref<4x4xi1>
    %461 = bufferization.to_memref %177 : memref<4x4xi32>
    %462 = bufferization.to_memref %181 : memref<4x4xi1>
    %463 = bufferization.to_memref %182 : memref<4x4xi32>
    %464 = bufferization.to_memref %183 : memref<4x4xi32>
    %465 = bufferization.to_memref %184 : memref<4xi32>
    %466 = bufferization.to_memref %186 : memref<4x4xi32>
    %467 = bufferization.to_memref %187 : memref<4x4xi32>
    %468 = bufferization.to_memref %193 : memref<4x4xi32>
    %469 = bufferization.to_memref %197 : memref<4x4xi32>
    %470 = bufferization.to_memref %200 : memref<4x4xi32>
    %471 = bufferization.to_memref %202 : memref<4x4xf32>
    %472 = bufferization.to_memref %204 : memref<4x4xi32>
    %473 = bufferization.to_memref %205 : memref<4x4xf32>
    %474 = bufferization.to_memref %206 : memref<4x4xf32>
    %475 = bufferization.to_memref %207 : memref<4x4xi32>
    %476 = bufferization.to_memref %209 : memref<4x4xi32>
    %477 = bufferization.to_memref %213 : memref<4x4xi32>
    %478 = bufferization.to_memref %214 : memref<4x4xi32>
    %479 = bufferization.to_memref %215 : memref<4xi1>
    %480 = bufferization.to_memref %218 : memref<4x4xi32>
    %481 = bufferization.to_memref %221 : memref<4x4xi32>
    %482 = bufferization.to_memref %223 : memref<4x4xi32>
    %483 = bufferization.to_memref %224 : memref<4xi1>
    %484 = bufferization.to_memref %225 : memref<4x4xi32>
    %485 = bufferization.to_memref %237 : memref<4x4xi32>
    %486 = bufferization.to_memref %238 : memref<4xi32>
    %487 = bufferization.to_memref %242 : memref<4x4xi32>
    %488 = bufferization.to_memref %244 : memref<4x4xf32>
    %489 = bufferization.to_memref %247 : memref<4xi1>
    %490 = bufferization.to_memref %251 : memref<4x4xi32>
    %491 = bufferization.to_memref %253 : memref<4x4xi32>
    %492 = bufferization.to_memref %257 : memref<4x4xf32>
    %493 = bufferization.to_memref %258 : memref<4xf32>
    %494 = bufferization.to_memref %259 : memref<4x4xi32>
    %495 = bufferization.to_memref %264 : memref<4xi32>
    %496 = bufferization.to_memref %266 : memref<4x4xf32>
    %497 = bufferization.to_memref %268 : memref<4x4xi32>
    %498 = bufferization.to_memref %269 : memref<4x4xi32>
    %499 = bufferization.to_memref %277 : memref<4x4xi32>
    %500 = bufferization.to_memref %278 : memref<4xf32>
    %501 = bufferization.to_memref %280 : memref<4x4xi32>
    %502 = bufferization.to_memref %282 : memref<4x4xi32>
    %503 = bufferization.to_memref %284 : memref<4xf32>
    %504 = bufferization.to_memref %285 : memref<4x4xi1>
    %505 = bufferization.to_memref %286 : memref<4xf32>
    %506 = bufferization.to_memref %297 : memref<4x4xi32>
    %507 = bufferization.to_memref %298 : memref<4x4xi1>
    %508 = bufferization.to_memref %299 : memref<4x4xi32>
    %509 = bufferization.to_memref %301 : memref<4x4xi1>
    %510 = bufferization.to_memref %302 : memref<4x4xf32>
    %511 = bufferization.to_memref %303 : memref<4x4xi32>
    %512 = bufferization.to_memref %304 : memref<4x4xi32>
    %513 = bufferization.to_memref %305 : memref<4x4xf32>
    %514 = bufferization.to_memref %314 : memref<4x4xi32>
    %515 = bufferization.to_memref %318 : memref<4x4xf32>
    %516 = bufferization.to_memref %320 : memref<4x4xi32>
    %517 = bufferization.to_memref %321 : memref<4x4xi1>
    %518 = bufferization.to_memref %322 : memref<4x4xi32>
    %519 = bufferization.to_memref %323 : memref<4x4xi32>
    %520 = bufferization.to_memref %329 : memref<4x4xi32>
    %521 = bufferization.to_memref %331 : memref<4x4xi32>
    %522 = bufferization.to_memref %333 : memref<4x4xi32>
    %523 = bufferization.to_memref %336 : memref<4x4xi32>
    %524 = bufferization.to_memref %338 : memref<4xf32>
    %525 = bufferization.to_memref %341 : memref<4x4xi32>
    %526 = bufferization.to_memref %342 : memref<4x4xi32>
    %527 = bufferization.to_memref %343 : memref<4xf32>
    %528 = bufferization.to_memref %344 : memref<4x4xi32>
    %529 = bufferization.to_memref %345 : memref<4x4xf32>
    %530 = bufferization.to_memref %346 : memref<4x4xi32>
    %531 = bufferization.to_memref %347 : memref<4x4xi1>
    %532 = bufferization.to_memref %348 : memref<4xf32>
    %533 = bufferization.to_memref %349 : memref<4x4xf32>
    %534 = bufferization.to_memref %350 : memref<4x4xi32>
    %535 = bufferization.to_memref %352 : memref<4x4xi32>
    %536 = bufferization.to_memref %353 : memref<4x4xi32>
    %537 = bufferization.to_memref %354 : memref<4x4xi32>
    %538 = bufferization.to_memref %355 : memref<4xf32>
    %539 = bufferization.to_memref %357 : memref<4x4xi32>
    %540 = bufferization.to_memref %363 : memref<4x4xi1>
    %541 = bufferization.to_memref %364 : memref<4x4xi32>
    %542 = bufferization.to_memref %365 : memref<4x4xi32>
    %543 = bufferization.to_memref %366 : memref<4x4xf32>
    %544 = bufferization.to_memref %370 : memref<4x4xi1>
    %545 = bufferization.to_memref %372 : memref<4xf32>
    %546 = bufferization.to_memref %373 : memref<4x4xi32>
    %547 = bufferization.to_memref %374 : memref<4x4xi32>
    %548 = bufferization.to_memref %378 : memref<4x4xf32>
    %549 = bufferization.to_memref %379 : memref<4x4xi32>
    %550 = bufferization.to_memref %382 : memref<4x4xi32>
    %551 = bufferization.to_memref %384 : memref<4x4xi32>
    memref.copy %467, %519 : memref<4x4xi32> to memref<4x4xi32>
    %552 = linalg.matmul ins(%194, %359 : tensor<4x4xf32>, tensor<4x4xf32>) outs(%10 : tensor<4x4xf32>) -> tensor<4x4xf32>
    memref.store %108, %449[%c1, %c0] : memref<4x4xi32>
    memref.store %358, %501[%c3, %c0] : memref<4x4xi32>
    %553 = arith.remf %185, %220 : f32
    %554 = arith.addf %272, %48 : f32
    %555 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%451, %420 : memref<4x4xi32>, memref<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    memref.store %c1683202192_i32, %487[%c2, %c3] : memref<4x4xi32>
    %556 = memref.load %510[%c0, %c2] : memref<4x4xf32>
    %557 = arith.remf %23, %316 : f32
    %558 = arith.divui %212, %317 : i1
    memref.store %c92588919_i32, %498[%c3, %c0] : memref<4x4xi32>
    memref.store %553, %458[%c1, %c0] : memref<4x4xf32>
    %559 = arith.mulf %270, %134 : f32
    %c72771837_i32 = arith.constant 72771837 : i32
    %560 = linalg.matmul ins(%132, %132 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %561 = linalg.matmul ins(%51, %249 : tensor<4x4xf32>, tensor<4x4xf32>) outs(%10 : tensor<4x4xf32>) -> tensor<4x4xf32>
    %562 = arith.shrsi %168, %true : i1
    memref.copy %541, %497 : memref<4x4xi32> to memref<4x4xi32>
    %563 = memref.load %544[%c3, %c1] : memref<4x4xi1>
    memref.copy %464, %469 : memref<4x4xi32> to memref<4x4xi32>
    %564 = arith.maxui %77, %233 : i32
    memref.store %111, %416[%c1] : memref<4xf32>
    memref.store %108, %522[%c1, %c3] : memref<4x4xi32>
    %565 = memref.load %490[%c3, %c3] : memref<4x4xi32>
    memref.copy %413, %551 : memref<4x4xi32> to memref<4x4xi32>
    %566 = arith.divsi %315, %241 : i1
    %567 = arith.andi %30, %81 : i1
    %568 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%349, %474 : tensor<4x4xf32>, memref<4x4xf32>) outs(%10 : tensor<4x4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %out: f32):
      %683 = arith.mulf %in, %in_24 : f32
      linalg.yield %683 : f32
    } -> tensor<4x4xf32>
    %569 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%542, %262 : memref<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %570 = linalg.matmul ins(%50, %314 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %571 = arith.remf %70, %cst_21 : f32
    memref.copy %401, %397 : memref<4xf32> to memref<4xf32>
    %572 = arith.remui %100, %295 : i1
    %573 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%161, %115 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %out: i1):
      %683 = arith.muli %in, %in_24 : i1
      linalg.yield %683 : i1
    } -> tensor<4x4xi1>
    memref.copy %506, %435 : memref<4x4xi32> to memref<4x4xi32>
    memref.copy %alloc_14, %489 : memref<4xi1> to memref<4xi1>
    %574 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%50 : tensor<4x4xi32>) {
    ^bb0(%out: i32):
      %683 = arith.divui %out, %out : i32
      %684 = arith.shli %683, %683 : i32
      %685 = arith.muli %684, %out : i32
      %686 = arith.remui %683, %out : i32
      %687 = arith.andi %686, %685 : i32
      %688 = arith.xori %683, %out : i32
      %689 = arith.andi %688, %686 : i32
      %690 = arith.divui %684, %688 : i32
      %691 = arith.remui %684, %out : i32
      %692 = arith.shrsi %out, %691 : i32
      %693 = arith.shrui %689, %687 : i32
      linalg.yield %685 : i32
    } -> tensor<4x4xi32>
    %575 = arith.remui %229, %122 : i32
    memref.copy %506, %445 : memref<4x4xi32> to memref<4x4xi32>
    %576 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%92, %166 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %577 = arith.maxui %362, %168 : i1
    memref.copy %421, %407 : memref<4x4xi32> to memref<4x4xi32>
    memref.copy %407, %518 : memref<4x4xi32> to memref<4x4xi32>
    %578 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1, d0)>, affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%535, %167, %528 : memref<4x4xi32>, tensor<4xi32>, memref<4x4xi32>) outs(%8 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %in_25: i32, %out: i32):
      %683 = arith.shli %in_25, %in_24 : i32
      %684 = arith.minsi %in, %in_25 : i32
      %685 = arith.floordivsi %684, %684 : i32
      %686 = arith.shrsi %684, %in_25 : i32
      %687 = arith.muli %686, %685 : i32
      %688 = arith.minui %in, %685 : i32
      %689 = arith.minui %687, %684 : i32
      %690 = arith.addi %689, %689 : i32
      %691 = arith.divui %688, %690 : i32
      %692 = arith.maxui %out, %691 : i32
      linalg.yield %in : i32
    } -> tensor<4x4xi32>
    memref.store %216, %505[%c0] : memref<4xf32>
    %579 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%alloc_15, %21, %87 : memref<4xi32>, tensor<4xi32>, tensor<4xi32>) outs(%82 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %in_25: i32, %out: i32):
      %c1836636089_i32 = arith.constant 1836636089 : i32
      %683 = arith.divsi %in, %in_25 : i32
      %684 = arith.minui %out, %out : i32
      %685 = arith.addi %in_25, %in_24 : i32
      %686 = arith.shli %685, %685 : i32
      %687 = arith.subi %in_25, %686 : i32
      %688 = arith.andi %683, %c1836636089_i32 : i32
      %689 = arith.shrsi %in_25, %683 : i32
      %690 = arith.remsi %685, %689 : i32
      linalg.yield %690 : i32
    } -> tensor<4x4xi32>
    %580 = arith.addf %257, %51 : tensor<4x4xf32>
    %581 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%63, %452 : tensor<4x4xi1>, memref<4x4xi1>) outs(%13 : tensor<4x4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %out: i1):
      %683 = arith.muli %in, %in_24 : i1
      linalg.yield %683 : i1
    } -> tensor<4x4xi1>
    memref.store %189, %alloc_5[%c2] : memref<4xf32>
    memref.copy %466, %469 : memref<4x4xi32> to memref<4x4xi32>
    memref.copy %454, %540 : memref<4x4xi1> to memref<4x4xi1>
    %582 = arith.maxsi %80, %296 : i1
    %583 = linalg.matmul ins(%569, %242 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %584 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%385, %569 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %585 = arith.minsi %122, %340 : i32
    %586 = arith.minimumf %154, %255 : f32
    memref.copy %491, %447 : memref<4x4xi32> to memref<4x4xi32>
    %587 = linalg.matmul ins(%89, %581 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) -> tensor<4x4xi1>
    %588 = arith.divf %339, %58 : f32
    %589 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%207 : tensor<4x4xi32>) {
    ^bb0(%out: i32):
      %683 = arith.floordivsi %out, %out : i32
      %684 = arith.xori %683, %683 : i32
      %685 = arith.maxui %684, %out : i32
      %686 = arith.maxui %684, %684 : i32
      %687 = arith.maxsi %683, %685 : i32
      %688 = arith.minui %683, %687 : i32
      %689 = arith.floordivsi %684, %683 : i32
      %690 = arith.muli %688, %683 : i32
      %691 = arith.addi %689, %686 : i32
      %692 = arith.andi %688, %684 : i32
      linalg.yield %684 : i32
    } -> tensor<4x4xi32>
    %590 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d1, d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%101, %555 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%234 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.shrui %in, %out : i32
      %684 = arith.remsi %683, %in : i32
      %685 = arith.remsi %684, %out : i32
      %686 = arith.remsi %out, %in : i32
      %687 = arith.minui %686, %in : i32
      %688 = arith.divui %in_24, %in_24 : i32
      %689 = arith.divsi %out, %684 : i32
      %690 = arith.shrsi %in, %in : i32
      %691 = arith.divui %685, %683 : i32
      %692 = arith.minui %683, %out : i32
      %693 = arith.maxsi %688, %691 : i32
      linalg.yield %693 : i32
    } -> tensor<4x4xi32>
    memref.store %false, %alloc_13[%c0] : memref<4xi1>
    %591 = arith.muli %317, %230 : i1
    %592 = arith.maxui %368, %312 : i1
    %593 = linalg.matmul ins(%589, %352 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.store %313, %483[%c2] : memref<4xi1>
    %594 = memref.load %alloc_10[%c1, %c0] : memref<4x4xf32>
    %595 = arith.floordivsi %233, %137 : i32
    memref.store %cst, %414[%c3, %c2] : memref<4x4xf32>
    %596 = linalg.matmul ins(%173, %191 : tensor<4x4xi1>, tensor<4x4xi1>) outs(%13 : tensor<4x4xi1>) -> tensor<4x4xi1>
    %597 = arith.divui %true, %566 : i1
    %598 = memref.load %453[%c2] : memref<4xf32>
    memref.copy %402, %436 : memref<4xi1> to memref<4xi1>
    memref.copy %500, %alloc_5 : memref<4xf32> to memref<4xf32>
    memref.store %229, %464[%c0, %c1] : memref<4x4xi32>
    %599 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1, d0)>, affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%327, %479 : tensor<4x4xi1>, memref<4xi1>) outs(%301 : tensor<4x4xi1>) {
    ^bb0(%in: i1, %in_24: i1, %out: i1):
      %683 = arith.subi %out, %in_24 : i1
      %684 = arith.shrui %in, %out : i1
      %685 = arith.minsi %out, %in_24 : i1
      %686 = arith.maxui %in_24, %683 : i1
      %687 = arith.remui %in_24, %683 : i1
      %688 = arith.remsi %683, %687 : i1
      %689 = arith.remsi %out, %688 : i1
      %690 = arith.addi %686, %out : i1
      %691 = arith.muli %688, %688 : i1
      linalg.yield %685 : i1
    } -> tensor<4x4xi1>
    %600 = arith.ceildivsi %310, %52 : i32
    %601 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%36, %348, %160 : tensor<4xf32>, tensor<4xf32>, tensor<4xf32>) outs(%51 : tensor<4x4xf32>) {
    ^bb0(%in: f32, %in_24: f32, %in_25: f32, %out: f32):
      %683 = arith.mulf %out, %in_24 : f32
      %684 = arith.maximumf %in, %in : f32
      %685 = arith.minimumf %in_25, %in : f32
      %686 = arith.negf %in_25 : f32
      %687 = arith.addf %683, %685 : f32
      %688 = arith.remf %684, %in : f32
      %689 = arith.addf %in, %686 : f32
      linalg.yield %687 : f32
    } -> tensor<4x4xf32>
    %602 = arith.mulf %23, %216 : f32
    %603 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%523, %541 : memref<4x4xi32>, memref<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    memref.store %369, %400[%c0] : memref<4xf32>
    memref.copy %539, %421 : memref<4x4xi32> to memref<4x4xi32>
    %604 = linalg.matmul ins(%388, %583 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.store %383, %504[%c1, %c1] : memref<4x4xi1>
    %605 = linalg.matmul ins(%44, %373 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %606 = arith.ori %30, %567 : i1
    %607 = arith.shrui %155, %572 : i1
    memref.store %74, %476[%c0, %c0] : memref<4x4xi32>
    memref.store %190, %alloc_10[%c2, %c2] : memref<4x4xf32>
    memref.store %248, %431[%c2] : memref<4xi1>
    %608 = memref.load %445[%c0, %c1] : memref<4x4xi32>
    %609 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%280, %82 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    memref.copy %468, %537 : memref<4x4xi32> to memref<4x4xi32>
    %610 = arith.remf %cst_21, %48 : f32
    %611 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%455, %486 : memref<4x4xi32>, memref<4xi32>) outs(%209 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.minui %in, %out : i32
      %c296737004_i32 = arith.constant 296737004 : i32
      %684 = arith.shrsi %in_24, %out : i32
      %685 = arith.ceildivui %in_24, %c296737004_i32 : i32
      %686 = arith.minui %in_24, %c296737004_i32 : i32
      %687 = arith.cmpi uge, %685, %684 : i32
      %688 = arith.cmpi ult, %687, %687 : i1
      %689 = arith.remsi %in_24, %in_24 : i32
      linalg.yield %in_24 : i32
    } -> tensor<4x4xi32>
    %612 = arith.minimumf %554, %393 : f32
    memref.store %271, %alloc_15[%c1] : memref<4xi32>
    %613 = arith.divui %78, %319 : i1
    %614 = arith.cmpf ult, %216, %70 : f32
    %615 = arith.subi %145, %137 : i32
    %616 = memref.load %537[%c3, %c3] : memref<4x4xi32>
    %617 = memref.load %428[%c2, %c2] : memref<4x4xi32>
    %618 = arith.remf %157, %235 : f32
    %619 = arith.mulf %195, %58 : f32
    %620 = arith.maximumf %129, %290 : f32
    %621 = arith.mulf %37, %129 : f32
    %622 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%182, %521 : tensor<4x4xi32>, memref<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    memref.copy %447, %470 : memref<4x4xi32> to memref<4x4xi32>
    memref.copy %459, %517 : memref<4x4xi1> to memref<4x4xi1>
    %623 = arith.remui %565, %c941507673_i32 : i32
    %624 = memref.load %548[%c2, %c1] : memref<4x4xf32>
    %625 = arith.ceildivsi %293, %585 : i32
    %626 = arith.cmpi ugt, %100, %127 : i1
    memref.store %cst_22, %442[%c2] : memref<4xf32>
    memref.copy %419, %394 : memref<4xf32> to memref<4xf32>
    %627 = arith.cmpf olt, %598, %618 : f32
    %628 = arith.cmpi ugt, %334, %68 : i1
    memref.store %233, %469[%c0, %c0] : memref<4x4xi32>
    %629 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%422, %34 : memref<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %630 = arith.addi %616, %229 : i32
    %631 = arith.shrsi %203, %591 : i1
    %632 = linalg.matmul ins(%187, %132 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.copy %alloc_11, %438 : memref<4x4xi1> to memref<4x4xi1>
    %633 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%465 : memref<4xi32>) outs(%219 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %out: i32):
      %683 = arith.remui %out, %out : i32
      %684 = arith.divui %out, %in : i32
      %685 = arith.subi %684, %in : i32
      %686 = arith.cmpi slt, %684, %out : i32
      %687 = arith.muli %684, %out : i32
      %688 = arith.remui %685, %out : i32
      %689 = arith.xori %in, %683 : i32
      %690 = arith.divsi %687, %689 : i32
      %691 = arith.minui %683, %690 : i32
      %692 = arith.ceildivui %689, %691 : i32
      linalg.yield %out : i32
    } -> tensor<4x4xi32>
    %634 = linalg.matmul ins(%333, %579 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.store %375, %515[%c3, %c1] : memref<4x4xf32>
    %635 = memref.load %403[%c0, %c2] : memref<4x4xi32>
    %636 = arith.maxsi %196, %128 : i1
    memref.store %137, %478[%c3, %c3] : memref<4x4xi32>
    %637 = arith.ori %608, %135 : i32
    %638 = arith.cmpf ugt, %154, %cst_2 : f32
    %639 = arith.cmpf uno, %586, %164 : f32
    %640 = memref.load %439[%c2, %c0] : memref<4x4xi32>
    %641 = memref.load %537[%c3, %c1] : memref<4x4xi32>
    memref.copy %406, %484 : memref<4x4xi32> to memref<4x4xi32>
    %642 = arith.cmpf ogt, %cst_0, %99 : f32
    %643 = linalg.matmul ins(%186, %357 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.copy %500, %450 : memref<4xf32> to memref<4xf32>
    %644 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%465, %264 : memref<4xi32>, tensor<4xi32>) outs(%98 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.ceildivui %in_24, %in : i32
      %684 = arith.divui %true, %true : i1
      %685 = arith.maxsi %in, %out : i32
      %686 = arith.maxsi %684, %true : i1
      %687 = arith.subi %685, %683 : i32
      %688 = arith.shli %687, %685 : i32
      %689 = arith.divsi %687, %688 : i32
      %690 = arith.remsi %out, %in : i32
      linalg.yield %690 : i32
    } -> tensor<4x4xi32>
    memref.copy %522, %440 : memref<4x4xi32> to memref<4x4xi32>
    %645 = arith.cmpi slt, %592, %230 : i1
    %646 = arith.divui %137, %386 : i32
    %647 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%27 : tensor<4x4xi32>) {
    ^bb0(%out: i32):
      %683 = arith.maxsi %out, %out : i32
      %684 = arith.remui %out, %out : i32
      %685 = arith.ceildivui %683, %out : i32
      %686 = arith.cmpi ugt, %out, %out : i32
      %687 = arith.divui %686, %686 : i1
      %688 = arith.floordivsi %683, %out : i32
      %689 = arith.remui %687, %686 : i1
      %690 = arith.remui %687, %689 : i1
      %691 = arith.shli %690, %690 : i1
      linalg.yield %out : i32
    } -> tensor<4x4xi32>
    memref.copy %446, %412 : memref<4x4xi1> to memref<4x4xi1>
    memref.copy %430, %537 : memref<4x4xi32> to memref<4x4xi32>
    %648 = arith.negf %76 : f32
    %649 = memref.load %477[%c0, %c3] : memref<4x4xi32>
    memref.store %211, %488[%c1, %c2] : memref<4x4xf32>
    memref.store %600, %405[%c2] : memref<4xi32>
    %650 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%87, %alloc : tensor<4xi32>, memref<4xi32>) outs(%330 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.divsi %out, %in_24 : i32
      %684 = arith.maxsi %683, %in : i32
      %685 = arith.minsi %684, %683 : i32
      %686 = arith.cmpi uge, %683, %683 : i32
      %687 = arith.divui %out, %685 : i32
      %688 = arith.ceildivui %684, %687 : i32
      %689 = arith.minsi %in_24, %in_24 : i32
      %690 = arith.maxsi %687, %in_24 : i32
      %691 = arith.shrsi %684, %684 : i32
      linalg.yield %684 : i32
    } -> tensor<4x4xi32>
    memref.store %335, %541[%c1, %c1] : memref<4x4xi32>
    memref.store %360, %515[%c1, %c3] : memref<4x4xf32>
    %651 = linalg.matmul ins(%302, %561 : tensor<4x4xf32>, tensor<4x4xf32>) outs(%10 : tensor<4x4xf32>) -> tensor<4x4xf32>
    memref.store %635, %405[%c0] : memref<4xi32>
    %652 = memref.load %439[%c1, %c1] : memref<4x4xi32>
    %653 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%477, %605 : memref<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    %654 = memref.load %513[%c0, %c1] : memref<4x4xf32>
    %655 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d1, d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%184, %534 : tensor<4xi32>, memref<4x4xi32>) outs(%643 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in_24, %in_24 : i32
      %684 = arith.ceildivsi %in_24, %in_24 : i32
      %685 = arith.minsi %683, %684 : i32
      %686 = arith.minui %out, %in : i32
      %687 = arith.floordivsi %686, %in_24 : i32
      %688 = arith.maxsi %687, %683 : i32
      %689 = arith.addi %688, %in_24 : i32
      %690 = arith.floordivsi %689, %in : i32
      %691 = arith.muli %687, %689 : i32
      linalg.yield %688 : i32
    } -> tensor<4x4xi32>
    %656 = arith.addi %68, %246 : i1
    memref.store %619, %505[%c3] : memref<4xf32>
    %657 = arith.remui %275, %231 : i1
    %658 = arith.divf %245, %134 : f32
    %659 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%11 : tensor<4x4xf32>) {
    ^bb0(%out: f32):
      %683 = arith.minimumf %out, %out : f32
      %684 = arith.divf %683, %683 : f32
      %685 = arith.negf %684 : f32
      %686 = arith.remf %685, %685 : f32
      %687 = arith.negf %685 : f32
      %688 = arith.negf %out : f32
      %689 = arith.remf %687, %683 : f32
      linalg.yield %686 : f32
    } -> tensor<4x4xf32>
    %660 = arith.shrsi %625, %83 : i32
    memref.store %656, %alloc_14[%c3] : memref<4xi1>
    memref.copy %432, %427 : memref<4x4xi32> to memref<4x4xi32>
    %661 = arith.negf %189 : f32
    memref.copy %503, %545 : memref<4xf32> to memref<4xf32>
    %662 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d1, d0)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%486, %388, %537 : memref<4xi32>, tensor<4x4xi32>, memref<4x4xi32>) outs(%187 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %in_25: i32, %out: i32):
      %683 = arith.remui %in_24, %in_25 : i32
      %684 = arith.ceildivui %in_25, %in_25 : i32
      %685 = arith.muli %in_25, %683 : i32
      %686 = arith.shrsi %out, %out : i32
      %687 = arith.muli %686, %684 : i32
      %688 = arith.divui %683, %in_25 : i32
      %689 = arith.maxui %out, %687 : i32
      linalg.yield %689 : i32
    } -> tensor<4x4xi32>
    memref.store %600, %520[%c3, %c0] : memref<4x4xi32>
    memref.copy %399, %alloc_11 : memref<4x4xi1> to memref<4x4xi1>
    memref.store %371, %454[%c1, %c3] : memref<4x4xi1>
    memref.store %616, %497[%c3, %c3] : memref<4x4xi32>
    memref.store %602, %515[%c2, %c2] : memref<4x4xf32>
    %663 = arith.ceildivsi %267, %641 : i32
    memref.store %25, %496[%c2, %c3] : memref<4x4xf32>
    %664 = arith.cmpi ugt, %35, %663 : i32
    %cst_23 = arith.constant 9.784990e+08 : f32
    memref.copy %527, %532 : memref<4xf32> to memref<4xf32>
    %665 = linalg.matmul ins(%609, %297 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.store %640, %523[%c0, %c1] : memref<4x4xi32>
    memref.store %553, %398[%c1, %c0] : memref<4x4xf32>
    memref.store %188, %545[%c1] : memref<4xf32>
    memref.store %c941507673_i32, %546[%c0, %c0] : memref<4x4xi32>
    %666 = memref.load %418[%c0, %c0] : memref<4x4xi1>
    memref.copy %394, %532 : memref<4xf32> to memref<4xf32>
    memref.copy %494, %534 : memref<4x4xi32> to memref<4x4xi32>
    memref.copy %408, %514 : memref<4x4xi32> to memref<4x4xi32>
    memref.copy %411, %518 : memref<4x4xi32> to memref<4x4xi32>
    memref.store %361, %520[%c3, %c0] : memref<4x4xi32>
    memref.store %67, %508[%c1, %c1] : memref<4x4xi32>
    %667 = arith.addi %614, %657 : i1
    %668 = linalg.matmul ins(%622, %61 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.copy %453, %505 : memref<4xf32> to memref<4xf32>
    %669 = memref.load %433[%c0, %c3] : memref<4x4xi32>
    %670 = linalg.matmul ins(%650, %634 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.store %c1683202192_i32, %443[%c2, %c3] : memref<4x4xi32>
    memref.copy %524, %500 : memref<4xf32> to memref<4xf32>
    memref.store %175, %520[%c3, %c1] : memref<4x4xi32>
    memref.copy %411, %512 : memref<4x4xi32> to memref<4x4xi32>
    %671 = memref.load %464[%c3, %c0] : memref<4x4xi32>
    memref.copy %472, %448 : memref<4x4xi32> to memref<4x4xi32>
    %672 = arith.maxui %595, %35 : i32
    memref.store %70, %492[%c0, %c1] : memref<4x4xf32>
    %673 = linalg.matmul ins(%242, %570 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.copy %424, %511 : memref<4x4xi32> to memref<4x4xi32>
    memref.copy %549, %541 : memref<4x4xi32> to memref<4x4xi32>
    %674 = linalg.matmul ins(%119, %73 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    memref.store %671, %447[%c3, %c0] : memref<4x4xi32>
    memref.store %575, %526[%c3, %c0] : memref<4x4xi32>
    memref.store %57, %517[%c0, %c3] : memref<4x4xi1>
    %675 = linalg.matmul ins(%379, %385 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) -> tensor<4x4xi32>
    %676 = arith.divsi %317, %607 : i1
    memref.copy %485, %542 : memref<4x4xi32> to memref<4x4xi32>
    memref.store %240, %410[%c2, %c1] : memref<4x4xi32>
    memref.store %true, %alloc_13[%c2] : memref<4xi1>
    %677 = arith.divf %559, %594 : f32
    %678 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} outs(%323 : tensor<4x4xi32>) {
    ^bb0(%out: i32):
      %683 = arith.divsi %out, %out : i32
      %684 = arith.maxsi %683, %out : i32
      %685 = arith.remsi %684, %683 : i32
      %686 = arith.andi %out, %685 : i32
      %687 = arith.shli %685, %684 : i32
      %688 = arith.ceildivsi %684, %685 : i32
      %689 = arith.maxsi %out, %685 : i32
      %690 = arith.remsi %687, %689 : i32
      %691 = arith.remsi %687, %690 : i32
      %692 = arith.addi %685, %691 : i32
      %693 = arith.remui %691, %690 : i32
      %694 = arith.maxsi %693, %687 : i32
      linalg.yield %688 : i32
    } -> tensor<4x4xi32>
    memref.store %649, %430[%c0, %c2] : memref<4x4xi32>
    memref.copy %475, %432 : memref<4x4xi32> to memref<4x4xi32>
    memref.store %672, %alloc_15[%c2] : memref<4xi32>
    memref.copy %530, %411 : memref<4x4xi32> to memref<4x4xi32>
    memref.store %376, %alloc_10[%c1, %c3] : memref<4x4xf32>
    %679 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%516, %alloc_4, %184 : memref<4x4xi32>, memref<4xi32>, tensor<4xi32>) outs(%304 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %in_25: i32, %out: i32):
      %683 = arith.remsi %out, %in_25 : i32
      %684 = arith.ceildivsi %in_24, %in_25 : i32
      %685 = arith.floordivsi %out, %out : i32
      %686 = arith.maxsi %in_25, %685 : i32
      %687 = arith.remsi %in, %in_25 : i32
      %688 = arith.xori %in_24, %687 : i32
      %689 = arith.subi %in, %out : i32
      %690 = arith.andi %684, %683 : i32
      %691 = arith.shli %690, %687 : i32
      %692 = arith.addi %in_24, %688 : i32
      linalg.yield %691 : i32
    } -> tensor<4x4xi32>
    memref.store %676, %alloc_14[%c1] : memref<4xi1>
    memref.store %376, %alloc_16[%c2, %c1] : memref<4x4xf32>
    memref.store %556, %524[%c3] : memref<4xf32>
    memref.copy %430, %468 : memref<4x4xi32> to memref<4x4xi32>
    memref.store %640, %464[%c2, %c3] : memref<4x4xi32>
    %680 = memref.load %481[%c0, %c1] : memref<4x4xi32>
    memref.copy %520, %536 : memref<4x4xi32> to memref<4x4xi32>
    memref.store %311, %519[%c3, %c1] : memref<4x4xi32>
    memref.store %198, %461[%c1, %c3] : memref<4x4xi32>
    %681 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%223, %589 : tensor<4x4xi32>, tensor<4x4xi32>) outs(%7 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %out: i32):
      %683 = arith.muli %in, %in_24 : i32
      linalg.yield %683 : i32
    } -> tensor<4x4xi32>
    memref.store %241, %479[%c1] : memref<4xi1>
    %682 = linalg.generic {indexing_maps = [affine_map<(d0, d1) -> (d1, d0)>, affine_map<(d0, d1) -> (d0)>, affine_map<(d0, d1) -> (d1, d0)>, affine_map<(d0, d1) -> (d0, d1)>], iterator_types = ["parallel", "parallel"]} ins(%193, %167, %132 : tensor<4x4xi32>, tensor<4xi32>, tensor<4x4xi32>) outs(%679 : tensor<4x4xi32>) {
    ^bb0(%in: i32, %in_24: i32, %in_25: i32, %out: i32):
      %683 = arith.maxui %out, %out : i32
      %684 = arith.divsi %out, %683 : i32
      %685 = arith.maxsi %in, %683 : i32
      %686 = arith.remsi %in_25, %out : i32
      %687 = arith.remui %685, %out : i32
      %688 = arith.divsi %in_25, %out : i32
      %689 = arith.addi %686, %688 : i32
      linalg.yield %684 : i32
    } -> tensor<4x4xi32>
    memref.copy %alloc_7, %527 : memref<4xf32> to memref<4xf32>
    memref.copy %462, %509 : memref<4x4xi1> to memref<4x4xi1>
    memref.copy %441, %404 : memref<4x4xi32> to memref<4x4xi32>
    memref.store %646, %456[%c3, %c0] : memref<4x4xi32>
    memref.store %cst_23, %493[%c2] : memref<4xf32>
    memref.copy %543, %434 : memref<4x4xf32> to memref<4x4xf32>
    memref.store %140, %415[%c2, %c0] : memref<4x4xi32>
    memref.copy %alloc_18, %405 : memref<4xi32> to memref<4xi32>
    memref.store %42, %538[%c3] : memref<4xf32>
    memref.store %680, %502[%c2, %c3] : memref<4x4xi32>
    return
  }
}

