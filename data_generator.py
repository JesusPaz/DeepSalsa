import pymysql
import os

# Dictionary with the id from the DB and the new id
dict_id = {}

# Dictionary that contains song, user and beats
ids_databeats = {}


# Change the id from the database to a new one, only to the songs with 3 repetitions
def rename_id():
    global dict_id
    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa")

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "SELECT `ID_CANCION` FROM `despacho_cancion` WHERE `REPETICIONES` = 3"
            cursor.execute(sql)
            query = cursor.fetchall()

            i = 1
            for x in query:
                dict_id[x[0]] = i
                i += 1

            print(len(dict_id))

            file = open("Id_to_final_number.txt", "w")
            file.write("ID_DB   ID_NEW\n")
            for y in dict_id:
                file.write(str(y) + " " + str(dict_id[y]) + "\n")
            file.close()

    finally:
        connection.close()


# Generate a new txt that contains the beats of a song tagged
def generate_txt(id_song, id_user, beats):
    file = open("data/" + str(id_song) + "_" + str(id_user) + ".txt", "w")
    file.write(beats)
    file.close()


# create a dictionary that contains all the id_song, id_user and beats
def create_dict_beats():
    rename_id()
    global ids_databeats

    connection = pymysql.connect("127.0.0.1",
                                 "admin",
                                 "1539321441",
                                 "beatsalsa")

    try:
        with connection.cursor() as cursor:

            for x in dict_id:
                # Create a new record
                sql = "SELECT `FK_ID_CANCION`, `FK_CEDULA_USUARIO`, `BEATS` FROM `databeats` WHERE `FK_ID_CANCION` = %s"
                cursor.execute(sql, x)
                query = cursor.fetchall()


                for y in range(3):
                    ids_databeats[str(x) + "_" + str(query[y][1])] = str(query[y][2])
                    generate_txt(str(dict_id[x]), query[y][1], query[y][2])

            print(len(ids_databeats))
    finally:
        connection.close()

create_dict_beats()

