from pyspark.sql import Column


def get_alias(column: Column):
    try:
        return column._jc.expr().name()
    except:
        return column._jc.expr().sql()