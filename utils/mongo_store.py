import pymongo
from utils.csv_parser import get_downloaded_files_list_array, move_parsed_files


def insert_to_mongodb(my_dict: list) -> bool:
    """
    This function takes a list of dictionaries as an argument and inserts them into a MongoDB database

    :param my_dict: list
    :type my_dict: list
    :return: A boolean value.False if any error, otherwise True
    """

    try:
        mongodb_uri = "mongodb://localhost:27017"
        myclient = pymongo.MongoClient(mongodb_uri)
        mydb = myclient["gdrive-csv-automation"]

        mycol = mydb["parsed-csv-data"]
        result = mycol.insert_many(my_dict)
        # moving parsed files from to_parse to parsed directory after writing to database
        move_parsed_files(get_downloaded_files_list_array())
        return result.acknowledged
    except Exception:
        return False
