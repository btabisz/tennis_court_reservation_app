import csv
from datetime import timedelta
import json
from reservations import Reservations


class Save:
    def __init__(self):
        self.reservations = Reservations()

    def save_to_csv(self, save_start_date, save_end_date, file_name):
        conn = self.reservations.create_connection_db()
        cur = conn.cursor()
        with open(f'{file_name}.csv', 'w', encoding='utf-8', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['name', 'start_time', 'end_time'])
            cur.execute("SELECT name, strftime('%d.%m.%Y %H:%M', start_time), strftime('%d.%m.%Y %H:%M', end_time) "
                        "FROM reservations WHERE date(start_time)>=?"
                        "AND date(start_time)<=? ORDER BY start_time", (save_start_date.date(), save_end_date.date()))
            rows = cur.fetchall()
            for row in rows:
                csvwriter.writerow((row[0], row[1], row[2]))
        conn.close()

    def save_to_json(self, save_start_date, save_end_date, file_name):
        schedule_dict = {}
        schedule_list = []
        conn = self.reservations.create_connection_db()
        cur = conn.cursor()
        save_date = save_start_date
        while save_date <= save_end_date:
            cur.execute("SELECT name, time(start_time), time(end_time) FROM reservations WHERE date(start_time)=? "
                        "ORDER BY start_time", (save_date.date(),))
            rows = cur.fetchall()
            if len(rows) > 0:
                for row in rows:
                    schedule_list.append({"name": row[0], "start_time": row[1][0:5], "end_time": row[2][0:5]})
                schedule_dict[save_date.strftime('%d.%m')] = schedule_list
                schedule_list = []
            else:
                schedule_dict[save_date.strftime('%d.%m')] = []
            save_date += timedelta(days=1)
        conn.close()

        with open(f'{file_name}.json', 'w', encoding="utf-8") as jsonfile:
            json.dump(schedule_dict, jsonfile, ensure_ascii=False, indent=0)
