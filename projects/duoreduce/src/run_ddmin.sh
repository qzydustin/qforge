#!/bin/bash

for file in benchmark/bug_reproduction/2023-Dec-MLIR-ISSUE/added_mlir/*.mlir; do
  if [ $file != "benchmark/bug_reproduction/2023-Dec-MLIR-ISSUE/added_mlir/64071.mlir" ] && [ $file != "benchmark/bug_reproduction/2023-Dec-MLIR-ISSUE/added_mlir/76579.mlir" ] && [ $file != "benchmark/bug_reproduction/2023-Dec-MLIR-ISSUE/added_mlir/73191.mlir" ] && [ $file != "benchmark/bug_reproduction/2023-Dec-MLIR-ISSUE/added_mlir/73285.mlir" ]; then
    
    result_file=$(echo "$file" | sed 's/added_mlir/result_mlir/')

    # python3 ddmin/ddmin.py $file /home/yqiu054/circt/llvm/build/bin/mlir-opt ddmin/mlir-pass.txt 4 > $result_file
    python3 ddmin/ddmin.py $file ~/circt/llvm/build/bin/mlir-opt ddmin/mlir-pass.txt 4 > $result_file

    echo "$file done."

  fi
done
