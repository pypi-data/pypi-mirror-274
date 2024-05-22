import numpy as np
from collections import Counter
from joblib import Parallel, delayed
from sklearn.model_selection import ParameterGrid
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error, root_mean_squared_error
from logging import basicConfig, INFO, getLogger

logger = getLogger(__name__)
basicConfig(level=INFO, format='[%(asctime)s %(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


def train_evaluate(model, X_train, X_test, y_train, y_test, print=True, describe='准确率', return_predict=False, evaluate_func=accuracy_score):
	"""Train and evaluate a model

	Parameters
    ----------
	model: Model
	X_train:
	X_test:
	y_train:
	y_test:
	print:
	describe:
	return_predict: whether return predictions
	evaluate_func: accuracy_score, mean_squared_error, root_mean_squared_error etc.

	Returns
    -------
    score or (score, predictions)

    Examples
    --------
    >>> import numpy as np
    >>> from sklearn.ensemble import RandomForestClassifier
    >>> from sklearn.model_selection import train_test_split
    >>> from sklearntools import train_evaluate
    >>> X, y = np.arange(20).reshape((10, 2)), range(10)
    >>> X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
    >>> model = RandomForestClassifier(n_estimators=837, bootstrap=False)
    >>> train_evaluate(model, X_train, X_test, y_train, y_test)
    0.88
	"""

	model.fit(X_train, y_train)
	prediction = model.predict(X_test)
	if 'classifier' == model._estimator_type:
		evaluate_func = accuracy_score
	else:
		evaluate_func = evaluate_func or mean_squared_error
	score = evaluate_func(y_test, prediction)
	if print:
		if evaluate_func == accuracy_score:
			logger.info(f'{describe}: {score:.1%}')
		else:
			if '准确率' == describe:
				if evaluate_func == mean_squared_error:
					describe = 'MSE'
				elif evaluate_func == root_mean_squared_error:
					describe = 'RMSE'
			logger.info(f'{describe}: {score:.2f}')
	if return_predict:
		return score, prediction
	return score


def train_evaluate_split(model, X, y, test_size=0.2, print=True, describe='准确率', return_predict=False, random_state=42, evaluate_func=accuracy_score):
	"""Train and evaluate a model

	Parameters
	----------
	model: Model
	X:
	y:
	test_size:
	print:
	describe:
	return_predict: whether return predictions
	random_state:
	evaluate_func: accuracy_score, mean_squared_error, root_mean_squared_error etc.

	Returns
	-------
	score or (score, predictions)

	Examples
	--------
	>>> import numpy as np
	>>> from sklearn.ensemble import RandomForestClassifier
	>>> from sklearntools import train_evaluate_split
	>>> X, y = np.arange(20).reshape((10, 2)), range(10)
	>>> model = RandomForestClassifier(n_estimators=837, bootstrap=False)
	>>> train_evaluate_split(model, X, y, test_size=0.2)
	0.88
	"""
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
	return train_evaluate(model, X_train, X_test, y_train, y_test, print, describe, return_predict, evaluate_func)


def search_model_params(model_name, X_train, X_test, y_train, y_test, param_grid, result_num=5, iter_num=8):
	"""
	Train and evaluate a model

	Parameters
	----------
	model_name:
	X_train:
	X_test:
	y_train:
	y_test:
	param_grid:
	result_num:
	iter_num:

	Examples
	--------
	>>> import numpy as np
	>>> from sklearn.ensemble import RandomForestClassifier
	>>> from sklearn.model_selection import train_test_split
	>>> from sklearntools import search_model_params
	>>> X, y = np.arange(20).reshape((10, 2)), range(10)
	>>> X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
	>>> param_grid = {'n_estimators': np.arange(800, 820, 1), 'bootstrap': [False, True]}
	>>> search_model_params(RandomForestClassifier, X_train, X_test, y_train, y_test, param_grid, result_num=3)
	"""
	classifier = 'classifier' == model_name._estimator_type
	results = Parallel(n_jobs=-1)(
		delayed(_search_params)(model_name, classifier, X_train, X_test, y_train, y_test, params) for params in
		ParameterGrid(param_grid)
	)
	results = sorted(results, key=lambda x: x[1], reverse=classifier)[:result_num]
	for param, score in results:
		if classifier:
			logger.info(f'param: {param}\tscore: {score:.1%}')
		else:
			logger.info(f'param: {param}\tscore: {score:.4f}')
		_evaluate_params(model_name, classifier, X_train, X_test, y_train, y_test, param, iter_num)


def search_model_params_split(model_name, X, y, param_grid, test_size=0.2, result_num=5, iter_num=8, random_state=42):
	"""Train and evaluate a model

	Parameters
	----------
	model_name:
	X:
	y:
	test_size:
	param_grid:
	result_num:
	iter_num:
	random_state:

	Examples
	--------
	>>> import numpy as np
	>>> from sklearn.ensemble import RandomForestClassifier
	>>> from sklearntools import search_model_params_split
	>>> X, y = np.arange(20).reshape((10, 2)), range(10)
	>>> param_grid = {'n_estimators': np.arange(800, 820, 1), 'bootstrap': [False, True]}
	>>> search_model_params_split(RandomForestClassifier, X, y, param_grid, test_size=0.2, result_num=3)
	"""
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
	return search_model_params(model_name, X_train, X_test, y_train, y_test, param_grid, result_num, iter_num)


def search_test_size(model, X, y, test_sizes=np.arange(0.15, 0.36, 0.01), random_state=42, evaluate_func=None):
	"""
	Examples
	--------
	>>> from sklearntools import search_test_size
	>>> search_test_size(model, X, y, random_state=42, evaluate_func=accuracy_score)
	"""
	classifier = 'classifier' == model._estimator_type
	results = Parallel(n_jobs=-1)(
		delayed(_search_test_size)(model, X, y, test_size, random_state, evaluate_func) for test_size in test_sizes
	)
	for test_size, score in results:
		if classifier:
			logger.info(f'test_size: {test_size:.0%} \t score: {score:.2%}')
		else:
			logger.info(f'test_size: {test_size:.0%} \t score: {score}:4f')


def search_random_state(model, X, y, random_states=np.arange(0, 20, 1), test_size=0.2, evaluate_func=None):
	"""
	Examples
	--------
	>>> from sklearntools import search_random_state
	>>> search_random_state(model, X, y, test_size=0.2, evaluate_func=accuracy_score)
	"""
	classifier = 'classifier' == model._estimator_type
	results = Parallel(n_jobs=-1)(
		delayed(_search_random_state)(model, X, y, test_size, random_state, evaluate_func) for random_state in random_states
	)
	for random_state, score in results:
		if classifier:
			logger.info(f'random_state: {random_state} \t score: {score:.2%}')
		else:
			logger.info(f'random_state: {random_state} \t score: {score}:4f')


def search_random_state2(model, X_train, X_test, y_train, y_test, random_states=np.arange(0, 20, 1), evaluate_func=None):
	"""
	Examples
	--------
	>>> from sklearntools import search_random_state2
	>>> search_test_size2(model, X_train, X_test, y_train, y_test, random_state=42, evaluate_func=accuracy_score)
	"""
	classifier = 'classifier' == model._estimator_type
	results = Parallel(n_jobs=-1)(
		delayed(_search_random_state2)(model, X_train, X_test, y_train, y_test, random_state, evaluate_func) for random_state in random_states
	)
	for random_state, score in results:
		if classifier:
			logger.info(f'random_state: {random_state} \t score: {score:.2%}')
		else:
			logger.info(f'random_state: {random_state} \t score: {score}:4f')


def _search_test_size(model, X, y, test_size, random_state, evaluate_func):
	return test_size, train_evaluate_split(model, X, y, test_size, False, None, False, random_state, evaluate_func)


def _search_random_state(model, X, y, test_size, random_state, evaluate_func):
	return random_state, train_evaluate_split(model, X, y, test_size, False, None, False, random_state, evaluate_func)


def _search_random_state2(model, X_train, X_test, y_train, y_test, random_state, evaluate_func):
	return random_state, train_evaluate(model, X_train, X_test, y_train, y_test, False, None, False, evaluate_func)


def _search_params(model_name, classifier, X_train, X_test, y_train, y_test, params):
	model = model_name(**params)
	model.fit(X_train, y_train)
	score = model.score(X_test, y_test)
	if not classifier:
		score = round(score, 4)
	return params, score


def _evaluate_params(model_name, classifier, X_train, X_test, y_train, y_test, param, iter_num):
	results = Parallel(n_jobs=-1)(
		delayed(_search_params)(model_name, classifier, X_train, X_test, y_train, y_test, param) for _ in range(iter_num))
	counter = Counter([result[1] for result in results])
	for score, count in sorted(counter.items(), key=lambda x: x[0], reverse=classifier):
		if classifier:
			logger.info(f'\tscore: {score:.1%}\tcount: {count}')
		else:
			logger.info(f'\tscore: {score:.4f}\tcount: {count}')

