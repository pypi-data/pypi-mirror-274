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
from sqlalchemy import func, literal_column, literal
from teradatamlspk.sql.column import Column
from teradataml.dataframe.sql import _SQLColumnExpression
from teradatasqlalchemy.types import INTEGER, DATE, FLOAT, NUMBER

# Suppressing the Validation in teradataml.
# Suppress the validation. PySpark accepts the columns in the form of a
# standalone Columns, i.e.,
# >>> from PySpark.sql.functions import col, sum
# >>> column_1 = col('x')
# >>> column_2 = col('y')
# >>> df.withColumn('new_column', sum(column1+column2).over(WindowSpec)
# Note that the above expression accepts Columns which are not bounded to
# any table. Since compilation is at run time in PySpark, if columns does not exist,
# the expression fails - BUT AT RUN TIME. On the other side, teradataml
# validates every thing before running it. To enable this behaviour,
# we are suppressing the validation.
from teradataml.common.utils import _Validators
from teradataml.dataframe.sql_functions import to_numeric
_Validators.skip_all = True
from sqlalchemy import literal_column, func, case, literal

_get_sqlalchemy_expr = lambda col: literal_column(col) if isinstance(col, str) else literal(col)
_get_tdml_col = lambda col: _SQLColumnExpression(_get_sqlalchemy_expr(col)) if isinstance(col, (str, int, float)) else col._tdml_column


col = lambda col: Column(tdml_column=_SQLColumnExpression(col))

column = lambda col: Column(tdml_column=_SQLColumnExpression(col))
lit = lambda col: Column(tdml_column=_SQLColumnExpression(literal(col)))
broadcast = lambda df: df
def coalesce(*cols):

    # cols can be a name of column or ColumnExpression. Prepare tdml column first.
    cols = [_SQLColumnExpression(col).expression if isinstance(col, str) else col._tdml_column.expression for col in cols]
    return Column(tdml_column=_SQLColumnExpression(func.coalesce(*cols)))

def input_file_name():
    raise NotImplementedError

isnan = lambda col: Column(tdml_column=(_SQLColumnExpression(col) if isinstance(col, str) else col._tdml_column).isna())
isnull = lambda col: Column(tdml_column=(_SQLColumnExpression(col) if isinstance(col, str) else col._tdml_column).isna())
monotonically_increasing_id = lambda : Column(tdml_column=_SQLColumnExpression('sum(1) over( rows unbounded preceding )'))
def named_struct(*cols):
    raise NotImplementedError
nanvl = lambda col1, col2: Column(tdml_column=_SQLColumnExpression(func.nvl(_get_tdml_col(col1).expression, _get_tdml_col(col2).expression)))
rand = lambda seed=0: Column(tdml_column=_SQLColumnExpression("cast(random(0,999999999) as float)/1000000000 (format '9.999999999')"))
randn = lambda seed=0: Column(tdml_column=_SQLColumnExpression("cast(random(0,999999999) as float)/1000000000 (format '9.999999999')"))
spark_partition_id = lambda: Column(tdml_column=_SQLColumnExpression("0"))
when = lambda condition, value: Column(tdml_column=_SQLColumnExpression(case((_get_tdml_col(condition).expression, value._tdml_column.expression if isinstance(value, Column) else value))))
bitwise_not = lambda col: Column(tdml_column=col._tdml_column.bitwise_not() if isinstance(col, Column) else _SQLColumnExpression(col).bitwise_not())
bitwiseNOT = lambda col: Column(tdml_column=col._tdml_column.bitwise_not() if isinstance(col, Column) else _SQLColumnExpression(col).bitwise_not())
expr = lambda str: Column(tdml_column=_SQLColumnExpression(str))
greatest = lambda *cols: Column(tdml_column=_get_tdml_col(cols[0]).greatest(*[_get_tdml_col(col) for col in cols[1:]]))
least = lambda *cols: Column(tdml_column=_get_tdml_col(cols[0]).least(*[_get_tdml_col(col) for col in cols[1:]]))
sqrt = lambda col: Column(tdml_column=_get_tdml_col(col).sqrt())
abs = lambda col: Column(tdml_column=_get_tdml_col(col).abs())
acos = lambda col: Column(tdml_column=_get_tdml_col(col).acos())
asin = lambda col: Column(tdml_column=_get_tdml_col(col).asin())
asinh = lambda col: Column(tdml_column=_get_tdml_col(col).asinh())
atan = lambda col: Column(tdml_column=_get_tdml_col(col).atan())
atanh = lambda col: Column(tdml_column=_get_tdml_col(col).atanh())
atan2 = lambda col1, col2: Column(tdml_column=_get_tdml_col(col2).atan2(_get_tdml_col(col1)))
bin = lambda col: Column(tdml_column=_get_tdml_col(col).to_byte().from_byte('base2'))
cbrt = lambda col: Column(tdml_column=_get_tdml_col(col).cbrt())
ceil = lambda col: Column(tdml_column=_get_tdml_col(col).ceil())
ceiling = lambda col: Column(tdml_column=_get_tdml_col(col).ceiling())
def conv(col):
    raise NotImplementedError
