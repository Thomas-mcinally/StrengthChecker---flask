import csv
import sqlite3

connection = sqlite3.connect("database.db")
cur = connection.cursor()

# create male_lifters table
cur.execute(
    """CREATE TABLE male_lifters(sex TEXT
                                        ,event TEXT
                                        ,equipment TEXT
                                        ,age FLOAT
                                        ,bodyweightKg FLOAT
                                        ,best3SquatKg FLOAT
                                        ,best3BenchKg FLOAT
                                        ,best3DeadliftKg FLOAT
                                        ,totalKg FLOAT
                                        ,age_bin TEXT
                                        ,weight_bin TEXT)"""
)

# create female_lifters table
cur.execute(
    """CREATE TABLE female_lifters(sex TEXT
                                          ,event TEXT
                                          ,equipment TEXT
                                          ,age FLOAT
                                          ,bodyweightKg FLOAT
                                          ,best3SquatKg FLOAT
                                          ,best3BenchKg FLOAT
                                          ,best3DeadliftKg FLOAT
                                          ,totalKg FLOAT
                                          ,age_bin TEXT
                                          ,weight_bin TEXT)"""
)

# fill male_lifters table
with open("male_powerlifters.csv", "r") as fin:
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin)  # comma is default delimiter
    to_db = [
        (
            i["sex"],
            i["event"],
            i["equipment"],
            i["age"],
            i["bodyweightKg"],
            i["best3SquatKg"],
            i["best3BenchKg"],
            i["best3DeadliftKg"],
            i["totalKg"],
            i["age_bin"],
            i["weight_bin"],
        )
        for i in dr
    ]

cur.executemany(
    "INSERT INTO male_lifters (sex,event,equipment,age,bodyweightKg,best3SquatKg,best3BenchKg,best3DeadliftKg,totalKg,age_bin,weight_bin) VALUES (?,?,?,?,?,?,?,?,?,?,?);",
    to_db,
)

# fill female_lifters table
with open("female_powerlifters.csv", "r") as fin:
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin)  # comma is default delimiter
    to_db = [
        (
            i["sex"],
            i["event"],
            i["equipment"],
            i["age"],
            i["bodyweightKg"],
            i["best3SquatKg"],
            i["best3BenchKg"],
            i["best3DeadliftKg"],
            i["totalKg"],
            i["age_bin"],
            i["weight_bin"],
        )
        for i in dr
    ]

cur.executemany(
    "INSERT INTO female_lifters (sex,event,equipment,age,bodyweightKg,best3SquatKg,best3BenchKg,best3DeadliftKg,totalKg,age_bin,weight_bin) VALUES (?,?,?,?,?,?,?,?,?,?,?);",
    to_db,
)

# important to commit and close for new rows to be added to tables
connection.commit()
connection.close()
