import ast, sys
import os, re, json
from collections import OrderedDict
from enum import Enum


class UserNoteType(Enum):
    NOT_SUPPORTED = 1
    PARTIALLY_SUPPORTED = 2
    NO_ACTION = 3

functions_with_default_values ={
    'LinearSVC': ['featuresCol', 'setFeaturesCol'],
    'KMeans': ['featuresCol', 'setFeaturesCol'],
    'GaussianMixture': ['featuresCol', 'setFeaturesCol'],
    'LinearRegression': ['featuresCol', 'setFeaturesCol'],
    'LogisticRegression': ['featuresCol', 'setFeaturesCol'],
    'MultilayerPerceptronClassifier': ['featuresCol', 'setFeaturesCol'],
    'DecisionTreeClassifier': ['featuresCol', 'setFeaturesCol'],
    'DecisionTreeRegressor': ['featuresCol', 'setFeaturesCol'],
    'VarianceThresholdSelector': ['featuresCol', 'setFeaturesCol'],
    'GBTClassifier': ['featuresCol', 'setFeaturesCol'],
    'RandomForestClassifier': ['featuresCol', 'setFeaturesCol'],
    'IsotonicRegression': ['featuresCol', 'setFeaturesCol'],
    'RandomForestRegressor': ['featuresCol', 'setFeaturesCol'],
    'NaiveBayes': ['featuresCol', 'setFeaturesCol'],
    'OneVsRest': ['featuresCol', 'setFeaturesCol'],
    'GBTRegressor': ['featuresCol', 'setFeaturesCol'],
    'ClusteringEvaluator': ['featuresCol', 'setFeaturesCol'],
    'UnivariateFeatureSelector': ['featuresCol', 'setFeaturesCol']
}

class UserNotes:
    def __init__(self, start_line_no, end_line_no,  python_object_name, user_notes, note_type):
        self.start_line_no = start_line_no
        self.end_line_no = end_line_no
        self.object_name = python_object_name
        self.user_notes = user_notes
        self.note_type = note_type

    def to_json(self):
        return {"Start Line No": self.start_line_no,
                "End Line No": self.end_line_no,
                "Object Name": self.object_name,
                "Notes": self.user_notes,
                "Notification Type": self.note_type.name
                }

class InvalidImport:
    def __init__(self, base_module_name, invalid_import, alias_name, start_line_no, end_line_no):
        self.base_module_name = base_module_name
        self.invalid_import = invalid_import
        self.alias_name = alias_name
        self.start_line_no = start_line_no
        self.end_line_no = end_line_no

    def __repr__(self):
        imp_stmt = "{}-{} as {}".format(self.base_module_name, self.invalid_import, self.alias_name) if self.alias_name \
            else "{}-{}".format(self.base_module_name, self.invalid_import)
        return "{}/LineNo({}, {})".format(imp_stmt, self.start_line_no, self.end_line_no)


