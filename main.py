from utils import gdrive, csv_parser, mongo_store


def main():
    """
    It downloads all the csv files from the google drive, parses them and stores them in the mongodb
    database
    """
    to_parse_status = csv_parser.get_downloaded_files_list_array()
    download_status = gdrive.download_all_csv_files()
    # True if files have been downloaded or there is file to be parsed in to_parse directory
    if download_status or to_parse_status:
        if to_parse_status:
            print("-> Parsing some files that were not parsed before")
        if download_status:
            print("-> Parsing downloaded files to database")
        my_dict = csv_parser.parse_csv()
        result = mongo_store.insert_to_mongodb(my_dict)
        print("Successfully wrote to database") if result else print(
            "Some error occured while writing to the database"
        )
    else:
        print("Nothing to parse")


if __name__ == "__main__":
    main()