cos = lambda col: Column(tdml_column=_get_tdml_col(col).cos())
cosh = lambda col: Column(tdml_column=_get_tdml_col(col).cosh())
cot = lambda col: Column(tdml_column=(1/_get_tdml_col(col).tan()))
csc = lambda col: Column(tdml_column=(1/_get_tdml_col(col).sin()))
e = lambda: Column(tdml_column=_SQLColumnExpression(literal(2.718281828459045)))
exp = lambda col: Column(tdml_column=_get_tdml_col(col).exp())
expm1 = lambda col: Column(tdml_column=_get_tdml_col(col).exp()-1)
def factorial(col):
    raise NotImplementedError
floor = lambda col: Column(tdml_column=_get_tdml_col(col).floor())
hex = lambda col: Column(tdml_column=_get_tdml_col(col).floor().cast(INTEGER()).hex())
unhex = lambda col: Column(tdml_column=_get_tdml_col(col).unhex())
hypot = lambda col1, col2: Column(tdml_column=_get_tdml_col(col1).hypot(_get_tdml_col(col2)))
ln = lambda col: Column(tdml_column=_get_tdml_col(col).ln())
def log(arg1):
    raise NotImplementedError
log10 = lambda col: Column(tdml_column=_get_tdml_col(col).log10())
log1p = lambda col: Column(tdml_column=_get_tdml_col(col+1).ln())
log2 = log
negate = lambda col: Column(tdml_column=_get_tdml_col(col)*-1)
negative = lambda col: Column(tdml_column=_get_tdml_col(col)*-1)
pi = lambda: Column(tdml_column=_SQLColumnExpression(literal(3.141592653589793)))
pmod = lambda dividend, divisor: Column(tdml_column=(_get_tdml_col(dividend)) % (_get_tdml_col(divisor)))
positive = lambda col: Column(tdml_column=_get_tdml_col(col)*1)
pow = lambda col1, col2: Column(tdml_column=_get_tdml_col(col1).pow(_get_tdml_col(col2)))
power = lambda col1, col2: Column(tdml_column=_get_tdml_col(col1).pow(_get_tdml_col(col2)))
rint = lambda col: Column(tdml_column=_get_tdml_col(col).round(0))
round = lambda col, scale=0: Column(tdml_column=_get_tdml_col(col).round(scale) if scale >= 0 else _get_tdml_col(col).trunc())
bround = lambda col, scale=0: Column(tdml_column=_get_tdml_col(col).round(scale) if scale >= 0 else _get_tdml_col(col).trunc())
shiftleft = lambda col, numBits: Column(tdml_column=_get_tdml_col(col).shiftleft(numBits))
shiftright = lambda col, numBits: Column(tdml_column=_get_tdml_col(col).shiftright(numBits))
def shiftrightunsigned(col, numBits):
    raise NotImplementedError
sign = lambda col: Column(tdml_column=_SQLColumnExpression(case((_get_tdml_col(col).expression>=0, 1), else_=-1)))
signum = lambda col: Column(tdml_column=_SQLColumnExpression(case((_get_tdml_col(col).expression>=0, 1), else_=-1)))
sin = lambda col: Column(tdml_column=_get_tdml_col(col).sin())
sinh = lambda col: Column(tdml_column=_get_tdml_col(col).sinh())
tan = lambda col: Column(tdml_column=_get_tdml_col(col).tan())
tanh = lambda col: Column(tdml_column=_get_tdml_col(col).tanh())
toDegrees = lambda col: Column(tdml_column=_get_tdml_col(col).degrees())

