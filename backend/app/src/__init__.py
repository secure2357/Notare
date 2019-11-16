# -*- coding: utf-8 -*-
from __future__ import absolute_import

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager

import v1
import os
import sqlite3
import hashlib
notes = [                                          
    [1, "this is the note", 1, "LlW7Es7gStA", 2.5, 1573010001000000, 1573010001000000],
    [2, "this is the second note", 1, "LlW7Es7gStA", 4.5, 1573010002000000, 1573010004000000],
    [3, "different video note", 1, "QLx2WZWilBc", 1.2, 1573010003000000, 1573010003000000],
    [4, "different video differnt user note", 2, "hW_EEWVlVxE", 43.2, 1573010004000000, 1573010009000000],
    [5, "what a note", 1, "EdYT2GsBqNs", 44.5, 1573010005000000, 1573010005000000],
]

videos = [
    ["LlW7Es7gStA", 1, "Pewdiepie is nuts", "comedy", 1573010001000000, 1573010004000000],
    ["QLx2WZWilBc", 1, "United States Grand Prix", "romance", 1573010003000000, 1573010003000000],
    ["EdYT2GsBqNs", 1, "The Flash: Fastest Speedsters Ranked", "sci-fi", 1573010005000000, 1573010005000000],
    [
        "hW_EEWVlVxE",
        2,
        "Building a Roller Coaster That Goes To Hell in Planet Coaster",
        "physics",
        1573010004000000,
        1573010009000000,
    ],
]

users = [[1, "mitchellshelton97@gmail.com", hashlib.sha256("password".encode()).hexdigest()], [2, "mitchell_shelton@y7mail.com", hashlib.sha256("secret".encode()).hexdigest()]]


def create_db():
    """
    create the database
    """
    # if db file does not exist use db file
    if not os.path.isfile("./database.db"):
        try:
            print("Creating DB!")
            conn = sqlite3.connect("database.db")
            cur = conn.cursor()
            sql_command = """
            CREATE TABLE notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                note VARCHAR,
                user_id INTEGER,
                video_id VARCHAR,
                timestamp DOUBLE,
                time_created INTEGER,
                last_edited INTEGER
            );
            CREATE TABLE videos (
                id VARCHAR NOT NULL,
                user_id INTEGER,
                video_title VARCHAR,
                categories VARCHAR,
                time_created INTEGER,
                last_edited INTEGER,
                PRIMARY KEY (id)
            );
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email VARCHAR,
                password VARCHAR
            );
            CREATE TABLE blacklisted_access_tokens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                access_token VARCHAR
            );
            """
            cur.executescript(sql_command)
            conn.commit()
            for note in notes:
                cur.execute(
                    "INSERT INTO notes (id, note, user_id, video_id, timestamp, time_created, last_edited) values (?,?,?,?,?,?,?)",
                    note,
                )
            for video in videos:
                cur.execute(
                    "INSERT INTO videos (id, user_id, video_title, categories, time_created, last_edited) values (?,?,?,?,?,?)",
                    video,
                )
            for user in users:
                cur.execute("INSERT INTO users (id, email, password) values (?,?,?)", user)

            conn.commit()
            cur.execute("""SELECT * FROM notes""")
            entries = cur.fetchall()
            print(entries)
            cur.execute("""SELECT * FROM videos""")
            entries = cur.fetchall()
            print(entries)
            cur.execute("""SELECT * FROM users""")
            entries = cur.fetchall()
            print(entries)

        except sqlite3.Error as e:
            print(e)
        finally:
            conn.close()


def create_app():
    app = Flask(__name__, static_folder="static")
    app.register_blueprint(v1.bp, url_prefix="/v1")
    cors = CORS(app)
    ONE_YEAR_IN_SECONDS = 31536000
    # Setup the Flask-JWT-Extended extension
    app.config["JWT_SECRET_KEY"] = "This key is super secret"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = ONE_YEAR_IN_SECONDS
    app.config["JWT_BLACKLIST_ENABLED"] = True
    app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access"]
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token["jti"]
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        SQL = f"SELECT * FROM blacklisted_access_tokens WHERE access_token = ?;"
        c.execute(SQL, (jti,))
        entries = c.fetchall()
        conn.close()
        return False if len(entries) == 0 else True

    return app


if __name__ == "__main__":
    create_db()
    create_app().run(host="127.0.0.1", port="5000", debug=True)
