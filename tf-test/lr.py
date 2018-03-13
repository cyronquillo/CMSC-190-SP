import sys
import os
import numpy as np

from sklearn import datasets
from scipy.optimize import minimize

# Import helper functions
# dir_path = os.path.dirname(os.path.realpath(__file__))
# sys.path.insert(0, dir_path + "/../utils")
from data_manipulation import feature_scale, train_test_split, add_bias_weights
from data_operation import accuracy_score


# The sigmoid function
def sigmoid(x):
	return 1 / (1 + np.exp(-x))

class LogisticRegression:
	def __init__(self, l=1, threshold=0.5):
		self.l = l
		self.threshold = threshold
		self.iterations = 0

	def iteration_callback(self, theta):
		self.theta = theta
		self.iterations += 1
		cost, grad = self.compute_cost_and_grad(self.theta, self.curr_X, self.curr_y)
		print('Iteration', self.iterations, ', Current cost:', cost)

	def compute_cost_and_grad(self, theta, X, y):
		"""
		Computes the cost and gradient of the function
		"""
		grad = np.zeros(self.n)

		# Predicted values using the current theta
		h = sigmoid(X.dot(theta))

		# Regularized cost function
		J = -1/self.m * (y.dot(np.log(h)) + (1-y).dot(np.log(1-h))) + (self.l/(2*self.m) * theta[1:].dot(theta[1:]))

		# Regularized gradient computation
		grad[0] = 1/self.m * X[:, 0].T.dot(h - y)
		grad[1:] = (1/self.m * X[:, 1:].T.dot(h - y)) + (self.l/self.m * theta[1:])

		return J, grad

	def fit(self, X, y, maxiter=100):
		X = add_bias_weights(X)
		self.curr_X = X
		self.curr_y = y
		self.m, self.n = X.shape
		self.theta = np.zeros(self.n)

		cost, grad = self.compute_cost_and_grad(self.theta, self.curr_X, self.curr_y)
		print('(Initial theta) Iteration', self.iterations, ', Current cost:', cost)
		minimize(self.compute_cost_and_grad, self.theta, method='BFGS', jac=True, args=(X, y), callback=self.iteration_callback, options={'disp': True, 'maxiter': maxiter})

	def predict(self, X):
		X = add_bias_weights(X)
		m = X.shape[0]
		p = np.zeros(m)
		h = sigmoid(X.dot(self.theta))

		for i in range(0, m):
			if (h[i] >= self.threshold):
				p[i] = 1

		return p


def main():
	data = datasets.load_breast_cancer()
	new_data = np.array([np.array([0.45,0.5]), np.array([0.4,0.55]), np.array([0.35,0.6]), np.array([0.3,0.65]), np.array([0.25,0.70]), np.array([0.20,0.75]), np.array([0.15,0.80]), np.array([0.10,0.85]), np.array([0.05,0.90]), np.array([0.55,0.95])])
	data.target = np.array([1,1,1,1,1,0,0,0,0,0])
	X = feature_scale(new_data)
	y = data.target


	X_train, X_test, y_train, y_test = train_test_split(X, y)

	clf = LogisticRegression()
	clf.fit(X_train, y_train)

	train_predicted = clf.predict(X_train)
	test_predicted = clf.predict(X_test)

	train_accuracy = accuracy_score(y_train, train_predicted)
	test_accuracy = accuracy_score(y_test, test_predicted)

	print('Train Accuracy:', train_accuracy)
	print('Test Accuracy:', test_accuracy)

if __name__ == "__main__":
	main()