# TODO: Ideal way is to write user defined function for all try-<arthimatic function> type functions.
try_add = lambda left, right: Column(tdml_column=_get_tdml_col(left) + _get_tdml_col(right))
try_avg = lambda col: Column(tdml_column=_get_tdml_col(col).avg())
try_divide = lambda left, right: Column(tdml_column=_get_tdml_col(left) / _get_tdml_col(right))
try_multiply = lambda left, right: Column(tdml_column=_get_tdml_col(left) * _get_tdml_col(right))
try_subtract = lambda left, right: Column(tdml_column=_get_tdml_col(left) - _get_tdml_col(right))
try_sum = lambda left: Column(tdml_column=_get_tdml_col(left).sum())

try_to_number = lambda col, format=None: Column(tdml_column=to_numeric(_get_tdml_col(col), format_ = format))
degrees = toDegrees
toRadians = lambda col: Column(tdml_column=_get_tdml_col(col).radians())
radians = toRadians
width_bucket = lambda v, min, max, numBucket: Column(tdml_column=_SQLColumnExpression(func.width_bucket(
    _get_tdml_col(v).expression, _get_tdml_col(min).expression, _get_tdml_col(max).expression, _get_tdml_col(numBucket).expression)))
add_months = lambda start, months: Column(tdml_column=_get_tdml_col(start).add_months(_get_tdml_col(months)))
def not_implemented(*args, **kwargs):
    raise NotImplementedError
def unknown(*args, **kwargs):
    raise NotImplementedError
convert_timezone = not_implemented
curdate = lambda : Column(tdml_column=_SQLColumnExpression(func.CURRENT_DATE()))
current_date = lambda : Column(tdml_column=_SQLColumnExpression(func.CURRENT_DATE()))
current_timestamp = lambda : Column(tdml_column=_SQLColumnExpression(func.CURRENT_TIMESTAMP()))
current_timezone = not_implemented
date_add = lambda start, days: Column(tdml_column=_SQLColumnExpression(literal_column("({}) + (nvl({}, 0)  * interval '1' DAY)".format(_get_tdml_col(start).compile(), _get_tdml_col(days).compile()))))
date_diff = lambda end, start: Column(tdml_column=_get_tdml_col(end) - _get_tdml_col(start))
date_format = lambda date, format: Column(tdml_column=_get_tdml_col(date).to_char(format))
date_from_unix_date = unknown
date_trunc = lambda format, timestamp: Column(tdml_column=_get_tdml_col(timestamp).trunc(formatter=format))
dateadd = date_add
datediff = date_diff
day = lambda col: Column(tdml_column=_get_tdml_col(col).day_of_month())
date_part = unknown
datepart = date_part
dayofmonth = lambda col: Column(tdml_column=_get_tdml_col(col).day_of_month())
dayofweek = lambda col: Column(tdml_column=_get_tdml_col(col).day_of_week())
dayofyear = lambda col: Column(tdml_column=_get_tdml_col(col).day_of_year())
extract = unknown
second = lambda col: Column(tdml_column=_get_tdml_col(col).second())
weekofyear = lambda col: Column(tdml_column=_get_tdml_col(col).week_of_year()+1)
year = lambda col: Column(tdml_column=_get_tdml_col(col).year())
quarter = lambda col: Column(tdml_column=_get_tdml_col(col).quarter_of_year())
month = lambda col: Column(tdml_column=_get_tdml_col(col).month_of_year())
last_day = lambda col: Column(tdml_column=_get_tdml_col(col).month_end())
localtimestamp = lambda: Column(tdml_column=_SQLColumnExpression(literal_column('CURRENT_TIMESTAMP AT LOCAL')))
make_dt_interval = unknown
make_interval = unknown
make_timestamp = unknown
make_timestamp_ltz = unknown
make_timestamp_ntz = unknown
make_ym_interval = unknown
minute = lambda col: Column(tdml_column=_get_tdml_col(col).minute())
months_between = lambda date1, date2, roundOff=True : Column(tdml_column=_get_tdml_col(date1).months_between(_get_tdml_col(date2))) \
    if not roundOff else Column(tdml_column=_get_tdml_col(date1).months_between(_get_tdml_col(date2)).round(8))
