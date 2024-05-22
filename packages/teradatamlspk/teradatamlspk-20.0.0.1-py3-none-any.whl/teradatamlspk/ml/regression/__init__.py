from teradataml import td_sklearn as osml
from teradatamlspk.sql.dataframe import DataFrame
from teradatamlspk.ml.util import Identifiable, _GenericMethods, LinearRegressionMethods, _RegressionMetrics
from teradatamlspk.ml.param import Params, Param
from teradatamlspk.ml.constants import ARGUMENT_MAPPER, SPARK_TO_OSML


LinearRegression = type("LinearRegression", (Params, _GenericMethods, ), {})
LinearRegressionModel = type("LinearRegressionModel", (LinearRegressionMethods, ), {"__getattr__": lambda self, item: getattr(self._spark_model_obj, item), "hasSummary": True})
LinearRegressionSummary = type("LinearRegressionSummary", (_RegressionMetrics, ), {})
LinearRegressionTrainingSummary = type("LinearRegressionTrainingSummary", (_RegressionMetrics, ), {})

DecisionTreeRegressor = type("DecisionTreeRegressor", (Params, _GenericMethods, ), {"supportedImpurities": []})
DecisionTreeRegressionModel = type("DecisionTreeRegressionModel", (_GenericMethods, ), {"__getattr__": lambda self, item: getattr(self._spark_model_obj, item)})

IsotonicRegression= type("IsotonicRegression", (Params, _GenericMethods, ), {})
IsotonicRegressionModel = type("IsotonicRegressionModel", (_GenericMethods, ), {"__getattr__": lambda self, item: getattr(self._spark_model_obj, item)})

RandomForestRegressor = type("RandomForestRegressor", (Params, _GenericMethods, ), {"supportedImpurities": ['mse', 'mae'], "supportedFeatureSubsetStrategies": []})
RandomForestRegressionModel = type("RandomForestRegressionModel", (_GenericMethods, ), {"__getattr__": lambda self, item: getattr(self._spark_model_obj, item)})

GBTRegressor = type("GBTRegressor", (Params, _GenericMethods, ), {"supportedImpurities": ['friedman_mse','mse', 'mae'], "supportedFeatureSubsetStrategies": [], "supportedLossTypes": ['ls', 'lad', 'huber', 'quantile']})
GBTRegressionModel = type("GBTRegressionModel", (_GenericMethods, ), {"__getattr__": lambda self, item: getattr(self._spark_model_obj, item)})
