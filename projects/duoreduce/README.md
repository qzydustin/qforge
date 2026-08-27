> **Vendored snapshot.** Source: https://github.com/UCLA-SEAL/DuoReduce @ `315b22c` (fetched 2026-08-27).
> Code lives in [`src/`](src/). The bundled Perses tree (`ddmin/perses/`), bug-reproduction and
> bug-study datasets, the `onnx_env/` virtualenv, and unpopulated submodules were removed — follow
> the upstream build instructions below to reconstruct them. Original license retained in [`LICENSE`](LICENSE).

# DuoReduce: Bug Isolation for Multi-Layer Extensible Compilation (FSE 2025)

Repo for DuoReduce. We use these programs as input to test compilers and improve the debuggability of compilers

### Build
1. Clone submodule: `git submodule update --init`
2. Clone LLVM/MLIR:
```
cd onnx-mlir
git clone -n https://github.com/llvm/llvm-project.git
cd llvm-project && git checkout 21f4b84c456b471cc52016cf360e14d45f7f2960 && cd ..
```
3. Build LLVM/MLIR:
```bash
./compile_mlir.sh configure
./compile_mlir.sh build
```
4. Clone onnx-mlir submodules:
```bash
cd onnx-mlir
git submodule update --init
```
4. Build onnx-mlir and toy compiler:
```
./compile_onnxmlir.sh configure
./compile_onnxmlir.sh build
```

5. Build CIRCT:
Check the link [here](https://circt.llvm.org/docs/GettingStarted/) 

### Usage
The ddmin main algorithm and compilation dependency-aware algorithm are in the folder DDMIN. You can check the implementation with ddmin.py. You can run our benchmark by running
```bash
./run_ddmin.sh
```

It is easy to start with an example
```
python3 ddmin.py a.generic.mlir your_path_to_circt-opt circt-pass-test.txt 4
```
It means we apply delta debugging for a.generic.mlir, with possible pass in circt-pass-test.txt, and parallelize it with 4 sub-process. The general form is followed:
```
python3 ddmin.py your.mlir your_path_to_circt-opt your_mlir_pass.txt para_number [possible_test_script.sh]
```
You can add your own test oracle as a test script. It should exit 0 when it pass the oracle and exit 1 otherwise
