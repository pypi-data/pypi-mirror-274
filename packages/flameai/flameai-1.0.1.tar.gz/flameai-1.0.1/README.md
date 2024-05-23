# flameai

Deep Learning Toolkit.

## Installation

Install the package: 

```bash
pip install flameai
```

## Usage

Example:

```python
import flameai.metrics

y_true = [1, 0, 1, 1, 0, 1, 0, 1, 0, 0]
y_pred = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
flameai.metrics.eval_binary(y_true, y_pred, threshold = 0.5)
```

The output will be: 

```
threshold: 0.50000
accuracy: 0.40000
precision: 0.40000
recall: 0.40000
f1_score: 0.40000
auc: 0.28000
cross-entropy loss: 4.56233
True Positive (TP): 2
True Negative (TN): 2
False Positive (FP): 3
False Negative (FN): 3
confusion matrix:
[[2 3]
 [3 2]]
```

## Development

Build:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade build

python3 -m build
```

Upload:

```bash
twine upload dist/* 
```