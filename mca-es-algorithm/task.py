import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from main import cma_es

# ---------------------------------------------------
# 1. Load and split data
# ---------------------------------------------------
X, y = load_iris(return_X_y=True)  # X: features (n_samples x n_features), y: labels
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y  # 70/30 split with stratification
)

scaler = StandardScaler().fit(X_train)  # feature scaler fit on train set
X_train = scaler.transform(X_train)  # scaled training features
X_val = scaler.transform(X_val)  # scaled validation features

# ---------------------------------------------------
# 2. Train 5 cheap base models
# ---------------------------------------------------
models = [
    LogisticRegression(max_iter=200),  # linear classifier
    RandomForestClassifier(n_estimators=50, random_state=0),  # tree ensemble
    GradientBoostingClassifier(n_estimators=50, random_state=0),  # boosting ensemble
    KNeighborsClassifier(n_neighbors=5),  # k-NN classifier
    SVC(probability=True, gamma="scale", random_state=0),  # RBF SVM with probs
]

probs_list = []  # list of per-model predicted class probabilities on validation set
for m in models:
    m.fit(X_train, y_train)  # train base model
    prediction = m.predict_proba(X_val)  # class probabilities (n_val x n_classes)
    probs_list.append(prediction)  # accumulate

# ---------------------------------------------------
# 3. Define ensemble and fitness function
# ---------------------------------------------------
def ensemble_probs_from_w(probs_list, w):
    """Compute ensemble probabilities given weights w.

    - probs_list: list of arrays (n_val x n_classes) from each model
    - w: array-like of model weights
    """
    w = np.clip(w, 0.0, 1.0)  # clamp weights to [0, 1]
    w_sum = max(w.sum(), 1e-12)  # avoid division by zero
    weighted = sum(w_i * p_i for w_i, p_i in zip(w, probs_list))  # weighted sum
    return weighted / w_sum  # normalized probabilities

def fitness(w):
    # Optimizer may pass Python lists; convert to numpy array for vector ops
    w = np.asarray(w, dtype=float)  # candidate weights vector
    probs = ensemble_probs_from_w(probs_list, w)  # ensemble probabilities
    preds = np.argmax(probs, axis=1)  # predicted class indices
    acc = accuracy_score(y_val, preds)  # validation accuracy
    return 1.0 - acc   # CMA-ES minimizes loss

best_w, best_loss = cma_es(
    fitness_function=fitness,
    dimension=len(models),
    max_iterations=3,
    random_seed=42,
)

# Clamp weights for reporting and downstream usage
best_w = np.clip(np.asarray(best_w, dtype=float), 0.0, 1.0)  # final weights in [0, 1]

final_probs = ensemble_probs_from_w(probs_list, best_w)  # ensemble probabilities with best weights
final_preds = np.argmax(final_probs, axis=1)  # ensemble predictions
final_acc = accuracy_score(y_val, final_preds)  # final validation accuracy

print({
    "validation_accuracy": float(final_acc),
    "loss": float(best_loss),
})