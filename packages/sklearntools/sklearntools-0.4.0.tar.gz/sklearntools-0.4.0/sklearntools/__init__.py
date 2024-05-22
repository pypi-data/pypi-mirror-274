from enum import Enum
from typing import Union
from collections import Counter
from joblib import Parallel, delayed
from sklearn.model_selection import ParameterGrid
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error
from logging import basicConfig, INFO, getLogger

logger = getLogger(__name__)
basicConfig(level=INFO, format='[%(asctime)s %(levelname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class ModelType(Enum):
	CLASSIFY = 'classify'
	REGRESS = 'regress'


def train_evaluate(model, X_train, X_test, y_train, y_test, describe='准确率', return_predict=False,
				   mode_type: Union[ModelType, str] = None):
	"""Train and evaluate a model

	Parameters
    ----------
	model: Model
	X_train:
	X_test:
	y_train:
	y_test:
	describe:
	return_predict: whether return predictions
	mode_type:

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
	mode_type = mode_type or ModelType.CLASSIFY.value
	mode_type = mode_type.value if isinstance(mode_type, ModelType) else mode_type

	prediction = model.predict(X_test)
	if mode_type.lower() == ModelType.CLASSIFY.value:
		score = accuracy_score(y_test, prediction)
		logger.info(f'{describe}: {score:.1%}')
		if return_predict:
			return score, prediction
		return score
	else:
		mse = mean_squared_error(y_test, prediction)
		logger.info(f'{"MSE" if "准确率" == describe else describe}: {mse:.2f}')
		if return_predict:
			return mse, prediction
		return mse


def train_evaluate_split(model, X, y, test_size=0.2, describe='准确率', return_predict=False, random_state=42,
						 mode_type: Union[ModelType, str] = None):
	"""Train and evaluate a model

	Parameters
	----------
	model: Model
	X:
	y:
	test_size:
	describe:
	return_predict: whether return predictions
	random_state:
	mode_type:

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
	return train_evaluate(model, X_train, X_test, y_train, y_test, describe, return_predict, mode_type)


def search_model_params(model_name, X_train, X_test, y_train, y_test, param_grid, result_num=5, iter_num=8,
						mode_type: Union[ModelType, str] = None):
	"""Train and evaluate a model

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
	mode_type:

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

	mode_type = mode_type or ModelType.CLASSIFY.value
	mode_type = mode_type.value if isinstance(mode_type, ModelType) else mode_type
	if mode_type.lower() == ModelType.CLASSIFY.value:
		results = Parallel(n_jobs=-1)(
			delayed(_search_params)(model_name, X_train, X_test, y_train, y_test, params) for params in
			ParameterGrid(param_grid))
		results = sorted(results, key=lambda x: x[1], reverse=True)[:result_num]
		for param, score in results:
			logger.info(f'param: {param}\t准确率: {score:.1%}')
			_evaluate_params(model_name, X_train, X_test, y_train, y_test, param, iter_num)
	else:
		results = Parallel(n_jobs=-1)(
			delayed(_search_params_mse)(model_name, X_train, X_test, y_train, y_test, params) for params in
			ParameterGrid(param_grid))
		results = sorted(results, key=lambda x: x[1])[:result_num]
		for param, mse in results:
			logger.info(f'param: {param}\tMSE: {mse:.2f}')
			_evaluate_params_mse(model_name, X_train, X_test, y_train, y_test, param, iter_num)


def search_model_params_split(model_name, X, y, param_grid, test_size=0.2, result_num=5, iter_num=8, random_state=42,
							  mode_type: Union[ModelType, str] = None):
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
	mode_type:

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
	return search_model_params(model_name, X_train, X_test, y_train, y_test, param_grid, result_num, iter_num, mode_type)


def _search_params(model_name, X_train, X_test, y_train, y_test, params):
	model = model_name(**params)
	model.fit(X_train, y_train)
	score = model.score(X_test, y_test)
	return params, score


def _search_params_mse(model_name, X_train, X_test, y_train, y_test, params):
	model = model_name(**params)
	model.fit(X_train, y_train)
	mse = mean_squared_error(y_test, model.predict(X_test))
	return params, mse


def _evaluate_params(model_name, X_train, X_test, y_train, y_test, param, iter_num):
	results = Parallel(n_jobs=-1)(
		delayed(_search_params)(model_name, X_train, X_test, y_train, y_test, param) for _ in range(iter_num))
	counter = Counter([result[1] for result in results])
	for score, count in sorted(counter.items(), key=lambda x: x[0], reverse=True):
		logger.info(f'\tscore: {score}\tcount: {count}')


def _evaluate_params_mse(model_name, X_train, X_test, y_train, y_test, param, iter_num):
	results = Parallel(n_jobs=-1)(
		delayed(_search_params_mse)(model_name, X_train, X_test, y_train, y_test, param) for _ in range(iter_num))
	counter = Counter([result[1] for result in results])
	for mse, count in sorted(counter.items(), key=lambda x: x[0]):
		logger.info(f'\tMSE: {mse}\tcount: {count}')
