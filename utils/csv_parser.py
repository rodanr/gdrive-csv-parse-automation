import os
import csv
import shutil
import string


def get_downloaded_files_list_array() -> list:
    """
    This function returns a list of all the files in the "downloads/to_parse" directory
    :return: A list of all the files in the directory "downloads/to_parse"
    """
    my_array_list = os.listdir("downloads/to_parse")
    return my_array_list


def csv_to_dict(filename: string) -> dict:
    """
    `csv_to_dict` takes a filename as an argument and returns a dictionary having  parsed content of given csv appended with the extra fileName key having its fileName as its value.
    :param filename: the name of the file to be parsed
    :type filename: string
    :return: A dictionary having  parsed content of given csv appended with the extra fileName key having its fileName as its value.
    """
    filepath = "downloads/to_parse/" + filename
    my_dict = {}
    with open(filepath, mode="r") as infile:
        reader = csv.reader(infile)
        my_dict = {rows[0]: rows[1] for rows in reader}
    my_dict.update({"fileName": filename})
    return my_dict


def move_file(source: string, destination: string):
    """
    "If the source file exists, move it to the destination."

    :param source: The file to move
    :type source: string
    :param destination: The destination path where the file will be moved to
    :type destination: string
    """
    if os.path.isfile(source):
        shutil.move(source, destination)


def move_parsed_files(filename_list: list):
    """
    This function takes a list of filenames and moves them from the `to_parse` folder to the `parsed`
    folder.

    :param filename_list: a list of filenames to move
    :type filename_list: list
    """
    for filename in filename_list:
        move_file("downloads/to_parse/" + filename, "downloads/parsed/" + filename)


def parse_csv() -> dict:
    """
    Parse all the csv files present in to_parse directory of downloads folder
    :return: A list of dictionaries parsed from the downloaded csvs.
    """
    filename_list = get_downloaded_files_list_array()
    my_parsed_dict_array = []
    for filename in filename_list:
        my_parsed_dict_array.append(csv_to_dict(filename))
    return my_parsed_dict_array


if __name__ == "__main__":
    parse_csv()
