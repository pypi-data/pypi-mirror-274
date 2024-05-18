# This code is based on code from Apache Spark under the license found in the LICENSE file located in the 'dataframe' folder.

from __future__ import annotations

import logging
import typing as t

from sqlframe.base.readerwriter import _BaseDataFrameReader, _BaseDataFrameWriter
from sqlframe.base.util import ensure_column_mapping, to_csv

if t.TYPE_CHECKING:
    from sqlframe.base._typing import OptionalPrimitiveType, PathOrPaths
    from sqlframe.base.types import StructType
    from sqlframe.duckdb.dataframe import DuckDBDataFrame
    from sqlframe.duckdb.session import DuckDBSession  # noqa

logger = logging.getLogger(__name__)


class DuckDBDataFrameReader(_BaseDataFrameReader["DuckDBSession", "DuckDBDataFrame"]):
    def load(
        self,
        path: t.Optional[PathOrPaths] = None,
        format: t.Optional[str] = None,
        schema: t.Optional[t.Union[StructType, str]] = None,
        **options: OptionalPrimitiveType,
    ) -> DuckDBDataFrame:
        """Loads data from a data source and returns it as a :class:`DataFrame`.

        .. versionadded:: 1.4.0

        .. versionchanged:: 3.4.0
            Supports Spark Connect.

        Parameters
        ----------
        path : str or list, t.Optional
            t.Optional string or a list of string for file-system backed data sources.
        format : str, t.Optional
            t.Optional string for format of the data source. Default to 'parquet'.
        schema : :class:`pyspark.sql.types.StructType` or str, t.Optional
            t.Optional :class:`pyspark.sql.types.StructType` for the input schema
            or a DDL-formatted string (For example ``col0 INT, col1 DOUBLE``).
        **options : dict
            all other string options

        Examples
        --------
        Load a CSV file with format, schema and options specified.

        >>> import tempfile
        >>> with tempfile.TemporaryDirectory() as d:
        ...     # Write a DataFrame into a CSV file with a header
        ...     df = spark.createDataFrame([{"age": 100, "name": "Hyukjin Kwon"}])
        ...     df.write.option("header", True).mode("overwrite").format("csv").save(d)
        ...
        ...     # Read the CSV file as a DataFrame with 'nullValue' option set to 'Hyukjin Kwon',
        ...     # and 'header' option set to `True`.
        ...     df = spark.read.load(
        ...         d, schema=df.schema, format="csv", nullValue="Hyukjin Kwon", header=True)
        ...     df.printSchema()
        ...     df.show()
        root
         |-- age: long (nullable = true)
         |-- name: string (nullable = true)
        +---+----+
        |age|name|
        +---+----+
        |100|NULL|
        +---+----+
        """
        if format:
            sql = f"SELECT * FROM read_{format}('{path}', {to_csv(options)})"
        else:
            sql = f"select * from '{path}'"
        df = self.session.sql(sql)
        if schema:
            df = df.select(*self._to_casted_columns(ensure_column_mapping(schema)))
        self.session._last_loaded_file = path  # type: ignore
        return df


class DuckDBDataFrameWriter(_BaseDataFrameWriter["DuckDBSession", "DuckDBDataFrame"]):
    def _write(self, path: str, mode: t.Optional[str], **options):  # type: ignore
        mode, skip = self._validate_mode(path, mode)
        if skip:
            return
        if mode == "append":
            raise NotImplementedError("Append mode not supported")
        options = to_csv(options, equality_char=" ")
        sqls = self._df.sql(pretty=False, optimize=False, as_list=True)
        for i, sql in enumerate(sqls):
            if i < len(sqls) - 1:
                self._df.session._fetch_rows(sql)
            else:
                self._df.session._fetch_rows(f"COPY ({sqls[0]}) TO '{path}' ({options})")
