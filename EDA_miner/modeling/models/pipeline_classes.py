"""
This module collects every model class, including input and transformers.

Notes to others:
    Feel free to tamper with anything or add your own models and classes. \
    Everything should implement an sklearn-like API providing a fit and \
    (more importantly) a transform method. It should also have a \
    `modifiable_params` dictionary with the names of attributes that can \
    be modified and a list of possible values (keep them limited, for now). \
    Input classes should subclass `GenericInput`. If you add new classes \
    remember to modify `ml_options` in `graph_structures.py`.
"""

import numpy as np
from textblob import TextBlob

from sklearn.base import BaseEstimator, ClassifierMixin, TransformerMixin
from sklearn.base import RegressorMixin, ClusterMixin
from sklearn.cluster import KMeans, DBSCAN, Birch, AgglomerativeClustering, MeanShift
from sklearn.decomposition import PCA, NMF, TruncatedSVD
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.impute import SimpleImputer, MissingIndicator
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.linear_model import Ridge, Lasso, SGDRegressor, SGDClassifier
from sklearn.naive_bayes import BernoulliNB, GaussianNB, MultinomialNB
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler, LabelBinarizer, Binarizer
from sklearn.preprocessing import StandardScaler, MaxAbsScaler, Normalizer
from sklearn.preprocessing import OneHotEncoder, PolynomialFeatures
from sklearn.svm import SVR, SVC, LinearSVC, LinearSVR, NuSVC, NuSVR
from sklearn.tree import DecisionTreeRegressor, DecisionTreeClassifier
from sklearn.tree import ExtraTreeRegressor, ExtraTreeClassifier
from xgboost import XGBClassifier


"""
======== Custom classes ========

All custom classes should subclass these ones.
This is done for checks down the line that
determine properties of nodes of the Graph
which in turn is useful for selecting dataset
and being able to create custom features or
handle outputs
"""


class InputFile(BaseEstimator, TransformerMixin):
    """
    An input node used for selecting a user-uploaded dataset.
    """

    modifiable_params = {"dataset": [None]}

    def __init__(self, dataset=None):
        self.dataset = dataset

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X


# TODO: Actually implement this.
class DataCleaner(BaseEstimator, TransformerMixin):
    modifiable_params = {}

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        return X


# Template for creating your own node classes
class CustomClassifier(BaseEstimator, ClassifierMixin):
    modifiable_params = {}

    def fit(self, X, y=None):
        return self

    def predict(self, X):
        return np.ones(X.shape[0])


# TODO: do an actual implementation
class SentimentAnalyzer(BaseEstimator, RegressorMixin):
    modifiable_params = {}

    def predict(self, X):
        if isinstance(X, np.ndarray):
            return np.array([TextBlob(x[0]).polarity for x in X])
        else:
            return np.array([TextBlob(x).polarity for x in X])


"""
======== Prebuilt classes ========

For EVERY model that is expected to have parametrization
you are expected to give its class a `modifiable_params`
dict with keys being the function argument and values the
allowed set of values (make it limited, i.e. few choices)
Also, the first is assumed to be the default value which
will be passed to the model upon the creation of pipelines.
And of course it must have `fit` and transform methods.
"""


"""
======== Transformers ========
"""

StandardScaler.modifiable_params = {
    "with_mean": [True, False],
    "with_std": [True, False]
}

MinMaxScaler.modifiable_params = {}

MaxAbsScaler.modifiable_params = {}

LabelBinarizer.modifiable_params = {}

# TODO: Add threshold as numeric input
Binarizer.modifiable_params = {}

Normalizer.modifiable_params = {
    "norm": ["l2", "l1", "max"]
}

OneHotEncoder.modifiable_params = {
    "drop": ["first", None]
}

PolynomialFeatures.modifiable_params = {
    "degree": [2, 3, 4, 5],
    "interaction_only": [False, True],
    "include_bias": [True, False]
}