_day_names = {"Mon": "MONDAY", "Tue": "TUESDAY", "Wed": "WEDNESDAY", "Thu": "THURSDAY", "Fri": "FRIDAY", "Sat": "SATURDAY", "Sun": "SUNDAY"}
next_day = lambda date, dayOfWeek: Column(tdml_column=_get_tdml_col(date).next_day(_day_names[dayOfWeek]))
hour = lambda col: Column(tdml_column=_get_tdml_col(col).hour())
make_date = unknown
now = localtimestamp
from_unixtime = unknown
unix_timestamp = unknown
to_unix_timestamp = unknown
to_timestamp = unknown
to_timestamp_ltz = unknown
to_timestamp_ntz = unknown
to_date = lambda col, format=None: Column(tdml_column=_get_tdml_col(col).to_date(format)) if format else Column(tdml_column=_get_tdml_col(col).cast(DATE))
trunc = lambda date, format: Column(tdml_column=_get_tdml_col(date).trunc(formatter=format))
from_utc_timestamp = unknown
to_utc_timestamp = unknown
weekday = lambda col: Column(tdml_column=_get_tdml_col(col).day_of_week()-2)
window = unknown
session_window = unknown
timestamp_micros = unknown
timestamp_millis = unknown
timestamp_seconds = unknown
try_to_timestamp = unknown
unix_date = lambda col: Column(tdml_column=_SQLColumnExpression(_get_tdml_col(col).expression-func.to_date("1970-01-01", 'YYYY-MM-DD')))
unix_micros = unknown
unix_millis = unknown
unix_micros = unknown
window_time = unknown
array = not_implemented
array_contains = not_implemented
arrays_overlap = not_implemented
array_join = not_implemented
create_map = not_implemented
slice = not_implemented
concat = lambda *cols: Column(tdml_column=_get_tdml_col(cols[0]).concat("", *cols[1:]))
array_position = not_implemented
element_at = not_implemented
array_append = not_implemented
array_size = not_implemented
array_sort = not_implemented
array_insert = not_implemented
array_remove = not_implemented
array_prepend = not_implemented
array_distinct = not_implemented
array_intersect = not_implemented
array_union = not_implemented
array_except = not_implemented
array_compact = not_implemented
transform = not_implemented
exists = not_implemented
forall = not_implemented
filter = not_implemented
aggregate = not_implemented
zip_with = not_implemented
transform_keys = not_implemented
transform_values = not_implemented
map_filter = not_implemented
map_from_arrays = not_implemented
map_zip_with = not_implemented
explode = not_implemented
explode_outer = not_implemented
posexplode = not_implemented
posexplode_outer = not_implemented
inline = not_implemented
inline_outer = not_implemented
get = not_implemented
get_json_object = not_implemented
json_tuple = not_implemented
from_json = not_implemented
schema_of_json = not_implemented
to_json = not_implemented
json_array_length = not_implemented
json_object_keys = not_implemented
size = not_implemented
cardinality = not_implemented
struct = not_implemented
sort_array = not_implemented
array_max = not_implemented
array_min = not_implemented
shuffle = not_implemented
reverse = not_implemented
flatten = not_implemented
sequence = not_implemented
array_repeat = not_implemented
map_contains_key = not_implemented
map_keys = not_implemented
map_values = not_implemented
map_entries = not_implemented
map_from_entries = not_implemented
arrays_zip = not_implemented
map_concat = not_implemented
from_csv = not_implemented
schema_of_csv = not_implemented
str_to_map = not_implemented
to_csv = not_implemented
try_element_at = not_implemented
years = not_implemented
months = not_implemented
days = not_implemented
hours = not_implemented
bucket = not_implemented



def asc(col):

    # col can be a string or Column Object.
    if isinstance(col, str):
        return Column(tdml_column=_SQLColumnExpression(col).asc().nulls_first())
    return Column(tdml_column=col._tdml_column.asc().nulls_first())

asc_nulls_first = lambda col: asc(col)

def asc_nulls_last(col):
    # col can be a string or Column Object.
    if isinstance(col, str):
        return Column(tdml_column=_SQLColumnExpression(col).asc().nulls_last())
    return Column(tdml_column=col._tdml_column.asc().nulls_last())


def desc(col):

    # col can be a string or Column Object.
    if isinstance(col, str):
        return Column(tdml_column=_SQLColumnExpression(col).desc().nulls_last())
    return Column(tdml_column=col._tdml_column.desc().nulls_last())

