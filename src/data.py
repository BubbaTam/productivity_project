# %% Imports
import os

import pandas as pd
import xml.etree.ElementTree as ET
import datetime as dt
import mysql.connector
from mysql.connector import Error
from config_priv import SqlDetails
import pandas as pd
from mysql.connector import Error
import json

from config import PROCESSED_DATA_FOLDER, RAW_DATA_FILE, MUSIC_JSON_FILE
#notes
# send the original data to raw data


class SpotifyClass():

    def load_data_to_sql():
        """
        will need to transform beforehand
        sacrifice of normalisation
        """
        with open(MUSIC_JSON_FILE) as f:
            json_data = json.load(f)
        try:
            connection = mysql.connector.connect(host=SqlDetails.host,
                                                 user=SqlDetails.user,
                                                 password=SqlDetails.password,
                                                 database=SqlDetails.database
                                                 )

            sql_query_create_table = """
            CREATE TABLE IF NOT EXISTS `personal_tracking`.`my_played_tracks`(
                song_name VARCHAR(200),
                artist_names VARCHAR(200),
                played_at VARCHAR(200),
                timestamp VARCHAR(200),
                CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
            );
            """

            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                #making cursor object for query execution
                cursor = connection.cursor()

                #queries:

                cursor.execute(sql_query_create_table)
                for count,value in enumerate(json_data['song_name']):
                    cursor.execute("INSERT INTO `personal_tracking`.`my_played_tracks` VALUES ('{}',{},'{}',{})".format(
                    str(json_data["song_name"][count]).replace("'","''"),
                    '"'+ str(json_data["artist_name"][count]).replace("'","''").replace(",","\,") +'"',
                    str(json_data["played_at"][count]).replace("'","''"),
                    '"'+str(json_data["timestamp"][count]).replace("'","''")+'"'))

                #important for inserting data to sql database
                connection.commit()
                print("sending data to database")
        except Error as e:
            print("Error while connecting to MySQL", e)

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")