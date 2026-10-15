#!/bin/bash

count_lines() {
    local file="$1"
    wc -l "$file" | cut -d ' ' -f 1
}

result_csv="benchmark/bug_reproduction/2023-Dec-MLIR-ISSUE/result_mlir_mlirpasstesttxt/result.csv"
echo "ID,LOC (Before),LOC (After),Reduction Rate" > "$result_csv"

skipped_files=(64067 64288 74301 74465)

for file_added in benchmark/bug_reproduction/2023-Dec-MLIR-ISSUE/added_mlir/*.mlir; do

    id=$(basename "$file_added" .mlir)

    if [[ ! " ${skipped_files[@]} " =~ " $id " ]]; then
        loc_before=$(count_lines "$file_added")
        file_result="benchmark/bug_reproduction/2023-Dec-MLIR-ISSUE/result_mlir_mlirpasstesttxt/$id.mlir"

        if [ -e "$file_result" ]; then

            loc_after=$(count_lines "$file_result")
            reduction_rate=$(awk "BEGIN {printf \"%.2f\", ($loc_before - $loc_after) / $loc_before}")
            echo "$id,$loc_before,$loc_after,$reduction_rate" >> "$result_csv"

        else
            echo "Error: $file_result not found."
        fi
    fi
    
done
