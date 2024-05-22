from sqlalchemy import  types as sqltypes
from sqlalchemy.engine import default, reflection
from sqlalchemy import util

from .compiler import(
    DDBCompiler,
    DDBDDLCompiler,
    DDBTypeCompiler,
    DDBIdentifierPreparer,
    # DDBExecutionContext,
)
from .types import(
    DDBString,
)

ischema_names = {
    "BOOL":     sqltypes.BOOLEAN,       # bool
    "CHAR":     sqltypes.CHAR,          # int8
    "SHORT":    sqltypes.SMALLINT,      # int16
    "INT":      sqltypes.INTEGER,       # int32
    "LONG":     sqltypes.NUMERIC,       # int64
    "DATE":     sqltypes.TIMESTAMP,      # DATE
    "MONTH":    sqltypes.DATETIME,      
    "TIME":     sqltypes.TIME,
    "MINUTE":   sqltypes.TIME,
    "SECOND":   sqltypes.TIME,
    "DATETIME": sqltypes.DATETIME,
    "TIMESTAMP":    sqltypes.TIMESTAMP,
    "NANOTIME":     sqltypes.TIME,
    "NANOTIMESTAMP":sqltypes.TIMESTAMP,
    "FLOAT":    sqltypes.FLOAT,         # float32   # precision problem
    "DOUBLE":   sqltypes.DECIMAL,       # float64
    "SYMBOL":   DDBString,      # symbol
    "STRING":   DDBString,      # string
}

colspecs = {
    sqltypes.TEXT:          DDBString,
    sqltypes.UnicodeText:   DDBString,
    sqltypes.VARCHAR:       DDBString,
    sqltypes.Unicode:       DDBString,
}

class DolphinDBDialect(default.DefaultDialect):
    name = "dolphindb"
    statement_compiler = DDBCompiler
    ddl_compiler = DDBDDLCompiler
    preparer = DDBIdentifierPreparer
    type_compiler = DDBTypeCompiler

    driver = "pydolphindb"
    supports_sane_rowcount = False
    supports_sane_multi_rowcount = False
    supports_native_decimal = True

    ischema_names = ischema_names
    colspecs = colspecs

    def __init__(self, **kwargs):
        default.DefaultDialect.__init__(self, **kwargs)

    def do_execute(self, cursor, statement, parameters, context=None):
        # print("do execute >>>>>>>>>>")
        # print("statement: ", statement)
        # print("parameters: ", parameters)
        statement = statement.replace("?", "%s")
        # print("statement: ", statement)
        # print("parameters: ", parameters)
        cursor.execute(statement, parameters)

    # def do_execute(self, cursor, sql, *args, **kwargs):
    #     print("here>>>>>>>>>>")
    #     print("sql: ", sql)
    #     print("args: ", args)
    #     print("kwargs: ", kwargs)
    #     cursor.execute(sql, *args, **kwargs)

    @classmethod
    def dbapi(cls):
        return __import__("pydolphindb")
        
    # TODO: need server support `select 1` clause
    def has_table(self, connection, table_name, schema=None):
        """Return ``True`` if the given table exists"""
        if schema is not None:
            current_schema = schema
        else:
            current_schema = self.default_schema_name
        if current_schema == "shared_table":
            # tblqry = """
            #     select 1 as has_table from {}
            # """.format(table_name)
            tblqry = """
                select name from objs(shared=true) where shared=true && name=`{}
            """.format(table_name)
            result = connection.execute(tblqry)
            b = result.fetchone()
            # print("has_table: ", b)
            return b is not None
        else:
            tblqry = """
                existsTable("{}", `{})
            """.format(current_schema, table_name)
            result = connection.execute(tblqry)
            a = result.fetchone()
            # print("has_table: ", a)
            return a[0]

    @reflection.cache
    def get_table_names(self, connection, schema=None, **kw):
        # print(">>>>>>> ")
        if schema is not None:
            current_schema = schema
        else:
            current_schema = self.default_schema_name

        

        # charset = self._connection_charset
        # print("charset: ", charset)
        # print("schema: ", current_schema)

        if(current_schema=="shared_table"):
            script = """
                select name from objs(shared=true) where shared=true
            """
        else:
            script = """
                select * from (
                    select distinct(tableName) 
                    from getTabletsMeta("{}/%", "%", top=-1)
                ) order by distinct_tableName
                """.format(current_schema[5:])

        # print("script: ", script)

        rp = connection.execute(script)
        return [r[0] for r in rp]

    @reflection.cache
    def get_pk_constraint(self, connection, table_name, schema=None, **kw):
        return []

    @reflection.cache
    def get_foreign_keys(self, connection, table_name, schema=None, **kw):
        return []

    @reflection.cache
    def get_unique_constraints(self, connection, table_name,
                                schema=None, **kw):
        return []

    @reflection.cache
    def get_indexes(self, connection, table_name, schema=None, **kw):
        return []

    @reflection.cache
    def get_schema_names(self, connection, **kw):
        # cursor = connection.execute(
        #     """
        #     select * from (
        #         select distinct(tableName) 
        #         from getTabletsMeta("/%", "%", top=-1)
        #     ) order by distinct_tableName
        #     """
        # )
        cursor = connection.execute(
            """
            schema = getDFSDatabases()
            select * from table(schema) order by schema asc
            """
        )
        return ["shared_table"] + [r[0] for r in cursor]

    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        # Query to extract the details of all the fields of the given table
        if schema is not None:
            current_schema = schema
        else:
            current_schema = self.default_schema_name
        if(current_schema == "shared_table"):
            tblqry = """
                schema({})['colDefs']
            """.format(table_name)
        else:
            tblqry = """
                schema(loadTable("{}", "{}"))['colDefs']
            """.format(current_schema, table_name)
        result = connection.execute(tblqry)
        cols = []
        while True:
            row = result.fetchone()
            if row is None:
                break
            name = row['name']
            typestr = row['typeString']
            coltype = self.ischema_names.get(typestr)
            if coltype is None:
                util.warn(
                    "Did not recognize type '%s' of column '%s'"
                    % (typestr, name)
                )
                coltype = sqltypes.NULLTYPE
            else:
                coltype = coltype()
            
            # define value of this type
            defvalue = None

            col_d = {
                "name": name,
                "type": coltype,
                "nullable": False,
                "default": defvalue,
                "autoincrement": "auto",
            }

            cols.append(col_d)
        # print("get_columns: ", cols)
        return cols