class UserGuide:
    def __init__(self, file_name):
        self.__file_name = file_name
        self.__notes = {}

    def __get_html_table(self):
        html_table = """
        <table>
          <tr >
          
              <th>Start Line No</th>
          
              <th>End Line No</th>
          
              <th>Object Name</th>
              
              <th>Notes</th>
          </tr>
          
          {}
                  
        </table>
        """
        rows = self.__get_html_table_rows()
        return html_table.format(rows)

    def __get_html_table_rows(self):
        # Sort the records first.
        records = [rec.to_json() for rec in
                   sorted(self.__notes.values(), key=lambda user_note: user_note.start_line_no)]
        row_template = """
        <tr>
              
              <td class="{html_cls}">{start_ln_no}</td>
              
              <td class="{html_cls}">{end_ln_no}</td>
              
              <td class="{html_cls}">{python_obj_name}</td>
              
              <td class="{html_cls}">{notes}</td>
              
          </tr>
        """
        result = []
        for rec in records:
            html_row = row_template.format(html_cls=self.__get_html_cls(rec["Notification Type"]),
                                           start_ln_no=rec["Start Line No"],
                                           end_ln_no=rec["End Line No"],
                                           python_obj_name=rec["Object Name"],
                                           notes=self.__get_notes(rec["Notes"]))
            result.append(html_row)
        return "".join(result)

    @staticmethod
    def __get_notes(notes):
        # If notes has multiple elements, return it in bullet points.
        if isinstance(notes, list):
            return "".join(["<li style='margin:0 0 5px 0;'> {} </li>".format(note) for note in notes])

        return notes

    def __get_html_cls(self, notification_type):
        if notification_type == UserNoteType.PARTIALLY_SUPPORTED.name:
            return "partially_supported"
        elif notification_type == UserNoteType.NOT_SUPPORTED.name:
            return "not_supported"
        return "notification"


    def __get_html_file_content(self):
        """ Functiont to get the HTML file content. """
        template =  """
        <!DOCTYPE html>
            <html>
              <head>
                <meta charset="utf-8"/>
                <title>pyspark2teradataml</title>
                <style>
                    body {{
                      font-family: Helvetica, Arial, sans-serif;
                      font-size: 12px;
                      position: relative;
                      float: left;
                      width: 100%;
                      margin:0;
                  }}
            
                  .heading {{
              font-size: 30px;
              position: relative;
              float: left;
              width: 100%;
              text-align: center;
              color: black;
              font-weight: bold;
              margin-top: 25px;
              margin-bottom: 25px;
            }}
            
                  .imp_notes {{
              font-size: 20px;
              position: relative;
              float: left;
              width: 100%;
              text-align: left;
              color: black;
              font-weight: bold;
              margin-top: 25px;
              margin-bottom: 25px;
            }}
            
            .how_to_interpret {{
              font-size: 12px;
              position: relative;
              float: left;
              width: 100%;
              text-align: left;
              color: black;
              font-weight: bold;
              margin-top: 25px;
              margin-bottom: 25px;
            }}
            
            p {{
              color: black;
            }}
            
            a {{
              color: #999;
            }}
            
            
            table {{
              /* border: #E1EcF4 1px solid; */
              border: #E1EcF4 1px solid;
              border-collapse: collapse;
              margin-top: 35px;
              margin-left: 5px;
              margin-right: 5px;
              margin-bottom: 5px;
            }}
            
            tr {{
              border-bottom: #E1EcF4 1px solid;
              height:35px;
              /* padding-top: 5px;
              padding-bottom: 5px; */
            }}
            
            .orange_background {{
              color: chocolate;
            }}
            
            th {{
              padding-left:5px;
              vertical-align: middle;
              padding-right:5px;
              text-align:center;
              background-color:#E1EcF4; 
              color:#6A737C; 
              font-size:13px;
              border-right: #ddd 1px solid;
            }}
            
            td {{
              border-right: #E1EcF4 1px solid;
              padding-left:5px;
              vertical-align: middle;
              padding-right:5px;
              text-align:left;
              padding-bottom: 5px;
              padding-top: 5px;
            }}
            
            .not_supported {{
              color: red;
            }}
            
            .partially_supported {{
              color: blue;
            }}
            
            .notification {{
              color: black;
            }}
            
            </style>
              </head>
              <body>
                  <span class="heading"> pyspark2teradataml - {} </span>
                  <span class="imp_notes">Important Notes: </span>
                  <ul>
                  
                    <li>Refer user guide and supportability matrix for ML functions. </li>
					<li>Some functions are not supported however they are supported with manual code changes. Look at the section 'Examples' in the user guide to know more details.  </li>
					<li>ML Functions accepts multiple columns for arguments. Hence, no need to pass vectors, update the script to pass multiple columns. </li>
					<li>RDD API's are not applicable to Vantage. Make use of DataFrame API's. </li>
					<li>Columns are case sensitive in teradatamlspk and they are case insensitive in PySpark. Convert the column names to appropriate case while converting the code. </li>
                    <li>DataFrame.rdd returns same DataFrame as RDD is not applicable to Vantage. Hence use DataFrame API's and do not use RDD API's. </li>
                    <li>pyspark2teradataml does not modify the SQL statements. Users are advised to manually update the SQL statements if the corresponding SQL statement is not valid in Vantage. </li>
                  </ul>
                  <h3>Text in below table in any of below three colors. Every color has significance as explained below: </h3>
                  <ul>
                  
                    <li><span style="color: red; text-decoration: underline;">red</span>: These API's do not have functionality in teradatamlspk. User need to achieve the functionality through some other way. </li>
                    <li><span style="color: blue; text-decoration: underline;">blue </span>: These API's have functionality but there may be some difference in functionality when compared with PySpark. Notes specifies what is the exact difference so user should change it manually. </li>
                    <li><span style="color: black; text-decoration: underline;">black </span>: This is for a notification to user. User do not need to act on this message. </li>
                  </ul>
                  <div id="html_table">
                    {}
                  </div>
              </body>
            </html>
        
        """
        file_name = os.path.basename(self.__file_name)
        return template.format(file_name, self.__get_html_table())

    def add_notes(self, user_note):

        # The way the parsing is happing can produce duplicates.
        # Hence remove the duplicates.
        # Duplicates are derived based on line numbers and keyword.
        key = (user_note.start_line_no, user_note.object_name)
        if key not in self.__notes:
            self.__notes[key] = user_note
        return self

    def publish(self, path, report_type="HTML"):
        """ Publishes a user guide in HTML format. """

        html_data = self.__get_html_file_content()
        with open(path, 'w') as fp:
            fp.write(html_data)
        print("Script conversion report '{}' published successfully. ".format(path))


