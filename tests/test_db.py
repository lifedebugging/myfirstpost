import os
import sqlite3
import threading
import tempfile
import pytest
import sys

sys.path.append("/home/user/Documents/Assignment/Perosnal_Finance_Tracker_Project")
from models import User
from db import get_db_connection

class TestGetDbConnection:
    def test_get_db_connection_returns_valid_connection(self):
        conn = get_db_connection()
        assert isinstance(conn, sqlite3.Connection)
        conn.close()

    def test_get_db_connection_creates_db_if_missing(self, tmp_path):
        db_path = tmp_path / "finance_tracker.db"
        # Change working directory so the db file is created in tmp_path
        orig_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            assert not db_path.exists()
            conn = get_db_connection()
            conn.close()
            assert db_path.exists()
        finally:
            os.chdir(orig_cwd)

    def test_get_db_connection_allows_sql_execution(self, tmp_path):
        db_path = tmp_path / "finance_tracker.db"
        orig_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("CREATE TABLE test (id INTEGER PRIMARY KEY, name TEXT)")
            cursor.execute("INSERT INTO test (name) VALUES (?)", ("Alice",))
            conn.commit()
            cursor.execute("SELECT name FROM test WHERE id=1")
            result = cursor.fetchone()
            assert result[0] == "Alice"
            conn.close()
        finally:
            os.chdir(orig_cwd)

    def test_get_db_connection_invalid_path_raises_exception(self, monkeypatch):
        def raise_operational_error(path):
            raise sqlite3.OperationalError("unable to open database file")
        monkeypatch.setattr(sqlite3, "connect", raise_operational_error)
        with pytest.raises(sqlite3.OperationalError, match="unable to open database file"):
            get_db_connection()

    def test_get_db_connection_concurrent_access(self, tmp_path):
        orig_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            results = []
            exceptions = []

            def worker():
                try:
                    conn = get_db_connection()
                    results.append(isinstance(conn, sqlite3.Connection))
                    conn.close()
                except Exception as e:
                    exceptions.append(e)

            threads = [threading.Thread(target=worker) for _ in range(5)]
            for t in threads:
                t.start()
            for t in threads:
                t.join()

            assert all(results)
            assert not exceptions
        finally:
            os.chdir(orig_cwd)

    def test_get_db_connection_corrupted_db_file(self, tmp_path):
        db_path = tmp_path / "finance_tracker.db"
        # Write invalid data to simulate corruption
        with open(db_path, "wb") as f:
            f.write(b"not a sqlite database")
        orig_cwd = os.getcwd()
        os.chdir(tmp_path)
        try:
            conn = get_db_connection()
            with pytest.raises(sqlite3.DatabaseError):
                conn.execute("SELECT * FROM sqlite_master")
            conn.close()
        finally:
            os.chdir(orig_cwd)
