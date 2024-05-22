# ##################################################################
#
# Copyright 2023 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: Pradeep Garre(pradeep.garre@teradata.com)
# Secondary Owner: Adithya Avvaru(adithya.avvaru@teradata.com)
#
#
# Version: 1.0
#
# ##################################################################
import teradataml, re
from teradataml import create_context, get_context, remove_context, configure, display, execute_sql
from teradataml.dataframe.dataframe import DataFrame as tdml_DataFrame
from teradatamlspk.sql.dataframe import DataFrame
from teradatamlspk.sql.catalog import Catalog
from teradatamlspk.sql.readwriter import DataFrameReader
from teradatamlspk.conf import RuntimeConfig


display.max_rows = 20

class TeradataSession:

    catalog = Catalog()
    conf = RuntimeConfig()

    @property
    def version(self):
        return configure.database_version

    @property
    def teradataContext(self):
        from teradatamlspk import TeradataContext
        return TeradataContext()

    class Builder:

        def config(self, key=None, value=None, conf=None, map=None):
            TeradataSession.conf = conf if conf else RuntimeConfig()
            return self

        def enableHiveSupport(self):
            return self

        def getOrCreate(self, **kwargs):
            context = get_context()
            if not context:
                create_context(**kwargs)

            return TeradataSession()

        def master(self, master):
            return self

        def remote(self, url):
            return self

        def appName(self, name):
            return self

        def create(self, **kwargs):
            create_context(**kwargs)
            return TeradataSession()

    builder = Builder()

    def createDataFrame(self, data):
        """
        :param data: Vantage Table name.
        :return: teradataml DataFrame.
        """
        if isinstance(data, str):
            return DataFrame(tdml_DataFrame(data))

    def getActiveSession(self):
        return self

    def active(self):
        return self

    @staticmethod
    def newSession():
        raise NotImplemented("The API is not supported in Teradata Vantage.")

    @property
    def readStream(self):
        raise NotImplemented("The API is not supported in Teradata Vantage.")

    def sql(self, sqlQuery, args=None, kwargs=None):
        if args:
            sqlQuery = sqlQuery.format(**args)
        if re.search(r'^\s*select', sqlQuery, re.IGNORECASE):
            return DataFrame(tdml_DataFrame.from_query(sqlQuery))
        else:
            return execute_sql(sqlQuery)


    @property
    def read(self):
        return DataFrameReader()

    @staticmethod
    def stop():
        remove_context()
        return

    @staticmethod
    def streams():
        raise NotImplemented("Not Applicable for Teradata Vantage.")

    @staticmethod
    def udf():
        raise NotImplemented("Not supported yet in Teradata Vantage.")

    @staticmethod
    def udtf():
        raise NotImplemented("Not supported yet Teradata Vantage.")

    @staticmethod
    def addArtifact():
        raise NotImplemented("Not Applicable for Teradata Vantage.")

    @staticmethod
    def addArtifacts():
        raise NotImplemented("Not Applicable for Teradata Vantage.")

    @staticmethod
    def copyFromLocalToFs():
        raise NotImplemented("Not Applicable for Teradata Vantage.")

    @staticmethod
    def client():
        raise NotImplemented("Not Applicable for Teradata Vantage.")

    @staticmethod
    def interruptAll():
        raise NotImplemented("Not Applicable for Teradata Vantage.")

    @staticmethod
    def interruptTag():
        raise NotImplemented("Not Applicable for Teradata Vantage.")

    @staticmethod
    def interruptOperation():
        raise NotImplemented("Not Applicable for Teradata Vantage.")

    @staticmethod
    def addTag():
        raise NotImplemented("Not Applicable for Teradata Vantage.")

    @staticmethod
    def removeTag():
        raise NotImplemented("Not Applicable for Teradata Vantage.")

    @staticmethod
    def getTags():
        raise NotImplemented("Not Applicable for Teradata Vantage.")

    @staticmethod
    def clearTags():
        raise NotImplemented("Not Applicable for Teradata Vantage.")

    @staticmethod
    def table(tableName):
        return DataFrame(tableName)

    def range(self, start, end=None, step=1, numPartitions = None):
        raise NotImplemented("Not Applicable for Teradata Vantage.")