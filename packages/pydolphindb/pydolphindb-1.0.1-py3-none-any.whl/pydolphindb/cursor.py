from pandas import DataFrame
from .exceptions import ProgrammingError
import warnings
import pandas as pd
from numpy import ndarray
import numpy as np
import decimal
from typing import Optional, Tuple, List

class Cursor(object):
    """
    This is the object you use to interact with the database.

    Do not create an instance of a Cursor yourself. Call
    connections.Connection.cursor().

    See `Cursor <https://www.python.org/dev/peps/pep-0249/#cursor-objects>`_ in
    the specification.

    """

    def __init__(self, connection):
        self.connection = connection
        self.description: Optional[Tuple] = None
        self.rowcount: int = -1
        self.arraysize: int = 1
        self.rownumber:int = 0 
        self._executed: Optional[str] = None

        self._result: Optional[List]= None
        self._rows:List = []

    def close(self):
        """Close the cursor. No further scripts will be possible."""
        try:
            if self.connection is None:
                return
        finally:
            self.connection = None
            self._result = None

    def _check_executed(self):
        if not self._executed:
            raise ProgrammingError("execute() first")

    def fetchone(self):
        """Fetches a single row from the cursor. None indicates that
        no more rows are available.

        Returns:
            One result. 
            
        """
        self._check_executed()
        if self.rownumber >= len(self._rows):
            return None
        result = self._rows[self.rownumber]
        self.rownumber = self.rownumber + 1
        return result

    def fetchmany(self, size: Optional[int] = None):
        """Fetch up to size rows from the cursor. Result set may be smaller
        than size. If size is not defined, cursor.arraysize(by default is 1) is used.

        Args:
            size (int): Feche size.

        Returns:
            Size length result set.
            
        """
        self._check_executed()
        end = self.rownumber + (size or self.arraysize)
        result = self._rows[self.rownumber : end]
        self.rownumber = min(end, len(self._rows))
        return result

    def fetchall(self):
        """Fetches all available rows from the cursor.

        Returns:
            All available result set.
            
        """
        self._check_executed()
        if self.rownumber:
            result = self._rows[self.rownumber :]
        else:
            result = self._rows
        self.rownumber = len(self._rows)
        return result

    def _get_db(self):
        con = self.connection
        if con is None:
            raise ProgrammingError("cursor closed")
        return con

    def _run(self, script, db, *args, **kwargs):
        self._result = None
        self._do_get_result(script, db, *args, **kwargs)
        self._post_get_result()
        self._executed = script
        return self.rowcount

    def _get_result(self, script, db, *args, **kwargs):
        return db.run(script, *args, **kwargs)

    def _do_get_result(self, script, db, *args, **kwargs):
        self._result = self._get_result(script, db, *args, **kwargs)
        if self._result is None:
            self.description = tuple()
        else:
            description = []
            if(isinstance(self._result, DataFrame)):
                for col in self._result.columns:
                    description.append((
                        col,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        ))
            else:
                description.append((
                    "string",
                    None,
                    None,
                    None,
                    None,
                    None,
                    None))
            self.description = tuple(description)

        self.rownumber = 0

    def _DataFrame_to_list(self, df):
        result = []
        for _, row in df.iterrows():
            newrow = []
            for item in row:
                if isinstance(item, ndarray):
                    item = [x if not pd.isna(x) else None for x in list(item)]
                else:
                    if pd.isna(item):
                        item = None
                newrow.append(item)
            result.append(newrow)
        return result

    def _post_get_result(self):
        if(isinstance(self._result, DataFrame)):
            self._rows = self._DataFrame_to_list(self._result)
        elif(isinstance(self._result, list)):
            self._rows = self._result
        elif(isinstance(self._result, ndarray)):
            self._rows = [x if not pd.isna(x) else None for x in list(self._result)]
        elif(isinstance(self._result, type(None))):
            self._rows = []
        else:
            self._rows = [self._result]
        self.rowcount = len(self._rows)
        self._result = None

    def execute(self, script: str, parameters=None, *args, **kwargs) -> int:
        """Execute a script.

        Args:
            script: DolphinDB script to be executed.  
            parameters: parameter to replace %s in script. 

        Note: If args is a tuple, then %s must be used as the
        parameter placeholder in the query. If a mapping is used,

        Args:
            *args: See the DolphinDB parameter list for details.
            **kwargs: See the DolphinDB parameter list for details.

        Returns:
            Integer represents rows affected, if any.

        """
        db = self._get_db()

        if(script == "select 1"):
            script = "1+1"

        if parameters is not None:
            parameters = tuple(parameters)
            try:
                script = script % parameters
            except TypeError as m:
                raise ProgrammingError(str(m))

        assert isinstance(script, str)
        rowcount = self._run(script, db, *args, **kwargs)
        return rowcount
            
    def executemany(self, script: str, seq_of_parameters: List) -> int:
        """Execute a multi-row script.

        Args:
            script: DolphinDB script to be executed.
            seq_of_parameters: It is used as parameter.

        Returns:
            Number of rows affected, if any.

        Note:
            This method improves performance on multiple-row INSERT and
            REPLACE. Otherwise it is equivalent to looping over args with
            execute().

        """
        if not seq_of_parameters:
            raise ProgrammingError("need two parameter")

        self.rowcount = sum(self.execute(script, arg) for arg in seq_of_parameters)
        return self.rowcount

    def __iter__(self):
        warnings.warn("DB-API extension cursor.__iter__() used")
        return self

    def setinputsizes(self):
        """Not supported"""
        raise RuntimeError("This method is not supported for DolphinDB.")

    def setoutputsize(self):
        """Not supported"""
        raise RuntimeError("This method is not supported for DolphinDB.")

    def next(self):
        """Get next result set, Similar with fetchone.

        Returns:
            One row result.
            
        """
        row = self.fetchone()
        if row is None:
            raise StopIteration
        return row

    __next__ = next

