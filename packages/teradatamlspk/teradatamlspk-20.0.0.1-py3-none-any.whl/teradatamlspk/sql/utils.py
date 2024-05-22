# ##################################################################
#
# Copyright 2023 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: Pooja Chaudhary(pooja.chaudhary@teradata.com)
# Secondary Owner: Pradeep Garre(pradeep.garre@teradata.com)
#
#
# Version: 1.0
#
# ##################################################################
from teradatamlspk.sql.constants import *

class AnalysisException(Exception):
    def __init__(self, msg, code):
        super(AnalysisException, self).__init__(msg)
        self.code = code

def _get_spark_type(td_type):
    """
    Function to get the corresponding Spark Type from Teradata Type.
    """

    # td_type is a class.
    if isinstance(td_type, type):
        return _get_spark_type(td_type())

    # td_type is an instance of some Data Type.
    if isinstance(td_type, (CHAR, VARCHAR)):
        return TD_TO_SPARK_TYPES.get(td_type.__class__)(length=td_type.length)

    if isinstance(td_type, DECIMAL):
        return TD_TO_SPARK_TYPES.get(td_type.__class__)(precision=td_type.precision, scale=td_type.scale)

    return TD_TO_SPARK_TYPES.get(td_type.__class__)()

def _get_tdml_type(spark_type):
    # if spark_type is a class.
    if isinstance(spark_type, type):
        return _get_tdml_type(spark_type())

    # td_type is an instance of some Data Type.
    if isinstance(spark_type, (VarcharType)):
        return SPARK_TO_TD_TYPES.get(spark_type.__class__)(spark_type.length)

    if isinstance(spark_type, DecimalType):
        return SPARK_TO_TD_TYPES.get(spark_type.__class__)(spark_type.precision, spark_type.scale)
    
    return SPARK_TO_TD_TYPES.get(spark_type.__class__)()