from teradataml import td_sklearn as osml
from teradatamlspk.sql.dataframe import DataFrame
from teradatamlspk.ml.util import Identifiable, _GenericMethods, _Metrics, LogisticRegressionMethods, RandomForestClassifierMethods, _NaiveBayesMethods, _OneVsRestMethods
from teradatamlspk.ml.param import Params, Param
from teradatamlspk.ml.constants import ARGUMENT_MAPPER, SPARK_TO_OSML

LinearSVC = type("LinearSVC", (Params, _GenericMethods, ), {})
LinearSVCModel = type("LinearSVCModel", (_GenericMethods, ), {"__getattr__": lambda self, item: getattr(self._spark_model_obj, item), "hasSummary": True})
LinearSVCSummary = type("LinearSVCSummary", (_Metrics, ), {})
LinearSVCTrainingSummary = type("LinearSVCTrainingSummary", (_Metrics, ), {})

LogisticRegression = type("LogisticRegression", (Params, _GenericMethods, ), {})
LogisticRegressionModel = type("LogisticRegressionModel", (LogisticRegressionMethods, ), {"__getattr__": lambda self, item: getattr(self._spark_model_obj, item), "hasSummary": True})
LogisticRegressionSummary = type("LogisticRegressionSummary", (_Metrics, ), {})
LogisticRegressionTrainingSummary = type("LogisticRegressionTrainingSummary", (_Metrics, ), {})

DecisionTreeClassifier = type("DecisionTreeClassifier", (Params, _GenericMethods, ), {"supportedImpurities": ['entropy', 'gini']})
DecisionTreeClassificationModel = type("DecisionTreeClassificationModel", (_GenericMethods, ), {"__getattr__": lambda self, item: getattr(self._spark_model_obj, item)})

GBTClassifier = type("GBTClassifier", (Params, _GenericMethods, ), {"supportedImpurities": ['friedman_mse','mse', 'mae'], "supportedFeatureSubsetStrategies": [], "supportedLossTypes": ['deviance', 'exponential']})
GBTClassificationModel = type("GBTClassificationrModel", (_GenericMethods, ), {"__getattr__": lambda self, item: getattr(self._spark_model_obj, item)})

RandomForestClassifier = type("RandomForestClassifier", (Params, _GenericMethods, ), {"supportedImpurities": ['entropy', 'gini'], "supportedFeatureSubsetStrategies": []})
RandomForestClassificationModel = type("RandomForestClassificationModel", (RandomForestClassifierMethods, ), {"__getattr__": lambda self, item: getattr(self._spark_model_obj, item), "hasSummary": True})
RandomForestClassificationSummary = type("RandomForestClassificationSummary", (_Metrics, ), {})
RandomForestClassificationTrainingSummary = type("RandomForestClassificationTrainingSummary", (_Metrics, ), {})

NaiveBayes = type("NaiveBayes", (Params, _NaiveBayesMethods, ), {})
NaiveBayesModel = type("NaiveBayesModel", (_NaiveBayesMethods, ), {"__getattr__": lambda self, item: getattr(self._spark_model_obj, item)})

MultilayerPerceptronClassifier = type("MultilayerPerceptronClassifier", (Params, _GenericMethods, ), {})
MultilayerPerceptronClassificationModel = type("MultilayerPerceptronClassificationModel", (_GenericMethods, ), {"__getattr__": lambda self, item: getattr(self._spark_model_obj, item), "hasSummary": True})
MultilayerPerceptronClassificationSummary = type("MultilayerPerceptronClassificationSummary", (_Metrics, ), {})
MultilayerPerceptronClassificationTrainingSummary = type("MultilayerPerceptronClassificationTrainingSummary", (_Metrics, ), {})

OneVsRest = type("OneVsRest", (Params, _OneVsRestMethods, ), {})
OneVsRestModel = type("OneVsRestModel", (_OneVsRestMethods, ), {"__getattr__": lambda self, item: getattr(self._spark_model_obj, item)})

