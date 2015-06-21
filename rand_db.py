import sqlite3
import random


class Database():
	def __init__(self, s_name_db):
		self.__conn = sqlite3.connect(s_name_db)
		self.__cur = self.__conn.cursor()

	def randomize(self):
		table_names = ('ships', 'weapons', 'hulls', 'engines')
		for table_name in table_names:
			for row in self.__generator(table_name):
				sql = 'REPLACE INTO {0} VALUES({1})'.format(table_name, ('?,' * len(row))[:-1])
				self.__cur.execute(sql, row)
		self.__conn.commit()
		self.__cur.close()

	def __generator(self, s_table_name):
		self.__cur.execute('SELECT * FROM {0}'.format(s_table_name))
		table_dump = self.__cur.fetchall()
		for row in table_dump:
			l_row = list(row)
			if random.randint(0, 1):
				for i in xrange(1, len(l_row)):
					if random.randint(0, 1):
						if type(l_row[i]) is int:
							l_row[i] += random.randint(1, 100)
						else:
							l_row[i] = table_dump[random.randint(0, len(table_dump) - 1)][i]
			yield l_row


if __name__ == "__main__":
	Database('database.db').randomize()