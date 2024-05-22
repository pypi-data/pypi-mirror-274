# ##################################################################
#
# Copyright 2024 Teradata. All rights reserved.
# TERADATA CONFIDENTIAL AND TRADE SECRET
#
# Primary Owner: Shravan Jat(shravan.jat@teradata.com)
# Secondary Owner: Pradeep Garre(pradeep.garre@teradata.com)
#
#
# Version: 1.0
#
# ##################################################################
from collections import OrderedDict
import os
from teradataml import ReadNOS, WriteNOS, read_csv, DataFrame as tdml_DataFrame, copy_to_sql
from teradataml import get_connection, execute_sql, db_list_tables, db_drop_table
from teradataml.common.utils import UtilFuncs


class DataFrameReader:
    def __init__(self, **kwargs):

        # Always
        #   'format' holds the format for file. - parquet, csv, orc etc.
        #   'mode' holds the format for file. - parquet, csv, orc etc.
        self.__params = {**kwargs}

    def format(self, source):
        self.__params.update({"stored_as": "PARQUET" if source == 'parquet' else 'TEXTFILE'})
        return DataFrameReader(**self.__params)

    def json(self, path, **kwargs):
        self.__params.update({"location": path, "stored_as": "TEXTFILE"})
        from teradatamlspk.sql.dataframe import DataFrame as tdmlspk_DataFrame
        return tdmlspk_DataFrame(ReadNOS(**self.__params).result)


    def option(self, key, value):
        self.__params[key] = value
        return DataFrameReader(**self.__params)

    def parquet(self, path, **kwargs):
        self.__params.update({"location": path, "stored_as": "PARQUET"})
        from teradatamlspk.sql.dataframe import DataFrame as tdmlspk_DataFrame
        return tdmlspk_DataFrame(ReadNOS(**self.__params).result)

    def options(self, **options):
        self.__params.update(**options)
        return DataFrameReader(**self.__params)

    def load(self, path, format = 'parquet', schema = None, **options):
        if os.path.exists(path):
            self.__params.pop('stored_as', None)
            return self.csv(path = path, schema = schema)
        if not self.__params.get("stored_as"):
            self.__params.update({"stored_as": "PARQUET" if format == 'parquet' else 'TEXTFILE'})
        self.__params.update({"location": path})
        from teradatamlspk.sql.dataframe import DataFrame as tdmlspk_DataFrame
        return tdmlspk_DataFrame(ReadNOS(**self.__params).result)

    def csv(self, path, **kwargs):
        from teradatamlspk.sql.dataframe import DataFrame as tdmlspk_DataFrame

        # Check whether to use tdml read_csv or NoS.
        # Check if the specified path is existed in clients machine or not.
        # If yes, do read_csv. Else, use NoS.
        if os.path.exists(path):

            from teradatamlspk.sql.constants import SPARK_TO_TD_TYPES

            # Define the arguments for read_csv.
            _args = {**self.__params}

            schema = kwargs.get("schema")
            if ("types" not in _args) and schema:
                # Generate types argument.
                types = OrderedDict()
                for column in schema.fieldNames():
                    types[column] = SPARK_TO_TD_TYPES[type(schema[column].dataType)]

                _args["types"] = types
            else:
                # Teradata read_csv can not infer the data.
                raise Exception("Schema is mandatory for Teradata Vantage. ")

            table_name = _args.get("table_name")
            if not table_name:
                # Generate a temp table name.
                _args["table_name"] = UtilFuncs._generate_temp_table_name(
                    prefix="tdmlspk_read_csv", gc_on_quit=True)

            _args["filepath"] = path

            # Call read_csv from teradataml.
            res = read_csv(**_args)

            # Result can be tdml DataFrame or a tuple -
            #       first element is teradataml DataFrame.
            #       second element is a dict.
            # Look read_csv documentation for details.
            if isinstance(res, tdml_DataFrame):
                return tdmlspk_DataFrame(res)

            # Now we are here. So, this returns a tuple.
            # Print the warnings and error DataFrame's dict.
            print(res[1])

            # Then return teradatamlspk DataFrame.
            return tdmlspk_DataFrame(res[0])

        self.__params.update({"location": path, "stored_as": "TEXTFILE"})

        return tdmlspk_DataFrame(ReadNOS(**self.__params).result)

