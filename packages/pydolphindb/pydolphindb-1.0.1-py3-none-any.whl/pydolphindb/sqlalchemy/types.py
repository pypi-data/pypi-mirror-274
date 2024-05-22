import sqlalchemy.types as sqltypes
from sqlalchemy.sql import operators, expression
from sqlalchemy.sql import default_comparator

class DDBString(sqltypes.String):
    __visit_name__ = "DDBString"
    def literal_processor(self, dialect):
        def process(value):
            return '"%s"' % value

        return process