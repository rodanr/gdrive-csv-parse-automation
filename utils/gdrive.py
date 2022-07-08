from __future__ import print_function
import io
import os.path
from urllib import request
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]


def download_all_csv_files() -> bool:
    """
    It downloads all the csv files from the scp folder in the drive and saves them in the
    downloads/to_parse folder
    :return: It returns a boolean value. True if atleast one file have been downloaded
    """
    # setting up credentials
    creds = None
    if os.path.exists("credentials/token.json"):
        creds = Credentials.from_authorized_user_file("credentials/token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials/credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("credentials/token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("drive", "v3", credentials=creds)

        # Call the Drive v3 API
        results = (
            service.files()
            .list(
                q="mimeType='application/vnd.google-apps.folder' and name='scp' and trashed= false",
                spaces="drive",
                fields="nextPageToken, files(id, name)",
            )
            .execute()
        )
        items = results.get("files", [])
        if not items:
            print("No files found.")
            return
        # storing the scp folder id
        scp_folder_id = items[0]["id"]
        # creating query for getting files inside scp folder
        query = "'" + scp_folder_id + "'" + " in parents and trashed=false"
        scp_files = service.files().list(q=query).execute()
        # getting all the files name and file id
        files_dictionary_array = []
        for file in scp_files.get("files", []):
            files_dictionary_array.append({"id": file["id"], "name": file["name"]})
        # counter to show download
        download_count = 0
        for file_info in files_dictionary_array:
            # skipping other files than csv
            if not file_info["name"].lower().endswith(".csv"):
                continue
            # skipping file if it already exists ins parsed or to_parse directory
            parsed_file_path = "downloads/parsed/" + file_info["name"]
            to_parse_file_path = "downloads/to_parse/" + file_info["name"]
            if os.path.exists(parsed_file_path) or os.path.exists(to_parse_file_path):
                print(f'{file_info["name"]} already exists')
                continue
            # getting content of the file
            request = service.files().get_media(fileId=file_info["id"])
            file = io.BytesIO()
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(
                    f'Downloading {file_info["name"]}  {int(status.progress() * 100)}.'
                )
            # saving to a file
            file_path = "downloads/to_parse/" + file_info["name"]
            with open(file_path, "wb") as f:
                f.write(file.getbuffer())
                download_count += 1
            print(f'Downloaded {file_info["name"]}')
        print(f"|Downloaded: {download_count} files|")
        # sends true if download_count is not '0' and sends false if donwload_count is '0'
        return not download_count == 0
    except HttpError as error:
        # If possible: Handle errors from drive API.
        print(f"An error occurred: {error}")
