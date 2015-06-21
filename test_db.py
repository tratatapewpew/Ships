import shutil
import sqlite3
import rand_db
import nose
from nose.tools import *


class Test(object):
	def __init__(self):
		self.__connects = [sqlite3.connect(name) for name in ('dump.db', 'database.db')]
		self.__cursors = [conn.cursor() for conn in self.__connects]

	@classmethod
	def setUpClass(cls):
		shutil.copyfile('database.db', 'dump.db')
		rand_db.Database('database.db').randomize()

	def test_generator(self):
		o_cur, n_cur = self.__cursors #o - origin; n - new

		table_names = o_cur.execute('SELECT name FROM sqlite_master where type="table" and name != "ships"').fetchall()
		o_ship = o_cur.execute('SELECT * FROM ships').fetchall()
		n_ship = n_cur.execute('SELECT * FROM ships').fetchall()
		for o_row, n_row in zip(o_ship, n_ship):
			o_ship_name = o_row[0]
			for o_item, n_item, table_name in zip(o_row[1:], n_row[1:], table_names):
				yield self.check_eq, o_ship_name, o_item, n_item, table_name[0]

		for conn, cur in zip(self.__connects, self.__cursors):
			conn.commit()
			cur.close()

	def check_eq(self, s_ship_name, o_value, n_value, s_value_name):
		o_cur, n_cur = self.__cursors

		eq_(o_value, n_value, '\n\t{0}, {1}\n\t\texpected {2}, was {3}'.format(s_ship_name, o_value, n_value, o_value))

		o_cur.execute('PRAGMA table_info({0})'.format(s_value_name))
		col_names = [info[1] for info in o_cur.fetchall()]

		o_params = o_cur.execute('SELECT * FROM {0} WHERE {1} = "{2}"'.format \
			                              (s_value_name, s_value_name[:-1], o_value)).fetchall()
		n_params = n_cur.execute('SELECT * FROM {0} WHERE {1} = "{2}"'.format \
			                              (s_value_name, s_value_name[:-1], n_value)).fetchall()

		result = []
		for col_name, o_param, n_param in zip(col_names, o_params[0], n_params[0]):
			if o_param != n_param:
				result.append((col_name, o_param, n_param))

		msg = '\n\t{0}, {1}\n\t\t'.format(s_ship_name, o_value)
		for r in result:
			col_name, o_param, n_param = r
			msg += '{0} : expected {1}, was {2}\n\t\t'.format(col_name, n_param, o_param)

		ok_(not result, msg)


if __name__ == '__main__':
	nose.run(defaultTest=__name__)