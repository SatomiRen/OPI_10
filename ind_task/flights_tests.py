#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import unittest
import flights
import sqlite3
import os
from random import choice, randint
from string import ascii_lowercase, digits, ascii_uppercase


class FlightsTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up for class"""

        print("setUpClass")
        print("==========")

    @classmethod
    def tearDownClass(cls):
        """Tear down for class"""
        print("==========")
        print("tearDownClass")

    def setUp(self):
        """Set up for test"""
        print("Set up for [" + self.shortDescription() + "]")
        print("Creating the test DB...")

    def tearDown(self):
        """Tear down for test"""
        print("Tear down for [" + self.shortDescription() + "]")
        os.remove('test_db.db')
        print("The test DB has been deleted")

    def test_select_all(self):
        """The whole selection test"""
        conn = sqlite3.connect('test_db.db')
        cursor = conn.cursor()
        cursor.execute(
            """  
          CREATE TABLE IF NOT EXISTS flight_numbers (
              num_id INTEGER PRIMARY KEY AUTOINCREMENT,
              num_title TEXT NOT NULL
              )
            """
        )
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS flights (
            flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_destination TEXT NOT NULL,
            num_id INTEGER NOT NULL,
            airplane_type TEXT NOT NULL,
            FOREIGN KEY(num_id) REFERENCES flight_numbers(num_id)
            )
            """
        )
        db_list = []
        num_of_records = randint(2, 10)
        print(f"Number of records in test DB: {num_of_records}")
        for _ in range(num_of_records):
            ar_types = ('Military', 'Passenger', 'Sanitary')
            letters = ascii_lowercase
            num_let = ascii_uppercase
            length = randint(1, 10)
            dest = ''.join(choice(letters) for i in range(length))
            num = ''.join(choice(num_let) for i in range(2)) + ''.join(
                choice(digits) for i in range(3))
            ar_type = choice(ar_types)
            ans = {
                'flight_destination': dest,
                'flight_number': num,
                'airplane_type': ar_type
            }
            print(ans)
            db_list.append(ans)
            # flights.add_flight('test_db.db', dest, num, ar_type)
            # conn = sqlite3.connect(database_path)
            # conn = sqlite3.connect('test_db.db')
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT num_id FROM flight_numbers WHERE num_title = ?
                """,
                (num,)
            )
            row = cursor.fetchone()
            if row is None:
                cursor.execute(
                    """
                    INSERT INTO flight_numbers (num_title) VALUES (?)
                    """,
                    (num,)
                )
                num_id = cursor.lastrowid
            else:
                num_id = row[0]
            cursor.execute(
                """
                INSERT INTO flights (flight_destination, num_id, airplane_type)
                VALUES (?, ?, ?)
                """,
                (dest, num_id, ar_type)
            )
            conn.commit()
            self.assertListEqual(flights.select_all('test_db.db'), db_list)
        conn.close()

    def test_select_by_type(self):
        """Selection test"""
        conn = sqlite3.connect('test_db.db')
        cursor = conn.cursor()
        cursor.execute(
            """  
          CREATE TABLE IF NOT EXISTS flight_numbers (
              num_id INTEGER PRIMARY KEY AUTOINCREMENT,
              num_title TEXT NOT NULL
              )
            """
        )
        cursor.execute(
            """
        CREATE TABLE IF NOT EXISTS flights (
            flight_id INTEGER PRIMARY KEY AUTOINCREMENT,
            flight_destination TEXT NOT NULL,
            num_id INTEGER NOT NULL,
            airplane_type TEXT NOT NULL,
            FOREIGN KEY(num_id) REFERENCES flight_numbers(num_id)
            )
            """
        )
        ar_types = ('Military', 'Passenger', 'Sanitary')
        letters = ascii_lowercase
        num_let = ascii_uppercase
        length = randint(1, 10)
        dest = ''.join(choice(letters) for i in range(length))
        num = ''.join(choice(num_let) for i in range(2)) + ''.join(
            choice(digits) for i in range(3))
        ar_type = choice(ar_types)
        print(f"dest {dest}, num {num}, type {ar_type}")
        cursor.execute(
            """
            SELECT num_id FROM flight_numbers WHERE num_title = ?
            """,
            (num,)
        )
        row = cursor.fetchone()
        if row is None:
            cursor.execute(
                """
                INSERT INTO flight_numbers (num_title) VALUES (?)
                """,
                (num,)
            )
            num_id = cursor.lastrowid
        else:
            num_id = row[0]
        cursor.execute(
            """
            INSERT INTO flights (flight_destination, num_id, airplane_type)
            VALUES (?, ?, ?)
            """,
            (dest, num_id, ar_type)
        )
        conn.commit()
        ans = [
            {
                'flight_destination': dest,
                'flight_number': num,
                'airplane_type': ar_type
            }
        ]
        print(ans)
        self.assertListEqual(
            flights.select_flights('test_db.db', ar_type), ans
        )
        conn.close()
