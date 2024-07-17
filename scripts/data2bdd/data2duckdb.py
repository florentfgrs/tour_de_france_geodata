#!/usr/bin/env python3

import argparse
import csv
import json
import logging
from datetime import datetime
from pathlib import Path

import duckdb
from shapely.geometry import shape

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
logging.basicConfig(level=logging.WARNING, format="%(levelname)s - %(message)s")


_FILE_PATH_ = Path(__file__).resolve().parent


def database_exists(db_path: Path) -> bool:
    """Check if the database already exists

    :param db_path: Database path
    :type db_path: Path
    """
    if db_path.exists():
        logging.info("The base already exists, no new base will be created.")
    return db_path.exists()


def create_database(db_path: Path) -> None:
    """Create database

    :param db_path: Database path
    :type db_path: Path
    """
    try:
        connection = duckdb.connect(str(db_path))
        connection.close()
        logging.info(f"{db_path} database has been created.")
    except Exception as e:
        logging.error(e)


def execute_query_on_db(sql: str, db_path: Path, query_name) -> None:
    """Execute SQL query on database

    :param sql: SQL Query
    :type sql: str
    :param db_path: Database path
    :type db_path: Path
    """

    try:
        with duckdb.connect(str(db_path)) as con:
            con.execute(sql)
            logging.info(query_name)
    except Exception as e:
        logging.error(e)
        logging.error(query_name)


def install_load_extension(db_path: Path) -> None:
    """Install and load the needed extension

    :param db_path: _description_
    :type db_path: Path
    """
    sql = " INSTALL spatial ;"
    execute_query_on_db(sql, db_path, "Install extension")


def geojson_to_wkt(geojson_path: str) -> list:
    """Takes a gejson as input and returns the geometry of features in a list of wkt

    :param geojson_path: GeoJSON file path
    :type geojson_path: str
    :return: List of wkt
    :rtype: list
    """
    with open(geojson_path, "r") as f:
        geojson_data = json.load(f)

    wkt_list = []

    for feature in geojson_data["features"]:
        geometry = feature["geometry"]
        shapely_geometry = shape(geometry)
        wkt_list.append(shapely_geometry.wkt)

    return wkt_list


def main():
    parser = argparse.ArgumentParser(description="Insert data into a DuckDB database.")
    parser.add_argument(
        "database_path", type=str, help="The path to the DuckDB database file."
    )
    parser.add_argument(
        "data_path", type=str, help="Local path git directory tour_de_france_geodata."
    )

    args = parser.parse_args()

    # Create base if not exists
    try:
        database_path = Path(args.database_path)
    except Exception as e:
        logging.error(e)
        return

    if not database_exists(database_path):
        create_database(database_path)
    install_load_extension(database_path)

    main_directory = Path(args.data_path)
    for year_directory in main_directory.iterdir():
        if year_directory.is_dir():
            with open(_FILE_PATH_ / "create_table.sql", "r") as file:
                sql_query = file.read()
                sql_query = sql_query.format(year_directory.name, year_directory.name)
            execute_query_on_db(sql_query, database_path, "Create table")

            for stage_directory in year_directory.iterdir():
                if stage_directory.is_dir():
                    geojson_path = (
                        stage_directory
                        / f"trace_{year_directory.name}_{str(int(stage_directory.name))}.geojson"
                    )
                    csv_path = (
                        stage_directory
                        / f"metadata_{year_directory.name}_{str(int(stage_directory.name))}.csv"
                    )
                    if geojson_path.exists():
                        wkb = (
                            f"ST_GeomFromTEXT('{geojson_to_wkt(str(geojson_path))[0]}')"
                        )
                    else:
                        wkb = "NULL"
                    with open(csv_path, "r", newline="", encoding="utf-8") as file:
                        csv_reader = csv.reader(file, delimiter=";")
                        next(csv_reader)  # Skip header row
                        for row in csv_reader:
                            numero = int(row[0])
                            date = datetime.strptime(row[1], "%d/%m/%Y").strftime(
                                "%Y-%m-%d"
                            )
                            depart = row[2].replace("'", "''")
                            arrivee = row[3].replace("'", "''")
                            long = float(row[4])
                            denivele = "NULL" if row[5] == "NC" else float(row[5])
                            typee = int(row[6])
                            url = row[7]

                            sql_insert = f"LOAD SPATIAL ; INSERT INTO tour_de_france_{year_directory.name} VALUES ({numero}, '{date}', '{depart}', '{arrivee}', {long}, {denivele}, {typee}, '{url}', {wkb})"
                            execute_query_on_db(
                                sql_insert,
                                database_path,
                                f"Insert data {stage_directory}",
                            )


if __name__ == "__main__":
    main()