SimpleImputer.modifiable_params = {
    "strategy": ["most_frequent", "mean", "median"]
}

MissingIndicator.modifiable_params = {}

CountVectorizer.modifiable_params = {
    "stop_words": [None, "english"],
    "analyzer": ["word", "char", "char_wb"],
    "max_features": [None, 1000, 2000, 5000, 10000, 15000, 25000],
    "max_df": [1, 0.1, 0.2, 0.5, 0.75, 0.95],
    "min_df": [1, 0.1, 0.2, 0.5, 0.75, 0.95],
}

TfidfVectorizer.modifiable_params = {
    "stop_words": [None, "english"],
    "analyzer": ["word", "char", "char_wb"],
    "max_features": [None, 1000, 2000, 5000, 10000, 15000, 25000],
    "max_df": [1, 0.1, 0.2, 0.5, 0.75, 0.95],
    "min_df": [1, 0.1, 0.2, 0.5, 0.75, 0.95],
}

PCA.modifiable_params = {
    "n_components": [None, 2, 3, 5, 10, 20, 50, 100, 300],
    "whiten": [False, True],
}

NMF.modifiable_params = {
    "n_components": [None, 2, 3, 5, 10, 20, 50, 100, 300],
}

TruncatedSVD.modifiable_params = {
    "n_components": [2, None, 3, 5, 10, 20, 50, 100, 300],
}


"""
======== Regression ========
"""

LinearRegression.modifiable_params = {
    "fit_intercept": [True, False],
}

Ridge.modifiable_params = {
    "alpha": [1, 0.1, 0.2, 0.5, 2, 5, 10],
    "fit_intercept": [True, False],
}

Lasso.modifiable_params = {
    "alpha": [1, 0.1, 0.2, 0.5, 2, 5, 10],
    "fit_intercept": [True, False],
}

SVR.modifiable_params = {
    "alpha": [1, 0.1, 0.2, 0.5, 2, 5, 10],
    "kernel": ["rbf", "poly", "linear"],
    "degree": [3, 1, 2, 5, 7, 10],
    "C": [1, 0.1, 0.2, 0.5, 2, 5, 10],
}

DecisionTreeRegressor.modifiable_params = {
    "max_depth": [None, 3, 5, 7, 9, 12],
}

ExtraTreeRegressor.modifiable_params = {
    "max_depth": [None, 3, 5, 7, 9, 12],
}

DummyRegressor.modifiable_params = {
    "strategy": ["mean", "median"],
}

KNeighborsRegressor.modifiable_params = {
    "n_neighbors": [5, 3, 7, 9]
}

RandomForestRegressor.modifiable_params = {
    "n_estimators": [10, 20, 50, 100, 200, 500],
    "max_depth": [None, 3, 5, 7, 9, 12, 15],
    "max_features": ["auto", 0.1, 0.2, 0.5, 0.7, 0.9, 1]
}

SGDRegressor.modifiable_params = {
    "loss": ["squared_loss", "huber", "epsilon_insensitive",
             "squared_epsilon_insensitive"],
    "penalty": ["none", "l2", "l1", "elasticnet"],
    "l1_ratio": [0.15, 0.01, 0.05, 0.1, 0.2, 0.5, 0.75, 0.9],
    "learning_rate": ["optimal", "constant", "invscaling", "adaptive"]
}

LinearSVR.modifiable_params = {
    "C": [1, 0.01, 0.1, 0.5, 2, 5, 10],
    "fit_intercept": [True, False],
    "max_iter": [200, 50, 100, 500, 1000]
}

NuSVR.modifiable_params = {
    "nu": [0.5, 0.01, 0.1, 0.2, 0.7, 0.85, 1],
    "C": [1, 0.01, 0.1, 0.5, 2, 5, 10],
    "gamma": [1, 0.01, 0.1, 0.5, 2, 5, 10],
    "degree": [3, 1, 2, 5],
    "kernel": ["rbf", "linear", "poly", "sigmoid"],
    "max_iter": [200, 50, 100, 500, 1000]
}


