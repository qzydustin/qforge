# Delta-debugging for MLIR


## Build CIRCT

1. Follow the steps on CIRCT website [here](https://circt.llvm.org/docs/GettingStarted/)
2. You should have `circt-opt` in `circt/build/bin` folder

### Build onnx-MLIR

You should have built onnx-MLIR following the [README.md](https://github.com/wjy99-c/MLIR-s-benchmark/tree/main) 

### Usage

It is easy to start with an example
```
python3 ddmin.py a.generic.mlir your_path_to_circt-opt circt-pass-test.txt 4
```
It means we apply delta debugging for a.generic.mlir, with possible pass in circt-pass-test.txt, and parallelize it with 4 sub-process. The general form is followed:
```
python3 ddmin.py your.mlir your_path_to_circt-opt your_mlir_pass.txt para_number [possible_test_script.sh]
```
You can add your own test oracle as a test script. It should exit 0 when it pass the oracle and exit 1 otherwise
