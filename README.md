# QForge

**QForge** scopes a secure, open ecosystem for robust quantum compilation. A
quantum computer only returns trustworthy answers if the compiler that lowers a
circuit to hardware preserves its behavior on a noisy device — and today that
layer is fragmented across vendor-specific stacks with no shared governance, no
cross-vendor pass interface, and no security model for third-party
contributions. QForge brings the tooling that isolates, diagnoses, reduces, and
mitigates quantum-software failures into one platform, and plans the governance,
provenance, and community structure a durable ecosystem needs.

## The unified story

Reliable quantum compilation is a pipeline, and each founding project owns one
stage of it:

1. **Find** where hardware breaks the compiler's assumptions — **QRisk** mines
   recurring, backend-specific abnormal circuit patterns from real
   quantum-hardware executions and mitigates them with semantics-preserving
   compiler transformations.
2. **Test** that a transformation is actually behavior-preserving — **QDiff**
   generates semantics-preserving program variants and differentially tests them
   across quantum software stacks with distribution-aware equivalence checking.
3. **Reduce** a failure to something a maintainer can act on — **DuoReduce**
   isolates bugs in multi-layer extensible compilation, shrinking failing
   circuits and pass sequences to minimal reproductions.
4. **Evaluate** whether the tests that guard all of this are any good —
   **Argus** is a traceable mutation engine whose quantum-integration track
   generates quantum-aware mutants to expose gaps in test suites.

QRisk and QDiff are quantum-native today. DuoReduce and Argus are proven
foundations from classical compiler and testing research whose quantum tracks
extend the pipeline end to end.

## Repository layout

```
projects/
  qrisk/        README.md + src/   pattern discovery & compiler mitigation
  qdiff/        README.md + src/   differential testing for quantum stacks
  duoreduce/    README.md + src/   bug isolation & program reduction
  argus/        README.md + src/   traceable mutation engine
index.html, styles.css, script.js   the QForge website (GitHub Pages)
```

Each project folder is a **vendored snapshot** of its upstream repository: the
source is under `src/`, the project's own `README.md` (with a provenance banner)
sits at the folder root, and the upstream `LICENSE` is preserved where it
applies. Large datasets, generated benchmarks, virtualenvs, and result logs were
removed to keep this repository lightweight — each folder README links back to
upstream for the full material.

| Project | Upstream | Snapshot |
| --- | --- | --- |
| QRisk | [qzydustin/qrisk](https://github.com/qzydustin/qrisk) | `0d60343` |
| QDiff | [UCLA-SEAL/QDiff](https://github.com/UCLA-SEAL/QDiff) | `d968cbc` |
| DuoReduce | [UCLA-SEAL/DuoReduce](https://github.com/UCLA-SEAL/DuoReduce) | `315b22c` |
| Argus | [ucr-riple/Argus](https://github.com/ucr-riple/Argus) | `4be9881` |

## What we are building

- **Shared discovery:** one home for the tools, their use cases, documentation,
  and reproducible examples.
- **Interoperability:** shared test artifacts, representations, and adapters so
  the tools compose while staying independently useful.
- **Community practice:** open contribution paths, issue triage, release
  guidance, and feedback from researchers, practitioners, and industry partners.
- **Trust and sustainability:** transparent governance, provenance and signing
  for contributed passes, security practices, evaluation metrics, and long-term
  maintenance.

## Get involved

We welcome quantum-software researchers, tool builders, educators, students, and
industry practitioners.

- Explore the [QForge website](https://qzydustin.github.io/qforge/).
- Share feedback or report a problem through
  [Issues](https://github.com/qzydustin/qforge/issues).
- Propose documentation, examples, integrations, or community resources through a
  pull request.

## License

The QForge platform (website, documentation, and the integration glue in this
repository) is released under the [MIT License](LICENSE). Each vendored project
under `projects/` retains its own upstream license; see the `LICENSE` file inside
that folder where present.
