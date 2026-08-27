> **Vendored snapshot.** Source: https://github.com/UCLA-SEAL/QDiff @ `d968cbc` (fetched 2026-08-27).
> Code lives in [`src/`](src/). The generated benchmark suite (`benchmark/`, ~20k programs),
> result data (`data/`, `WrongBehavior/`), and `testing record*.txt` logs were removed — fetch the
> upstream repository for those. Original license retained in [`LICENSE`](LICENSE).


# QDiff
QDiff: Differential Testing for Quantum Software Stacks (ASE 2021)

## Summary
The past few years have witnessed the proliferation of quantum software stacks (QSS) developed in response to rapid hardware advances in quantum computing. A QSS includes a quantum programming language, an optimizing compiler that compiles a quantum algorithm expressed in a high-level language into quantum gate instructions, a quantum simulator that emu- lates these instructions on a classical device, the control software that turns circuits into analog signals sent to the quantum computer, and execution on very expensive quantum hardware. In comparison to traditional compilers and architecture simulators, QSSes are difficult to tests due to the probabilistic nature of results, the lack of clear hardware specifications, and quantum programming complexity. 

We propose a novel differential testing approach for QSSes, named QDIFF with three major innovations: (1) We generate input programs to be tested via semantics-preserving, source to source transformation to explore program variants. (2) We speed up differential testing by filtering out quantum circuits that are not worthwhile to execute on quantum hardware by analyzing static characteristics such as circuit depth, 2-gate operations, gate error rates, and T1 relaxation time. (3) We design an extensible equivalence checking mechanism via distribution comparison functions such as Kolmogorov–Smirnov test and cross entropy.

## Team 
This project is developed by Professor [Miryung Kim](http://web.cs.ucla.edu/~miryung/) and [Harry Xu](http://web.cs.ucla.edu/~harryxu/)'s group at UCLA. 
If you encounter any problems, please open an issue or feel free to contact us:

[Jiyuan Wang](http://web.cs.ucla.edu/~wangjiyuan): PhD student, wangjiyuan@cs.ucla.edu;

[Qian Zhang](http://web.cs.ucla.edu/~zhangqian/): Postdoctoral researcher, zhangqian@cs.ucla.edu;


## How to cite 
Please refer to our ASE'21 paper, [QDiff: Differential Testing for Quantum Software Stacks](https://web.cs.ucla.edu/~wangjiyuan/research/ASE2021_QDiff.pdf) for more details. 
### Bibtex  
Coming soon.


## Prerequisites

To run QDiff, you'll need to install [Qiskit](https://qiskit.org/), [Cirq](https://github.com/quantumlib/Cirq), and [Pyquil](https://github.com/rigetti/pyquil) first. If you want to use IBM quantum computer, you need to register [an IBM account](https://login.ibm.com/authsvc/mtfim/sps/authsvc?PolicyId=urn:ibm:security:authentication:asf:basicldapuser&Target=https%3A%2F%2Flogin.ibm.com%2Foidc%2Fendpoint%2Fdefault%2Fauthorize%3FqsId%3D4fe12f10-6024-45b9-8678-4efde445c742%26client_id%3DN2UwMWNkYmMtZjc3YS00).


## How to use this tool
You can start QDiff directly with the default seed programs.

```bash
python3 ./direction/to/QDiff/beginTest/QTest.py
```

## Video
Coming soon.

## FAQ 