class DataFrameWriterV2:
    def __init__(self, df, table, schema_name=None):
        self._df = df
        self._table_name = table
        self._schema_name = schema_name

    def append(self):
        """ Appends data to table. If table does not exist, function creates the table. """
        if self.__is_table_exists():
            sql = """
            INSERT INTO {}
            {}
            """.format(self._get_table_name(), self._df.show_query())
        else:
            sql = """
            CREATE MULTISET TABLE {} AS
            ({})
            WITH DATA
            NO PRIMARY INDEX
            """.format(self._get_table_name(), self._df.show_query())

        execute_sql(sql)

    def create(self):
        """Function to create a table based from DataFrame."""
        sql = """
        CREATE MULTISET TABLE {} AS
        ({})
        WITH DATA
        NO PRIMARY INDEX
        """.format(self._get_table_name(), self._df.show_query())
        execute_sql(sql)

    def createOrReplace(self):
        """
        Function replaces the table with DataFrame if table alreay exists.
        Else, function creates the table with DataFrame.
        """
        try:
            db_drop_table(self._table_name, schema_name=self._schema_name)
        except Exception:
            pass

        sql = """
            CREATE MULTISET TABLE {} AS
            ({})
            WITH DATA
            NO PRIMARY INDEX
            """.format(self._get_table_name(), self._df.show_query())
        execute_sql(sql)

    def replace(self):
        """Function replaces the table with DataFrame. """
        db_drop_table(self._table_name, schema_name=self._schema_name)
        sql = """
        CREATE MULTISET TABLE {} AS
        ({})
        WITH DATA
        NO PRIMARY INDEX
        """.format(self._get_table_name(), self._df.show_query())
        execute_sql(sql)

    def __is_table_exists(self):
        """Internal function to check whether table exists or not. """
        connection = get_connection()
        return connection.dialect.has_table(connection, table_name=self._table_name, schema=self._schema_name)

    def _get_table_name(self):
        return '"{}"."{}"'.format(self._schema_name, self._table_name) if self._schema_name else self._table_name


class DataFrameWriter:
    """
    teradatamlspk writer class enables users to write DataFrame on aws, azure, google cloud etc.
    using WriteNOS capability in csv or parquet format.
    """
    def __init__(self, **kwargs):
        """Constructor for writer class."""
        self.__params = {**kwargs}

    def format(self, source):
        """Specifies the underlying output data source."""
        self.__params.update({"stored_as": source.upper()})
        return DataFrameWriter(**self.__params)

    def json(self, path, **kwargs):
        """Saves the content of the DataFrame in JSON format (JSON Lines text format or newline-delimited JSON) at the specified path."""
        self.__params.update({"location": path, "stored_as": "JSON"})
        WriteNOS(**self.__params)

    def option(self, key, value):
        """Adds an output option for the underlying data source."option" are same as WriteNOS."""
        self.__params[key] = value
        return DataFrameWriter(**self.__params)

    def parquet(self, path, **kwargs):
        """Saves the content of the DataFrame in Parquet format at the specified path."""
        self.__params.update({"location": path, "stored_as": "PARQUET"})
        WriteNOS(**self.__params)

    def options(self, **options):
        """Adds output options for the underlying data source."options" are same as WriteNOS parameters."""
        self.__params.update(**options)
        return DataFrameWriter(**self.__params)

    def save(self, path, format = None, mode = None, partitionBy = None,**options):
        """
        Saves the contents of the DataFrame to a data source.
        The data source is specified by the format and a set of options.
        """
        if not self.__params.get("stored_as"):
            self.__params.update({"stored_as": format.upper()})
        self.__params.update({"location": path})
        WriteNOS(**self.__params)

    def csv(self, path, **kwargs):
        """Saves the content of the DataFrame in CSV format at the specified path."""
        self.__params.update({"location": path, "stored_as": "CSV"})
        WriteNOS(**self.__params)

    def saveAsTable(self, name, format = None, mode = 'ignore', partitionBy = None, **options):
        mode_dict ={"ignore": "fail", "overwrite": "replace", "append": "append"}
        _args = {"df": self.__params["data"],
                 "table_name": name,
                 "if_exists": mode_dict[self.__params["mode"]] if self.__params.get("mode", None) else mode_dict[mode]}
        if self.__params.get("types", None):
            _args.update({"types": self.__params["types"]})
        copy_to_sql(**_args)

    def insertInto(self, tableName, overwrite = False):
        _args = {"df": self.__params["data"],
                 "table_name": tableName,
                 "if_exists": ("replace" if self.__params["overwrite"] else "append")
                    if self.__params.get("overwrite", None)
                    else ("replace" if overwrite else "append")}
        if self.__params.get("types", None):
            _args.update({"types": self.__params["types"]})
        copy_to_sql(**_args)