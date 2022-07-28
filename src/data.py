# %% Imports
import os

import pandas as pd
import xml.etree.ElementTree as ET
import datetime as dt
import mysql.connector
from mysql.connector import Error
import pandas as pd
from mysql.connector import Error
import json

from config import PROCESSED_DATA_FOLDER, RAW_DATA_FILE, MUSIC_JSON_FILE, RAW_DATA_FOLDER
from config_priv import SqlDetails
from src.utilities import save_json_file
#notes
# send the original data to raw data


class SpotifyClass():
    def extract_spotify_data(data):
        song_names = []
        artist_names = []
        played_at_list = []
        timestamps = []
        try:
            for song in data["items"]:
                song_names.append(song["track"]["name"])
                played_at_list.append(song["played_at"])
                timestamps.append(song["played_at"][0:10])
                artist_names_for_song =[]
                for artists in song["track"]["album"]["artists"]:
                    artist_names_for_song.append(artists["name"])
                artist_names.append(artist_names_for_song)
        except:
            print("there is a problem before getting data from api")

        # Prepare a dictionary in order to turn it into a pandas dataframe below
        try:
            song_dict = {
                "song_name" : song_names,
                "artist_name": artist_names,
                "played_at" : played_at_list,
                "timestamp" : timestamps
            }
        except:
            print("There is a problem moving data into a dataframe")
        try:
            save_json_file(song_dict,RAW_DATA_FOLDER,"today_music")
        except:
            print("there is a problem saving to file")
        return song_dict

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