def desc_nulls_first(col):

    # col can be a string or Column Object.
    if isinstance(col, str):
        return Column(tdml_column=_SQLColumnExpression(col).desc().nulls_first())
    return Column(tdml_column=col._tdml_column.desc().nulls_first())

desc_nulls_last = lambda col: desc(col)

def _get_agg_expr(col, func_name, **params):
    """Helper function to get aggregate function expression. """
    # Params can have teradatamlspk Column. Convert it to teradataml Column.
    params = {pname: pcol._tdml_column if isinstance(pcol, Column) else pcol for pname,pcol in params.items()}
    tdml_column = getattr(_SQLColumnExpression(col), func_name)(**params) if isinstance(col, str)\
        else getattr(col._tdml_column, func_name)(**params)
    expr_ = _SQLColumnExpression(col) if isinstance(col, str) else col._tdml_column
    agg_func_params = {"name": func_name, **params}
    return {"tdml_column": tdml_column, "expr_": expr_, "agg_func_params": agg_func_params}

avg = lambda col: Column(**_get_agg_expr(col, "mean", distinct=False))
any_value = lambda col, ignoreNulls=None: Column(**_get_agg_expr(col, "first_value"))
row_number = lambda: Column(**_get_agg_expr('col_', "row_number"))
count = lambda col: Column(**_get_agg_expr(col, "count", distinct=False))
rank = lambda: Column(**_get_agg_expr('col_', "rank"))
cume_dist = lambda: Column(**_get_agg_expr('col_', "cume_dist"))
dense_rank = lambda: Column(**_get_agg_expr('col_', "dense_rank"))
percent_rank = lambda: Column(**_get_agg_expr('col_', "percent_rank"))
max = lambda col: Column(**_get_agg_expr(col, "max", distinct=False))
mean = lambda col: Column(**_get_agg_expr(col, "mean", distinct=False))
min = lambda col: Column(**_get_agg_expr(col, "min", distinct=False))
sum = lambda col: Column(**_get_agg_expr(col, "sum", distinct=False))
std = lambda col: Column(**_get_agg_expr(col, "std", distinct=False, population=False))
stddev = std
stddev_samp = std
stddev_pop = lambda col: Column(**_get_agg_expr(col, "std", distinct=False, population=True))
var_pop = lambda col: Column(**_get_agg_expr(col, "var", distinct=False, population=True))
var_samp = lambda col: Column(**_get_agg_expr(col, "var", distinct=False, population=False))
variance = var_samp
lag = lambda col, offset=1, default=None: Column(**_get_agg_expr(col, "lag", offset_value=offset, default_expression=default))
lead = lambda col, offset=1, default=None: Column(**_get_agg_expr(col, "lead", offset_value=offset, default_expression=default))
count_distinct = lambda col: Column(**_get_agg_expr(col, "count", distinct=True))
countDistinct = count_distinct
corr = lambda col1, col2: Column(**_get_agg_expr(col1, "corr", expression=col2))
covar_pop = lambda col1, col2: Column(**_get_agg_expr(col1, "covar_pop", expression=col2))
covar_samp = lambda col1, col2: Column(**_get_agg_expr(col1, "covar_samp", expression=col2))
first = lambda col, ignorenulls=False: Column(**_get_agg_expr(col, "first_value"))
first_value = lambda col, ignorenulls=False: Column(**_get_agg_expr(col, "first_value"))
last = lambda col, ignorenulls=False: Column(**_get_agg_expr(col, "last_value"))
last_value = lambda col, ignorenulls=False: Column(**_get_agg_expr(col, "last_value"))
regr_avgx = lambda y, x: Column(**_get_agg_expr(y, "regr_avgx", expression=x))
regr_avgy = lambda y, x: Column(**_get_agg_expr(y, "regr_avgy", expression=x))
regr_count = lambda y, x: Column(**_get_agg_expr(y, "regr_count", expression=x))
regr_intercept = lambda y, x: Column(**_get_agg_expr(y, "regr_intercept", expression=x))
regr_r2 = lambda y, x: Column(**_get_agg_expr(y, "regr_r2", expression=x))
regr_slope = lambda y, x: Column(**_get_agg_expr(y, "regr_slope", expression=x))
regr_sxx = lambda y, x: Column(**_get_agg_expr(y, "regr_sxx", expression=x))
regr_sxy = lambda y, x: Column(**_get_agg_expr(y, "regr_sxy", expression=x))
regr_syy = lambda y, x: Column(**_get_agg_expr(y, "regr_syy", expression=x))
sum_distinct = lambda col: Column(**_get_agg_expr(col, "sum", distinct=True))
sumDistinct = sum_distinct

