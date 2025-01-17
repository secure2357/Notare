# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

from flask import request, g

from . import Resource
from .. import schemas
from flask_jwt_extended import jwt_required, get_jwt_identity


import sqlite3


class Tags(Resource):
    @jwt_required
    def get(self):

        data = []
        query_ops = ""
        for query_param in ["user_id", "tag"]:
            if query_param in g.args:
                if query_ops == "":
                    query_ops = f"WHERE {query_param}=?"
                    data.append(g.args[query_param])
                else:
                    query_ops += f" and {query_param}=?"
                    data.append(g.args[query_param])

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        SQL = f"SELECT * FROM tags {query_ops};"
        c.execute(SQL, tuple(data))
        tags_entries = c.fetchall()
        conn.close()

        response = {
            "tags": [{"user_id": entry[1], "tag": entry[2]} for entry in tags_entries],
            "num_tags": len(tags_entries),
        }

        return response, 200, None

    @jwt_required
    def post(self):

        for param in ["tag", "user_id"]:
            if param not in g.json:
                return {"errorMessage": f"param {param} not in body"}, 400

        # check if tag already created by user
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        SQL = f"SELECT * FROM tags where user_id=? and tag=?;"
        c.execute(SQL, (g.json["user_id"], g.json["tag"]))
        tags_entries = c.fetchall()
        conn.close()
        if len(tags_entries) != 0:
            return (
                {
                    "errorMessage": f"tag {g.json['tag']} already exists for user {g.json['user_id']}"
                },
                400,
            )

        # create tag
        SQL = f"INSERT INTO tags (user_id, tag) values (?,?)"
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(SQL, (g.json["user_id"], g.json["tag"]))
        conn.commit()

        response = {"tag": {"tag": g.json["tag"], "user_id": g.json["user_id"]}}

        return response, 200, None

    @jwt_required
    def delete(self):

        for param in ["tag", "user_id"]:
            if param not in g.json:
                return {"errorMessage": f"param {param} not in body"}, 400

        # check if tag already created by user
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        SQL = f"SELECT * FROM tags where user_id=? and tag=?;"
        c.execute(SQL, (g.json["user_id"], g.json["tag"]))
        tags_entries = c.fetchall()
        conn.close()
        if len(tags_entries) == 0:
            return (
                {
                    "errorMessage": f"category {g.json['tag']} doesn't exist for user {g.json['user_id']}"
                },
                400,
            )

        tag_id = tags_entries[0][0]
        # delete tag
        SQL = f"DELETE FROM tags WHERE id=?;"
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(SQL, (tag_id,))
        conn.commit()

        # Set all videos that have that tag id for the user to 0 aka No Tag
        SQL = f"UPDATE videos SET categories=? WHERE categories=? and user_id=?;"
        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute(SQL, (0, g.json["tag"], g.json["user_id"]))
        conn.commit()

        response = {}

        return response, 200, None