class _pyspark2teradatamlspk:
    """ Analyses the user script. """

    def __init__(self, file_path):

        if (not os.path.exists(file_path)):
            raise FileNotFoundError("File '{}' not found.".format(file_path))

        if not os.path.isfile(file_path):
            raise FileNotFoundError("Specified path '{}' is not a file.".format(file_path))

        self.__file_path = file_path
        user_notes = self.__get_user_notes()
        self.__unimplemented_imports = user_notes.get("not_supported")
        self.__not_supported = user_notes.get("not_supported")
        self.__partially_supported = user_notes.get("partially_supported")
        self.__notification = user_notes.get("notification")

    def __get_json_from_file(self, file_path):
        """ Gets the json from a file. """
        with open(file_path) as fp:
            return json.load(fp)

    def __get_user_notes(self):
        """ Gets the json file which has user notes. """
        return self.__get_json_from_file(os.path.join(os.path.dirname(__file__), "user_guide.json"))

    def __replace_pyspark_with_tdmlspk(self):
        with open(self.__file_path, "r") as fp:
            s = fp.read()
            rplce = re.sub('from pyspark', "from teradatamlspk", s)
            rplce = re.sub('import pyspark', "import teradatamlspk", rplce)
            rplce = re.sub('SparkSession', "TeradataSession", rplce)
            rplce = re.sub('SparkContext', "TeradataContext", rplce)
            rplce = re.sub('SparkConf', "TeradataConf", rplce)
            rplce = re.sub('.sparkContext', ".teradataContext", rplce)
            rplce = re.sub('.sparkUser', ".teradataUser", rplce)
            rplce = re.sub('getOrCreate\(\)', "getOrCreate(host=getpass.getpass('Enter host: '), user=getpass.getpass('Enter user: '), password=getpass.getpass('Enter password: '))", rplce)

        new_file = self.__get_new_file_name()
        with open(new_file, "w") as fw:
            fw.write(rplce)

        return new_file

    def __get_new_file_name(self, fmt="py"):
        if fmt == "py":
            return "{}_tdmlspk.py".format(self.__file_path[:-3])

        return "{}_tdmlspk.html".format(self.__file_path[:-3])

    def _get_module_and_py_obj(self, ast_node):
        """
        Function to return a list of InvalidImports with every tuple represents 5 elements.
        1st element represents top level module
        second element represents imported python object
        third element represents alias name of python object.
        fourth element represents starting line of import.
        fifth element represents ending line of import.
        Examples:
            If statement is - from pyspark.sql.abc import pqr as xyz, ijk
                Then function returns - [('from pyspark.sql.abc', 'pqr', 'xyz'), ('from pyspark.sql.abc', 'ijk', None)]
            If statement is - import pyspark.sql.abc.pqr as xyz, ijk
                Then function returns - [('pyspark.sql.abc', 'pqr', 'xyz'), ('ijk', 'ijk', None)]
        """
        if isinstance(ast_node, ast.ImportFrom):
            return [("from "+ast_node.module, node.name, node.asname, ast_node.lineno, ast_node.end_lineno)
                    for node in ast.walk(ast_node) if isinstance(node, ast.alias)]

        return [(".".join(node.name.split(".")[:-1]), self.__get_py_obj_name(node.name), node.asname, ast_node.lineno, ast_node.end_lineno)
                for node in ast.walk(ast_node) if isinstance(node, ast.alias)]

    @staticmethod
    def __get_module_name(s):
        return s.split(".")[0]

    @staticmethod
    def __get_py_obj_name(s):
        return s.split(".")[-1]

    def __get_invalid_imports(self, root_node):

        invalid_import_statements = []

        # walk through entire node. Get the invalid imports.
        for node in ast.walk(root_node):
            if isinstance(node, (ast.ImportFrom, ast.Import)):
                import_stmts = self._get_module_and_py_obj(node)
                invalid_imports = [InvalidImport(*imp_stmt) for imp_stmt in import_stmts if imp_stmt[1] in self.__unimplemented_imports]
                invalid_import_statements = invalid_import_statements + invalid_imports

        return invalid_import_statements

    def __segregate_invalid_imports_based_on_line_no(self, invalid_imports):
        """ Segregate the import statements that belongs to same line. """
        res = {}
        for invalid_import in invalid_imports:
            start_line, end_line = invalid_import.start_line_no, invalid_import.end_line_no
            k = (start_line, end_line)
            if k in res:
                res[k].append(invalid_import)
            else:
                res[k] = [invalid_import]

        return res

    def __remove_invalid_imports(self, invalid_imports):
        """
        Read the script again and store it in a list. The argument "invalid_imports"
        gives the reference of line numbers which has invalid import statements. Use
        those and read those lines again, parse it again using ast.
        Then either remove or replace those lines.
        """

        res = {}
        with open(self.__get_new_file_name()) as fp:
            actual_lines = fp.readlines()

        # loop through invalid imports.
        for invalid_import in invalid_imports:

            # Extract starting and ending line number.
            start_line_no, end_line_no = invalid_import

            # Note that ast gives real line numbers which starts from 1. However
            # variable 'actual_lines' starts it's index from 0.
            if start_line_no == end_line_no:
                actual_stmt = actual_lines[start_line_no-1]
            else:
                actual_stmt = "".join(actual_lines[start_line_no-1: end_line_no])

            # Variables which stores the submodule name and its alias name/parent path.
            # Store the imported submodule alias name and it's parent name in different
            # containers.
            imported_sub_modules_alias = {}
            imported_sub_modules_parent = {}

            # Variable which stores the submodule and it's parent.
            parent_module_ = ""

            # Read those lines which has invalid imports. Parse those and store it.
            for node in ast.walk(ast.parse(actual_stmt)):
                if isinstance(node, (ast.ImportFrom, ast.Import)):
                    for parent_module, sub_mod_name, alias_name, _, _ in self._get_module_and_py_obj(node):
                        imported_sub_modules_alias[sub_mod_name] = alias_name
                        imported_sub_modules_parent[sub_mod_name] = parent_module
                        parent_module_ = parent_module

            # At this stage, we have all the imported sub modules along with invalid submodules.
            # If all submodules are invalid, then the corresponding line(s) needs to be replaced with
            # empty string.
            if len(imported_sub_modules_alias) == len(invalid_imports[invalid_import]):
                if start_line_no == end_line_no:
                    res[start_line_no] = ""
                else:
                    res.update({i: "" for i in range(start_line_no, end_line_no+1)})
            else:
                # Here comes the tricky part. Some of the submodules are supported and
                # some are not.

                # First, find out valid sub modules so that only those can be kept.
                invalid_sub_modules = [mod.invalid_import for mod in invalid_imports[invalid_import]]
                valid_sub_modules = set(imported_sub_modules_alias) - set(invalid_sub_modules)

                # If the statement is of type 'from abc...', then prepare the statement again with only valid names.
                # Note that alias names should be kept as it is.
                if str(parent_module).startswith("from"):
                    sub_mod_str_ = ['{} as {}'.format(sub_mod, imported_sub_modules_alias[sub_mod]) if imported_sub_modules_alias[sub_mod]
                                    else sub_mod for sub_mod in valid_sub_modules]
                    stmt = "{} import {}".format(parent_module_, ", ".join(sub_mod_str_))
                else:
                    # If the statement is of type 'import abc...', even then prepare the statement again but there
                    # is a chance that the parent of submodule remains same as submodule. for example, when you parse
                    # 'import xyz as abc' with function _get_module_and_py_obj, the first element which represents parent
                    # and second element which represents submodule remains same because both are xyz and xyz here.
                    sub_mod_str_ = []
                    for sub_module in valid_sub_modules:

                        # Check if sub_module is associated with some parent path or not.
                        sub_mod_parent = imported_sub_modules_parent[sub_module]
                        if sub_mod_parent and sub_mod_parent!=sub_module:
                            sub_mod = "{}.{}".format(sub_mod_parent, sub_module)
                        else:
                            sub_mod = sub_module

                        # Check if it has alias or not.
                        sub_mod_lias = imported_sub_modules_alias[sub_module]
                        if sub_mod_lias:
                            sub_mod = '{} as {}'.format(sub_mod, sub_mod_lias)
                        else:
                            pass

                        sub_mod_str_.append(sub_mod)

                    stmt = "import {}".format(", ".join(sub_mod_str_))

                # If the statement spans for single line, then modify that line alone.
                # Else, modify the first line and create empty lines for subsequent lines.
                if start_line_no == end_line_no:
                    res[start_line_no] = stmt
                else:
                    res[start_line_no] = stmt
                    res.update({i: "" for i in range(start_line_no+1, end_line_no+1)})

        for line_no, new_stmt in res.items():
            _index = line_no - 1
            # Append new line character to statement.
            actual_lines[_index] = new_stmt+"\n"

        # Import getpass. Do not create a new line as line numbers may vary between the actual script
        # and new script and user may be confused when comparing the generated one with existing one.
        # Get the first import. Then, embed this string at the begining. - 'import getpass'.
        # NOTE: Do not embed at end as some of the imports may go to next line with a line delimiter.
        for index, line in enumerate(actual_lines):
            if line.startswith("import ") or line.startswith("from "):
                actual_lines[index] = "import getpass; {}".format(line)
                break;

        f_name = self.__get_new_file_name()
        with open(f_name, 'w') as fw:
            fw.writelines(actual_lines)

        return res

    def __get_node_details(self, node):
        """ Internal function to extract the keyword used in script. """
        # Extract the function.
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            return node.func.id, node.lineno, node.end_lineno
        # Extract Attribute.
        elif isinstance(node, ast.Attribute):
            return node.attr, node.lineno, node.end_lineno
        elif isinstance(node, ast.Name):
            return node.id, node.lineno, node.end_lineno
        # Extract read.csv() or read.json() or write.csv() kind of notations.
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and isinstance(node.func.value, ast.Attribute):
            return "{}.{}".format(node.func.value.attr, node.func.attr), node.lineno, node.end_lineno
        return None, None, None

    def __recurse_node(self, node, start_line_number, end_line_number, store_line_number):
        """
        DESCRIPTION:
            Function recursively traverse the node, find the line number of this arguments
            ['inputCol', 'inputCols', 'featuresCol', 'setInputCol', 'setInputCols', 'setFeaturesCol']
            which should be present in method.
            Example:
                * it will include this line 'assembler1(inputCols="column")'
                   and ignore this line 'inputCols = "name"'

        PARAMETERS:
            node:
                Required Argument.
                Specifies node present in ast.
                Types: ast object

            start_line_number:
                Required Argument.
                Stores start line of method.
                Types: int

            end_line_number:
                Required Argument.
                Stores end line of method.
                Types: int

            store_line_number:
                Required Argument.
                Stores line number of methods which contain
                ['inputCol', 'inputCols', 'featuresCol', 'setInputCol',
                 'setInputCols', 'setFeaturesCol']
                Types: list

        RETURNS:
            None

        Example:
            >>> input_file = 'assembler1(inputCols="column")'
            >>> node = ast.parse(input_file)
            >>> __recurse_node(node, 0, 0, store_line_number)
            >>> print(store_line_number)
            >>>[(1, 1, 'inputCols')]

        """
        if hasattr(node, "__dict__"):
            for key, value in node.__dict__.items():
                if node.__dict__.get('arg', None) in ['inputCol', 'inputCols', 'featuresCol']:
                    store_line_number.append((start_line_number, end_line_number, node.__dict__.get('arg')))
                elif isinstance(value, list):
                    for x in value:
                        self.__recurse_node(x, node.__dict__.get('lineno', -1), node.__dict__.get('end_lineno', -1), store_line_number)
                else:
                    self.__recurse_node(value, node.__dict__.get('lineno', -1), node.__dict__.get('end_lineno', -1), store_line_number)
        else:
            if node in ['setInputCol', 'setInputCols', 'setFeaturesCol']:
                store_line_number.append((start_line_number, end_line_number, node))

    def __change_input_cols(self, store_line_number, user_guide):
        """
        DESCRIPTION:
            Function change the value of arguments ['inputCol', 'inputCols', 'featuresCol',
            'setInputCol', 'setInputCols', 'setFeaturesCol'] to "<Specify list of column names>"
            based on store_line_number and also updates html.
            Example:
                * assembler1(inputCols="column") --> assembler1(inputCols="<Specify list of column names>")

        PARAMETERS:
            store_line_number:
                Required Argument.
                Stores line number of methods which contain
                ['inputCol', 'inputCols', 'featuresCol', 'setInputCol',
                 'setInputCols', 'setFeaturesCol']
                Types: list
            user_guide:
                Required Argument.
                stores line number and keywords to generate html.
                Types: Class

        RETURNS:
            None
        """
        # Read the new file
        with open(self.__get_new_file_name()) as fp:
            actual_lines = fp.readlines()
        # Look for featuresCol, InputCols, InputCol, setInputCol, setInputCols, setFeaturesCol
        for start_line_number, end_line_number, value in store_line_number:

            # Replace values for 'setInputCol', 'setInputCols', 'setFeaturesCol' stored in "store_line_number".
            if value in ['setInputCol', 'setInputCols', 'setFeaturesCol']:
                for idx in range(start_line_number, end_line_number+1):
                    line = actual_lines[idx-1]
                    # To replace value we first find a ['setInputCol', 'setInputCols', 'setFeaturesCol'] as a index,
                    # Using that index we find a start index which should start from '(' and end_index should end with
                    # either ')' or '\n' then we replace the value.
                    pattern = re.compile(value+r"\s*?\(([^[]*?)[\)|\n]")
                    indexes = []
                    for match in re.finditer(pattern, line):
                        indexes.append(match.span(1))
                    for start_index, end_index in reversed(indexes):
                        line = "".join([line[:start_index], "\"<Specify list of column names>\"", line[end_index:]])
                    actual_lines[idx - 1] = line

                # Replace values for 'inputCol', 'inputCols', 'featuresCol' stored in "store_line_number".
                # To replace value we first find a ['inputCol', 'inputCols', 'featuresCol'] as a index,
                # Using that index we find a start index which should start from '=' and end_index should end with
                # either ')' or '\n' or ',' then we replace the value.
                # For VectorAssembler we are ignoring this.
            elif value in ['inputCol', 'inputCols', 'featuresCol']:
                for idx in range(start_line_number, end_line_number+1):
                    # ast line number starts with 1 while reading file using 'open' starts with 0
                    line = actual_lines[idx-1]
                    pattern = re.compile(value+r"\s*?=([^[]*?)[,|\n|\)]")
                    indexes = []
                    exclude_string, st_idx = "VectorAssembler", 0
                    for match in re.finditer(pattern, line):
                        if line.find(exclude_string, st_idx, match.span(1)[0]) == -1:
                            indexes.append(match.span(1))
                        st_idx = match.span(1)[1]
                    for start_index, end_index in reversed(indexes):
                        line = "".join([line[:start_index], "\"<Specify list of column names>\"", line[end_index:]])
                    actual_lines[idx - 1] = line

        # When neither of this values present
        # Example:  dt = DecisionTreeRegressor(maxDepth=2)
        # dt.setVarianceCol("variance")
        # model = dt.fit(df)
        # then we dont make change in script but in html.
        function_names = []
        for idx, line in enumerate(actual_lines):
            for key, values in functions_with_default_values.items():
                start_index = 0
                end_index = -1
                if ''.join([key, '(']) in line and values[0] not in line and values[1] not in line:
                    start_index = idx
                    i = idx
                    while i in range(idx, len(actual_lines)):
                        if values[0] in actual_lines[i] or values[1] in actual_lines[i]:
                            break
                        if 'fit' in actual_lines[i]:
                            end_index = i
                            break
                        i+=1
                if end_index != -1:
                    function_names.append((key, start_index))

        # Write the new file
        with open(self.__get_new_file_name(), 'w') as fw:
            fw.writelines(actual_lines)

        # Html updates when this arguments ['setInputCol', 'setInputCols', 'setFeaturesCol',
        # 'inputCol', 'inputCols', 'featuresCol'] are present.
        for start_line_number, end_line_number, keyword in store_line_number:
            user_guide.add_notes(UserNotes(start_line_number, end_line_number, keyword,
                                           "Replace following string `Specify list of column names` with list of column names manually",
                                            UserNoteType.PARTIALLY_SUPPORTED))
        # Html updates when this arguments ['setInputCol', 'setInputCols', 'setFeaturesCol',
        # 'inputCol', 'inputCols', 'featuresCol'] are not present.
        for keyword, start_line in function_names:
            # read the files using 'open' starts with '0' but in files it should be shown from '1'.
            user_guide.add_notes(UserNotes(start_line+1, start_line+1, keyword,
                                           f"Both `featuresCol` and `setfeaturesCol` not used hence default value to `features` will not work. Either use `featuresCol` or `setfeaturesCol` and provide list of columns",
                                           UserNoteType.PARTIALLY_SUPPORTED))


    def convert(self):

        # First convert the file.
        new_file_path = self.__replace_pyspark_with_tdmlspk()

        with open(new_file_path) as fp:
            root_node = ast.parse(fp.read())

        invalid_imports = self.__get_invalid_imports(root_node)

        # Segregate invalid imports according to line no's.
        invalid_imports = self.__segregate_invalid_imports_based_on_line_no(invalid_imports)

        new_lines = self.__remove_invalid_imports(invalid_imports)

        with open(new_file_path) as fp:
            root_node = ast.parse(fp.read())
        # Store line number of script where this arguments are present
        # ['setInputCol', 'setInputCols', 'setFeaturesCol', 'inputCol', 'inputCols', 'featuresCol']
        store_line_number = []
        # Recurse every line of script
        for x in root_node.body:
            self.__recurse_node(x, 0, 0, store_line_number)

        # Prepare user guide.
        user_guide = UserGuide(self.__file_path)
        # Change the lines based on 'store_line_number'
        self.__change_input_cols(store_line_number, user_guide)

        print("Python script '{}' converted to '{}' successfully.".format(self.__file_path, new_file_path))


        # Store the invalid import statement along with line numbers.
        # This will be helpfull for preparing the user notes for the
        # lines which use these invalid imports.
        invalid_import_stmts = {}

        # First prepare the notes for invalid imports.
        # We got the invalid import statements. Get user guide and string to
        # replace the lines.
        for start_line_no, end_line_no in invalid_imports:
            for py_obj in invalid_imports[(start_line_no, end_line_no)]:
                invalid_import_ = py_obj.invalid_import
                notes_ = self.__unimplemented_imports.get(invalid_import_)
                notes_ = notes_ + "<span style='font-style: italic;'> Import is ignored. </span>"
                user_guide.add_notes(UserNotes(start_line_no, end_line_no, invalid_import_, notes_, UserNoteType.NO_ACTION))

                alias_name = py_obj.alias_name
                invalid_import_stmts[alias_name if alias_name else invalid_import_] = (start_line_no, end_line_no)

        # Now parse the new file and get the notes for other functions or keywords.
        with open(new_file_path) as fp:
            root_node = ast.walk(ast.parse(fp.read()))

        for node in root_node:
            keyword, st_line, end_line = self.__get_node_details(node)
            if keyword in self.__not_supported:
                notes_ = self.__not_supported.get(keyword)
                user_guide.add_notes(UserNotes(st_line, end_line, keyword, notes_, UserNoteType.NOT_SUPPORTED))
                
            elif keyword in self.__partially_supported:

                notes_ = self.__partially_supported.get(keyword)
                user_guide.add_notes(UserNotes(st_line, end_line, keyword, notes_, UserNoteType.PARTIALLY_SUPPORTED))

            elif keyword in self.__notification:
                notes_ = self.__notification.get(keyword)
                user_guide.add_notes(UserNotes(
                    st_line, end_line, keyword, notes_, UserNoteType.NO_ACTION))

        user_guide.publish(path=self.__get_new_file_name("html"))

def pyspark2teradataml(file_path):
    """Utility which analyses and produces the script to run on Teradata Vantage. """
    _pyspark2teradatamlspk(file_path).convert()