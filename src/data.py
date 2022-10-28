# %% Imports
import os

import pandas as pd
import xml.etree.ElementTree as ET
import datetime as dt
import mysql.connector
from mysql.connector import Error
import json
import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth

from config import PROCESSED_DATA_FOLDER, RAW_DATA_FILE, MUSIC_JSON_FILE, RAW_DATA_FOLDER, HEALTH_DATA_PROCESS,SPOTIFY_SQL_FILE
from config_priv import SqlDetailsWSL, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, REDIRECT_URI, TOKEN_LOCATION
from src.utilities import save_json_file, time_at_start_today, dummy_sql_statement


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
    def get_data_from_spotify_api():
        def create_spotify_oauth():
            return SpotifyOAuth(
                client_id = SPOTIFY_CLIENT_ID,
                client_secret = SPOTIFY_CLIENT_SECRET,
                redirect_uri = REDIRECT_URI,
                scope = "user-read-recently-played"
            )
        def get_token():
            """To deal with if they don't already have a session token or if their token has expired """
            with open(TOKEN_LOCATION,"r") as f:
                token_data = json.load(f)
            oauth = create_spotify_oauth()
            token_info = oauth.refresh_access_token(token_data["refresh_token"])
            return token_info
        def recently_played():
            print("start of recently played")
            try:
                token_info = get_token()
            except:
                print("no log in details")
            sp = spotipy.Spotify(auth=token_info["access_token"])
            data = sp.current_user_recently_played(limit=50,after=time_at_start_today())
            SpotifyClass.extract_spotify_data(data)
        return recently_played()
    def load_data_to_sql():
        """
        will need to transform beforehand
        sacrifice of normalisation
        """
        with open(MUSIC_JSON_FILE) as f:
            json_data = json.load(f)
        try:
            connection = mysql.connector.connect(host=SqlDetailsWSL.host,
                                                 user=SqlDetailsWSL.user,
                                                 password=SqlDetailsWSL.password,
                                                 )

            sql_query_personal_tracking_database = """
            CREATE DATABASE IF NOT EXISTS personal_tracking;
            """
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()

                #queries:
                cursor.execute(sql_query_personal_tracking_database)
        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")

        try:
            my_sql_connection = mysql.connector.connect(host=SqlDetailsWSL.host,
                                                        user=SqlDetailsWSL.user,
                                                        password=SqlDetailsWSL.password,
                                                        database=SqlDetailsWSL.database
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
            if my_sql_connection.is_connected():
                db_Info = my_sql_connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                #making cursor object for query execution
                cursor = my_sql_connection.cursor()

                #queries:
                cursor.execute(sql_query_create_table)
                for count,value in enumerate(json_data['song_name']):
                    cursor.execute("INSERT INTO `personal_tracking`.`my_played_tracks` VALUES ('{}',{},'{}',{})".format(
                    str(json_data["song_name"][count]).replace("'","''"),
                    '"'+ str(json_data["artist_name"][count]).replace("'","''").replace(",","\,") +'"',
                    str(json_data["played_at"][count]).replace("'","''"),
                    '"'+str(json_data["timestamp"][count]).replace("'","''")+'"'))

                #important for inserting data to sql database
                my_sql_connection.commit()
                #print("sending data to database")
        except Error as e:
            print("Error while connecting to MySQL", e)

        finally:
            if my_sql_connection.is_connected():
                cursor.close()
                my_sql_connection.close()
                print("MySQL connection is closed")
    def transform_data_to_sql_file():
        """ """
        with open(MUSIC_JSON_FILE,"r") as f:
            json_data = json.load(f)
        if json_data == {'song_name': [], 'artist_name': [], 'played_at': [], 'timestamp': []}:
            sql_string = dummy_sql_statement()
            with open(SPOTIFY_SQL_FILE,"w") as f:
                f.write(sql_string)
        else:
            sql_string = """INSERT INTO `personal_tracking`.`my_played_tracks`
                        VALUES """
            for count,value in enumerate(json_data['song_name']):
                song_name = str(json_data["song_name"][count]).replace("'","''")
                artist_name = str(json_data["artist_name"][count]).replace("[","").replace("]","").replace("'","")
                played_at = str(json_data["played_at"][count]).replace("'","''")
                timestamp = str(json_data["timestamp"][count]).replace("'","''")

                data_tuple = (song_name,artist_name,played_at,timestamp)
                sql_string = sql_string + str(data_tuple) + ","

            sql_string = sql_string[:-1]
            sql_string = sql_string + ";"
            with open(SPOTIFY_SQL_FILE,"w") as f:
                f.write(sql_string)