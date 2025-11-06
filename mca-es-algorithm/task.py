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
X, y = load_iris(return_X_y=True)
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)
# print(f"Train samples: {len(X_train)}, Validation samples: {len(X_val)}")
# print(f"Dimension of features: {X.shape[1]} | Number of classes: {len(np.unique(y))}")

scaler = StandardScaler().fit(X_train)
X_train = scaler.transform(X_train)
X_val = scaler.transform(X_val)

# ---------------------------------------------------
# 2. Train 5 cheap base models
# ---------------------------------------------------
models = [
    LogisticRegression(max_iter=200),
    RandomForestClassifier(n_estimators=50, random_state=0),
    GradientBoostingClassifier(n_estimators=50, random_state=0),
    KNeighborsClassifier(n_neighbors=5),
    SVC(probability=True, gamma="scale", random_state=0),
]

probs_list = []
for m in models:
    m.fit(X_train, y_train)
    prediction = m.predict_proba(X_val)
    probs_list.append(prediction)

# print(f"Probability List {len(probs_list[0])}: {probs_list}")
# ---------------------------------------------------
# 3. Define ensemble and fitness function
# ---------------------------------------------------
def ensemble_probs_from_w(probs_list, w):
    w = np.clip(w, 0.0, 1.0)
    w_sum = max(w.sum(), 1e-12)
    weighted = sum(w_i * p_i for w_i, p_i in zip(w, probs_list))
    return weighted / w_sum

def fitness(w):
    # Optimizer may pass Python lists; convert to numpy array for vector ops
    w = np.asarray(w, dtype=float)
    probs = ensemble_probs_from_w(probs_list, w)
    preds = np.argmax(probs, axis=1)
    acc = accuracy_score(y_val, preds)
    return 1.0 - acc   # CMA-ES minimizes this

best_w, best_loss = cma_es(
    fitness_function=fitness,
    dimension=len(models),
    max_iterations=3,
    random_seed=42,
)

final_probs = ensemble_probs_from_w(probs_list, best_w)
final_preds = np.argmax(final_probs, axis=1)
final_acc = accuracy_score(y_val, final_preds)

print({
    "best_weights": np.round(best_w, 4).tolist(),
    "validation_accuracy": float(final_acc),
    "loss": float(best_loss),
})