ascii = lambda col: Column(tdml_column=_get_tdml_col(col).substr(1,1).ascii())
base64 = unknown
btrim = lambda str, trim=lit(" "): Column(tdml_column=_get_tdml_col(str).trim(_get_tdml_col(trim)))
char = lambda col: Column(tdml_column=_get_tdml_col(col).char())
character_length = lambda str: Column(tdml_column=_get_tdml_col(str).character_length())
char_length = character_length
concat_ws = lambda sep, *cols: Column(tdml_column=_get_tdml_col(cols[0]).concat(sep, *cols[1:]))
contains = lambda left, right: Column(tdml_column=_get_tdml_col(left).str.contains(_get_tdml_col(right)))
decode = not_implemented
elt = unknown
encode = unknown
endswith = lambda str, suffix: Column(tdml_column=_SQLColumnExpression(case((_get_tdml_col(str).endswith(_get_tdml_col(suffix)).expression, 1), else_=0)))
find_in_set = unknown
format_number = lambda col, d: Column(tdml_column=_get_tdml_col(col).format("z"*19 if d ==0 else "z"*19+"."+"z"*d))
format_string = unknown
ilike = lambda str, pattern, escapeChar=None: Column(tdml_column=_SQLColumnExpression(case((_get_tdml_col(str).ilike(pattern).expression, 1), else_=0)))
initcap = lambda col: Column(tdml_column=_get_tdml_col(col).initcap())
instr = lambda str, substr: Column(tdml_column=_get_tdml_col(str).instr(substr, 1, 1))
lcase = lambda str: Column(tdml_column=_get_tdml_col(str).lower())
length = lambda col: Column(tdml_column=_get_tdml_col(col).length())
like = lambda str, pattern, escapeChar=None: Column(tdml_column=_SQLColumnExpression(case((_get_tdml_col(str).like(pattern).expression, 1), else_=0)))
lower = lcase
left = lambda str, len: Column(tdml_column=_get_tdml_col(str).left(_get_tdml_col(len)))
levenshtein = lambda left, right, threshold=None: Column(tdml_column=_get_tdml_col(left).edit_distance(_get_tdml_col(right)))
locate = lambda substr, str, pos = 1: Column(tdml_column=_get_tdml_col(str).instr(substr, pos))
lpad = lambda col, len, pad: Column(tdml_column=_get_tdml_col(col).lpad(len, pad))
ltrim = lambda col: Column(tdml_column=_get_tdml_col(col).ltrim())
mask = unknown
octet_length = unknown
parse_url = unknown
position = lambda substr, str, start = 1: Column(tdml_column=_get_tdml_col(str).instr(_get_tdml_col(substr), _get_tdml_col(start)))
printf = unknown
rlike = unknown
regexp = unknown
regexp_like = unknown
regexp_count = unknown
regexp_extract = unknown
regexp_extract_all = unknown
regexp_replace = lambda string, pattern, replacement: Column(tdml_column=_get_tdml_col(string).regexp_replace(pattern, replacement))
regexp_substr = lambda str, regexp: Column(tdml_column=_get_tdml_col(str).regexp_substr(regexp))
regexp_instr = lambda str, regexp, idx = 1: Column(tdml_column=_get_tdml_col(str).regexp_instr(regexp, idx))
replace = lambda src, search, replace='': Column(tdml_column=_get_tdml_col(src).oreplace(_get_tdml_col(search), _get_tdml_col(replace)))
right = lambda str, len: Column(tdml_column=_get_tdml_col(str).right(_get_tdml_col(len)))
ucase = lambda str: Column(tdml_column=_get_tdml_col(str).upper())
unbase64 = unknown
rpad = lambda col, len, pad: Column(tdml_column=_get_tdml_col(col).rpad(len, pad))
repeat = lambda col, n: Column(tdml_column=_get_tdml_col(col).concat("", *[_get_tdml_col(col) for i in range(n-1)]))
rtrim = lambda col: Column(tdml_column=_get_tdml_col(col).rtrim())
soundex = lambda col: Column(tdml_column=_get_tdml_col(col).soundex())
split = not_implemented
split_part = not_implemented
startswith = lambda str, prefix: Column(tdml_column=_SQLColumnExpression(case((_get_tdml_col(str).startswith(_get_tdml_col(prefix)).expression, 1), else_=0)))
substr = lambda str, pos, len=1:Column(tdml_column=_get_tdml_col(str).substr(pos, len))
substring = substr
substring_index = unknown
overlay = unknown
sentences = not_implemented
to_binary = unknown
to_char = lambda col, format: Column(tdml_column=_get_tdml_col(col).to_char(format))
to_number = lambda col, format: Column(tdml_column=_SQLColumnExpression(func.to_number(_get_tdml_col(col).expression, format)))
to_varchar = unknown
translate = lambda srcCol, matching, replace: Column(tdml_column=_get_tdml_col(srcCol).translate(matching, replace))
trim = lambda col: Column(tdml_column=_get_tdml_col(col).trim())
upper = lambda col: Column(tdml_column=_get_tdml_col(col).upper())
url_decode = unknown
url_encode = unknown
bit_count = unknown
bit_get = unknown
getbit = unknown
call_function = unknown
call_udf = unknown
pandas_udf = unknown
udf = unknown
udtf = unknown
unwrap_udt = unknown
aes_decrypt = unknown
aes_encrypt = unknown
bitmap_bit_position = unknown
bitmap_bucket_number = unknown
bitmap_construct_agg = unknown
bitmap_count = unknown
bitmap_or_agg = unknown
current_catalog = not_implemented
current_database = lambda : Column(tdml_column=_SQLColumnExpression(literal_column("USER")))
current_schema = lambda : Column(tdml_column=_SQLColumnExpression(literal_column("DATABASE")))
current_user = lambda : Column(tdml_column=_SQLColumnExpression(literal_column("USER")))
input_file_block_length = not_implemented
input_file_block_start = not_implemented
md5 = unknown
sha = unknown
sha1 = unknown
sha2 = unknown
crc32 = unknown
hash = unknown
xxhash64 = unknown
assert_true = unknown
raise_error = unknown
reflect = unknown
hll_sketch_estimate = unknown
hll_union = unknown
java_method = unknown
stack = unknown
try_aes_decrypt = unknown
typeof = unknown
user = lambda : Column(tdml_column=_SQLColumnExpression(literal_column("USER")))
version = unknown
equal_null = unknown
ifnull = lambda col1, col2: nanvl(col1, col2)
isnotnull = lambda col: Column(tdml_column=_get_tdml_col(col).notnull())
nullif = lambda col1, col2: Column(tdml_column=case((_get_tdml_col(col1).expression == _get_tdml_col(col2).expression, None), else_=_get_tdml_col(col1).expression))
nvl = lambda col1, col2: Column(tdml_column=_SQLColumnExpression(func.nvl(_get_tdml_col(col1).expression, _get_tdml_col(col2).expression)))
nvl2 = lambda col1, col2, col3: Column(tdml_column=_SQLColumnExpression(
    func.nvl2(_get_tdml_col(col1).expression, _get_tdml_col(col2).expression, _get_tdml_col(col3).expression)))
xpath = not_implemented
xpath_boolean = not_implemented
xpath_double = not_implemented
xpath_float = not_implemented
xpath_int = not_implemented
xpath_long = not_implemented
xpath_number = not_implemented
xpath_short = not_implemented
xpath_string = not_implemented

def time_difference(col1, col2):
    """Returns the difference between two timestamps in seconds. """
    col1 = col1 if isinstance(col1, str) else col1._tdml_column.compile()
    col2 = col2 if isinstance(col2, str) else col2._tdml_column.compile()
    s = """
    (EXTRACT(DAY FROM ({0} - {1} DAY(4) TO SECOND)) * 86400) +
    (EXTRACT(HOUR FROM ({0} - {1} DAY(4) TO SECOND)) * 3600) +
    (EXTRACT(MINUTE FROM ({0} - {1} DAY(4) TO SECOND)) * 60) +
    (EXTRACT(SECOND FROM ({0} - {1} DAY(4)TO SECOND)))
    """.format(col1, col2)
    return Column(tdml_column=_SQLColumnExpression(literal_column(s, type_=FLOAT())))