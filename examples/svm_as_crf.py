# a CRF with one node is the same as a multiclass SVM

from time import time
import numpy as np

from sklearn.datasets import load_iris
from sklearn.cross_validation import train_test_split

from pystruct.problems import GraphCRF
from pystruct.learners import StructuredSVM

# do a binary digit classification
iris = load_iris()
X, y = iris.data, iris.target

# make each example into a tuple of a single feature vector and an empty edge
# list
X_ = [(np.atleast_2d(x), np.empty((0, 2), dtype=np.int)) for x in X]
Y = y.reshape(-1, 1)

X_train, X_test, y_train, y_test = train_test_split(X_, Y)

pbl = GraphCRF(n_features=4, n_states=3)
svm = StructuredSVM(pbl, verbose=2, check_constraints=False, C=20, n_jobs=1)


start = time()
svm.fit(X_train, y_train)
time_svm = time() - start
y_pred = np.hstack(svm.predict(X_test))
print("Score with pystruct crf svm: %f (took %f seconds)"
      % (np.mean(y_pred == y_test), time_svm))