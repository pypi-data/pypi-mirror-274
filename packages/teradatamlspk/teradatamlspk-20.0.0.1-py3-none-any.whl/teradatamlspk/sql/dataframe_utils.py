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

from teradatamlspk.sql.column import Column

class DataFrameUtils():

    @staticmethod
    def _tuple_to_list(args, arg_name):
        """
        Converts a tuple of string into list of string and multiple list of strings in a tuple
        to list of strings.

        PARAMETERS:
            args: tuple having list of strings or strings.

        EXAMPLES:
            tuple_to_list(args)

        RETURNS:
            list

        RAISES:
            Value error
        """
        if all(isinstance(value, str) for value in args):
            # Accept only strings in tuple.
            res_list = list(args)
        elif len(args) == 1 and isinstance(args[0], list):
            # Accept one list of strings in tuple.
            res_list = args[0]
        else:
            raise ValueError("'{}' argument accepts only strings or one list of strings".format(arg_name))
        return res_list

    @staticmethod
    def _get_columns_from_tuple_args(args, df_columns):
        """
        Converts a tuple of string, column expression or a list of strings/ column expression in a tuple
        to list of strings.

        PARAMETERS:
            args: tuple having list of strings/ column expression, strings or column expression.
            df_columns: list of column names in the DataFrame.

        EXAMPLES:
            _get_columns_from_tuple_args(args, df_columns)

        RETURNS:
            list
        """
        args = args[0] if len(args) == 1 and isinstance(args[0], list) else args
        columns = []
        for arg in args:
            if arg not in df_columns:
                pass
            else:
                arg = arg if isinstance(arg, str) else arg._tdml_column.name
                columns.append(arg)
        return columns

    @staticmethod
    def _get_agg_expr_alias_dict(expr):
        """ 
        Converts a list of Column Expressions to a dict, mapping of column name to aggregate functions.
        Also, a dict mapping of output column name to alias name (if given else output column name).

        PARAMETERS:
            expr: list of Column Expressions

        RETURNS:
            two-tuple of dictionary
        """
        expr_dict = {}
        alias_list = []
        output_col = []
        for func in expr:

            # Extract the name of column.
            col = func.expr_.compile().replace('"', "")

            # Extract function name.
            if func.agg_func_params["name"] == "count" and func.agg_func_params.get("distinct"):
                agg_func = "unique"
            else:
                agg_func = func.agg_func_params["name"]

            if col in expr_dict:
                expr_dict[col].append(agg_func)
            else:
                expr_dict[col] = [agg_func]
            col_name = agg_func + "_" + col
            output_col.append(col_name)
            alias_list.append(func.alias_name) if func.alias_name is not None else alias_list.append(col_name)
            alias_dict = dict(zip(output_col, alias_list))
        return expr_dict, alias_dict
        
