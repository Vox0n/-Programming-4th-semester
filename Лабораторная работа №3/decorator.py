import sys
import json
import sqlite3
from datetime import datetime
import functools

def trace(func=None, *, handle=sys.stderr):
    if func is None:
        return lambda func: trace(func, handle=handle)

    @functools.wraps(func)
    def inner(*args, **kwargs):
        now = datetime.now()
        params = list(map(str, args)) + [f"{k}={v}" for k, v in kwargs.items()]
        result = func(*args, **kwargs)
        log_entry = {
            "datetime": now.isoformat(),
            "func_name": func.__name__,
            "params": params,
            "result": str(result)
        }

        if handle in (sys.stdout, sys.stderr):
            handle.write(f"[{now}] Function: {func.__name__}, Params: {params}, Result: {result}\n")
        elif isinstance(handle, str) and handle.endswith(".json"):
            try:
                with open(handle, "r") as f:
                    data = json.load(f) if f.read() else []
            except (FileNotFoundError, json.JSONDecodeError):
                data = []
            data.append(log_entry)
            with open(handle, "w") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        elif isinstance(handle, sqlite3.Connection):
            cur = handle.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS logtable (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    datetime TEXT,
                    func_name TEXT,
                    params TEXT,
                    result TEXT
                )
            """)
            cur.execute("""
                INSERT INTO logtable (datetime, func_name, params, result)
                VALUES (?, ?, ?, ?)
            """, (log_entry["datetime"], log_entry["func_name"], json.dumps(log_entry["params"]), log_entry["result"]))
            handle.commit()
        return result

    return inner

def showlogs(con: sqlite3.Connection):
    """Отображает содержимое таблицы logtable из базы данных SQLite."""
    cur = con.cursor()
    cur.execute("SELECT * FROM logtable")
    for row in cur.fetchall():
        print(row)

@trace(handle=sys.stderr)
def increm(x):
    return x + 1

@trace(handle=sys.stdout)
def decrem(x):
    return x - 1

@trace(handle=sys.stdout)
def f2(x):
    return x**2

@trace(handle='logger.json')
def f3(x):
    return x**3

handle_for_f4 = sqlite3.connect(":memory:")
@trace(handle=handle_for_f4)
def f4(x):
    return x**4

# Вызываем функции
increm(2)
decrem(2)
f2(3)
f3(4)
f4(5)

# Показать логи
showlogs(handle_for_f4)
