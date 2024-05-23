import flameai.metrics

y_true = [1, 0, 1, 1, 0, 1, 0, 1, 0, 0]
y_pred = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
flameai.metrics.eval_binary(y_true, y_pred, threshold = 0.5)