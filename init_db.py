import sqlite3
import random


def fill_table(s_table_name, i_fields_amount, i_records_amount):
	names = []
	for field in xrange(0, i_records_amount):
		values = [value + random.randint(0, 100) for value in xrange(0, i_fields_amount)]
		name = '{0}-{1}'.format(s_table_name[:-1], str(field))
		names.append(name)
		sql = 'INSERT INTO {0} VALUES({1})'.format(s_table_name, ('?,' * (i_fields_amount + 1))[:-1])
		cur.execute(sql, [name] + values)
	return names


if __name__ == "__main__":
	conn = sqlite3.connect('database.db')
	cur = conn.cursor()

	cur.executescript("""
			CREATE TABLE "weapons" (
				`weapon`	TEXT NOT NULL,
				`reload speed`	INTEGER NOT NULL,
				`rotational speed`	INTEGER NOT NULL,
				`diameter`	INTEGER NOT NULL,
				`power volley`	INTEGER NOT NULL,
				`count`	INTEGER NOT NULL,
				PRIMARY KEY(weapon)
			);
			CREATE TABLE "hulls" (
				`hull`	TEXT NOT NULL,
				`armor`	INTEGER NOT NULL,
				`type`	INTEGER NOT NULL,
				`capacity`	INTEGER NOT NULL,
				PRIMARY KEY(hull)
			);
			CREATE TABLE "engines" (
				`engine`	TEXT NOT NULL,
				`power`	INTEGER NOT NULL,
				`type`	INTEGER NOT NULL,
				PRIMARY KEY(engine)
			);
			CREATE TABLE "ships" (
				`ship`	TEXT NOT NULL,
				`weapon`	TEXT NOT NULL,
				`hull`	TEXT NOT NULL,
				`engine`	TEXT NOT NULL,
				PRIMARY KEY(ship),
				FOREIGN KEY(`weapon`) REFERENCES weapons ( weapon ),
				FOREIGN KEY(`hull`) REFERENCES hulls ( hull ),
				FOREIGN KEY(`engine`) REFERENCES engines ( engine )
			)
		""")
	conn.commit()

	weapons = fill_table('weapons', 5, 20)
	hulls = fill_table('hulls', 3, 5)
	engines = fill_table('engines', 2, 6)

	for i in xrange(0, 200):
		ship = 'ship-{0}'.format(str(i))
		weapon = random.choice(weapons)
		hull = random.choice(hulls)
		engine = random.choice(engines)
		cur.execute('INSERT INTO ships VALUES(?,?,?,?)', (ship, weapon, hull, engine))

	conn.commit()