"""
======== Classification ========
"""

LogisticRegression.modifiable_params = {
    "penalty": ["l2", "l1"],
    "fit_intercept": [True, False],
    "C": [1, 0.1, 0.2, 0.5, 2, 5, 10],
    "multi_class": ["ovr", "multinomial", "auto"],
}

DummyClassifier.modifiable_params = {
    "strategy": ["stratified", "most_frequent", "prior", "uniform"],
}

KNeighborsClassifier.modifiable_params = {
    "n_neighbors": [5, 3, 7, 9]
}

XGBClassifier.modifiable_params = {}

RandomForestClassifier.modifiable_params = {
    "n_estimators": [10, 20, 50, 100, 200, 500],
    "max_depth": [None, 3, 5, 7, 9, 12, 15],
    "max_features": ["auto", 0.1, 0.2, 0.5, 0.7, 0.9, 1]
}

SGDClassifier.modifiable_params = {
    "loss": ["hinge", "log", "modified_huber",
             "perceptron", "squared_loss", "huber"],
    "penalty": ["none", "l2", "l1", "elasticnet"],
    "l1_ratio": [0.15, 0.01, 0.05, 0.1, 0.2, 0.5, 0.75, 0.9],
    "learning_rate": ["optimal", "constant", "invscaling", "adaptive"]
}

LinearSVC.modifiable_params = {
    "penalty": ["l2", "l1"],
    "C": [1, 0.01, 0.1, 0.5, 2, 5, 10],
    "fit_intercept": [True, False],
    "max_iter": [200, 50, 100, 500, 1000],
}

SVC.modifiable_params = {
    "gamma": [1, 0.01, 0.1, 0.5, 2, 5, 10],
    "degree": [3, 1, 2, 5],
    "C": [1, 0.01, 0.1, 0.5, 2, 5, 10],
    "kernel": ["rbf", "poly", "sigmoid"],
    "max_iter": [200, 50, 100, 500, 1000],
}

NuSVC.modifiable_params = {
    "nu": [0.5, 0.01, 0.1, 0.2, 0.7, 0.85, 1],
    "gamma": [1, 0.01, 0.1, 0.5, 2, 5, 10],
    "degree": [3, 1, 2, 5],
    "kernel": ["rbf", "linear", "poly", "sigmoid"],
    "max_iter": [200, 50, 100, 500, 1000]
}

DecisionTreeClassifier.modifiable_params = {
    "max_depth": [None, 3, 5, 7, 9, 12],
}

ExtraTreeClassifier.modifiable_params = {
    "max_depth": [None, 3, 5, 7, 9, 12],
}


"""
======== Clustering ========
"""

KMeans.modifiable_params = {
    "n_clusters": [8, 2, 3, 4, 5, 6, 7, 9, 10, 15, 20],
}

DBSCAN.modifiable_params = {
    "eps": [0.5, 0.01, 0.05, 0.1, 0.2, 1, 2, 5],
}

Birch.modifiable_params = {
    "threshold": [0.5, 0.1, 0.2, 0.75, 0.95],
}

AgglomerativeClustering.modifiable_params = {
    "n_clusters": [2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20],
    "linkage": ["ward", "complete", "average", "single"]
}

BernoulliNB.modifiable_params = {
    "alpha": [1, 0.1, 0.2, 0.5, 0.7, 0.85],
}

GaussianNB.modifiable_params = {}

MultinomialNB.modifiable_params = {
    "alpha": [1, 0.1, 0.2, 0.5, 0.7, 0.85],
}

MeanShift.modifiable_params = {
    "bandwidth": [0.5, 0.05, 0.1, 0.2, 1, 2, 5, 10],
    "min_bin_freq": [1, 2, 3, 5, 10, 20],
    "cluster_all": [True, False]
}
