import sqlite3


class TestDb:
    @staticmethod
    def insert_test_data():
        conn = sqlite3.connect('./db.sqlite')
        cur = conn.cursor()
        cur.execute("INSERT INTO reservations VALUES('Adam Nowak', '3023-04-13 12:00:00', '3023-04-13 13:00:00')")
        cur.execute("INSERT INTO reservations VALUES ('Szymon Kot', '3023-04-13 13:00:00', '3023-04-13 14:30:00')")
        cur.execute("INSERT INTO reservations VALUES ('Bartosz Polski', '3023-04-13 15:30:00', '3023-04-13 16:00:00')")
        cur.execute("INSERT INTO reservations VALUES ('Bartosz Polski', '3023-04-13 16:00:00', '3023-04-13 17:00:00')")
        cur.execute("INSERT INTO reservations VALUES ('Bartosz Polski', '3023-04-13 19:00:00', '3023-04-13 20:00:00')")
        cur.execute("INSERT INTO reservations VALUES ('Bartosz Polski', '3023-04-14 19:00:00', '3023-04-14 20:00:00')")
        conn.commit()
        conn.close()

    @staticmethod
    def delete_test_data():
        conn = sqlite3.connect('./db.sqlite')
        cur = conn.cursor()
        cur.execute("DELETE FROM reservations WHERE name=? and start_time=?", ('Adam Nowak', '3023-04-13 12:00:00'))
        cur.execute("DELETE FROM reservations WHERE name=? and start_time=?", ('Szymon Kot', '3023-04-13 13:00:00'))
        cur.execute("DELETE FROM reservations WHERE name=? and start_time=?", ('Bartosz Polski', '3023-04-13 15:30:00'))
        cur.execute("DELETE FROM reservations WHERE name=? and start_time=?", ('Bartosz Polski', '3023-04-13 16:00:00'))
        cur.execute("DELETE FROM reservations WHERE name=? and start_time=?", ('Bartosz Polski', '3023-04-13 19:00:00'))
        cur.execute("DELETE FROM reservations WHERE name=? and start_time=?", ('Bartosz Polski', '3023-04-14 19:00:00'))
        conn.commit()
        conn.close()
