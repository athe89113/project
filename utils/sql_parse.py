# coding=utf-8
from django.utils.lru_cache import lru_cache
import sqlparse
from sqlparse.sql import IdentifierList, Identifier
from sqlparse.tokens import Keyword, DML


class SqlParse(object):

    def __init__(self, *args, **kwargs):
        pass

    def parse(self, sql, encoding=None):
        return sqlparse.parse(sql, encoding)

    def stream(self, sql):
        return sqlparse.parse(sql)[0]

    def extract_type(self, sql):
        """
        :param sql: 原始sql 语句
        :return: 返回SQL 类型
            select * from bar => SELECT
            update foo set a=1 => UPDATE
        """
        stream = self.stream(sql)
        return stream.get_type()

    def extract_tables(self, sql):
        """
        :param sql: 原始sql 语句
        :return: 返回操作涉及的表
            select * from bar => [bar]
        """
        stream = self.stream(sql)
        return list(self._extract_table_identifiers(stream))

    @lru_cache(maxsize=1024)
    def extract_type_table(self, sql):
        """
        :param sql: 原始sql 语句
        :return: 返回(SQL 类型, 操作涉及的表)
        """
        stream = self.stream(sql)
        return stream.get_type(), list(self._extract_table_identifiers(stream))

    def _is_subselect(self, parsed):
        if not parsed.is_group:
            return False
        for item in parsed.tokens:
            if item.ttype is DML and item.value.upper() == 'SELECT':
                return True
        return False

    def _extract_from_part(self, parsed):
        from_seen = False
        for item in parsed.tokens:
            if from_seen:
                if self._is_subselect(item):
                    for x in self._extract_from_part(item):
                        yield x
                elif item.ttype is Keyword:
                    raise StopIteration
                else:
                    yield item
            elif item.ttype is Keyword and item.value.upper() == 'FROM':
                from_seen = True

    def _extract_table_identifiers(self, token_stream):
        for item in token_stream:
            if isinstance(item, IdentifierList):
                for identifier in item.get_identifiers():
                    if isinstance(identifier, sqlparse.sql.Token):
                        continue
                    yield identifier.get_name().replace('`', '')
            elif isinstance(item, Identifier):
                yield item.get_name().replace('`', '')


if __name__ == '__main__':

    TEST_JOIN_SQL = 'SELECT a.runoob_id, a.runoob_author, b.runoob_count FROM runoob_tbl a INNER JOIN ' \
                    'tcount_tbl b ON a.runoob_author = b.runoob_author;'
    TEST_UPDATE_SQL = "UPDATE runoob_tbl SET runoob_title='test_title' WHERE runoob_id=3;"
    TEST_WHERE_SQL = 'SELECT a.runoob_id, a.runoob_author, b.runoob_count FROM runoob_tbl a, tcount_tbl b WHERE' \
                     ' a.runoob_author = b.runoob_author;'

    TEST_MULTIPLE_SQL = TEST_JOIN_SQL + TEST_UPDATE_SQL

    TEST_SQLS = [TEST_JOIN_SQL, TEST_UPDATE_SQL, TEST_WHERE_SQL, TEST_MULTIPLE_SQL]

    def test_all_sql():
        p = SqlParse()
        sqls = [TEST_JOIN_SQL, TEST_UPDATE_SQL, TEST_WHERE_SQL] * 1000
        for s in sqls:
            p.extract_type_table(s)

    def test():
        import timeit
        print(timeit.timeit('test_all_sql()', 'from __main__ import test_all_sql', number=1))

    test()

    parse = SqlParse()
    for test_sql in TEST_SQLS:
        sql_type, tables = parse.extract_type_table(test_sql)
        print("操作类型: {0:5}, 操作表: {1}".format(sql_type, ', '.join(tables)))
