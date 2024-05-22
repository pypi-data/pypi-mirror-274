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
from teradatasqlalchemy.types import *
from teradatamlspk.sql.types import *
TD_TO_SPARK_TYPES = {INTEGER: IntegerType,
                     SMALLINT: ShortType,
                     BIGINT: LongType,
                     DECIMAL: DecimalType,
                     BYTEINT: ByteType,
                     BYTE: ByteType,
                     VARBYTE: ByteType,
                     BLOB: BlobType,
                     FLOAT: FloatType,
                     NUMBER: NumericType,
                     DATE: DateType,
                     TIME: TimeType,
                     INTERVAL_YEAR: IntervalYearType,
                     INTERVAL_YEAR_TO_MONTH: IntervalYearToMonthType,
                     INTERVAL_MONTH: IntervalMonthType,
                     INTERVAL_DAY: IntervalDayType,
                     INTERVAL_DAY_TO_HOUR: IntervalDayToHourType,
                     INTERVAL_DAY_TO_MINUTE: IntervalDayToMinuteType,
                     INTERVAL_DAY_TO_SECOND: IntervalDayToSecondType,
                     INTERVAL_HOUR: IntervalHourType,
                     INTERVAL_HOUR_TO_MINUTE: IntervalHourToMinuteType,
                     INTERVAL_HOUR_TO_SECOND: IntervalHourToSecondType,
                     INTERVAL_MINUTE: IntervalMinuteType,
                     INTERVAL_MINUTE_TO_SECOND: IntervalMinuteToSecondType,
                     INTERVAL_SECOND: IntervalSecondType,
                     PERIOD_DATE: PeriodDateType,
                     PERIOD_TIME: PeriodTimeType,
                     PERIOD_TIMESTAMP: PeriodTimestampType,
                     CLOB: ClobType,
                     XML: XmlType,
                     JSON: JsonType,
                     GEOMETRY: GeometryType,
                     MBR: MbrType,
                     MBB: MbbType,
                     TIMESTAMP: TimestampType,
                     CHAR: CharType,
                     VARCHAR: VarcharType,
                     TDUDT: UserDefinedType}

SPARK_TO_TD_TYPES = {ByteType: BYTE,
                     FractionalType: DecimalType,
                     DoubleType: DECIMAL,
                     StringType: VARCHAR,
                     **{v:k for k,v in TD_TO_SPARK_TYPES.items() if v != ByteType}}

SQL_NAME_TO_SPARK_TYPES = { "STRING": StringType(),
                            "INTEGER" : IntegerType(),
                            "INT" : IntegerType(),
                            "REAL": FloatType(),
                            "FLOAT": FloatType(),
                            "BYTE": ByteType(),
                            "TINYINT": ByteType(),
                            "SHORT": ShortType(),
                            "SMALLINT": ShortType(),
                            "LONG": LongType(),
                            "BIGINT": LongType(),
                            "DOUBLE": DoubleType(),
                            "DATE": DateType(),
                            "TIMESTAMP": TimestampType(),
                            "TIMESTAMP_LTZ": TimestampType(),
                            "DECIMAL": DecimalType(),
                            "DEC": DecimalType(),
                            "NUMERIC": DecimalType(),
                            "INTERVAL YEAR": IntervalYearType(),
                            "INTERVAL YEAR TO MONTH": IntervalYearToMonthType(),
                            "INTERVAL MONTH": IntervalMonthType(),
                            "INTERVAL DAY": IntervalDayType(),
                            "INTERVAL DAY TO HOUR": IntervalDayToHourType(),
                            "INTERVAL DAY TO MINUTE": IntervalDayToMinuteType(),
                            "INTERVAL DAY TO SECOND": IntervalDayToSecondType(),
                            "INTERVAL HOUR": IntervalHourType(),
                            "INTERVAL HOUR TO MINUTE": IntervalHourToMinuteType(),
                            "INTERVAL HOUR TO SECOND": IntervalHourToSecondType(),
                            "INTERVAL MINUTE": IntervalMinuteType(),
                            "INTERVAL MINUTE TO SECOND": IntervalMinuteToSecondType(),
                            "INTERVAL SECOND": IntervalSecondType()
}
