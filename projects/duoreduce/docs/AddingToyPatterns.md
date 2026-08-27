# Adding Toy Rewrite Patterns and Mutators

1. Follow the build instructions for onnx-mlir in the [README](README.md).
2. Add a new RewritePattern in [ToyPass.cpp](../onnx-mlir/src/Transform/ONNX/ToyPass.cpp). A guide for writing a pattern can be found [here](https://mlir.llvm.org/docs/PatternRewriter/). The following is an example of a RewritePattern:
```c++
// An OpRewritePattern is a subclass of RewritePattern that matches only a
// specific type of operation. In this case, it matches only ONNXAddOp
struct AddToMulPattern : public OpRewritePattern<ONNXAddOp> {
  // Use the constructor from the base class
  using OpRewritePattern<ONNXAddOp>::OpRewritePattern;

  // The match function returns either success() if the op matches the pattern
  // or failure() if the op does not match. This function should not modify the
  // IR in any way.
  LogicalResult match(ONNXAddOp op) const override {
    // In this example, we match only ONNXAddOp ops that have floating point operands. 
    if (op.getOperand(0).getType().dyn_cast<TensorType>().getElementType().isa<FloatType>()) {
      if (op.getOperand(0).getType().dyn_cast<TensorType>().getElementType().isa<FloatType>()) {
        return success();
      }
    }
    return failure();
  }

  // Assuming the pattern matches, the rewrite function mutates the IR to
  // perform the desired transformation. All mutations must be done with the
  // PatternRewriter object in order to track (and possibly revert) the changes
  // made.
  void rewrite(ONNXAddOp op, PatternRewriter &rewriter) const override {
    // Our transform replaces the ONNXAddOp with a ONNXMulOp
    rewriter.replaceOpWithNewOp<ONNXMulOp>(op, op.getOperand(0), op.getOperand(1));
  }
};
```
3. Add the corresponding mutator to trigger the `RewritePattern` in [ToyMutators.cpp](../onnx-mlir/src/Transform/ONNX/ToyMutators.cpp) and [ToyMutators.h](../onnx-mlir/src/Transform/ONNX/ToyMutators.h). The toy mutator takes the same form as the `RewritePattern` described above. The match function should match operations that have a similar structure/role (e.g. has the same traits or implements the same interfaces). The rewrite function should mutate the operation to satisfy the conditions of the original `RewritePattern`.