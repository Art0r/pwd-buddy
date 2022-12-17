from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import FileNotUploadedError
import shutil
import os


def delete_all_then_upload(upload_folder: str) -> bool:
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)

    file_list = drive.ListFile(
        {'q': "'{}' in parents and trashed=false".format('1K5RD4yJVid4zOl090E6lJHEws_tNpYVV')}).GetList()
    for file in file_list:
        try:
            gauth.service.files().delete(fileId=file['id']).execute()
        except:
            continue

    upload_file_list = ['accounts.txt']

    try:
        for upload_file in upload_file_list:
            gfile = drive.CreateFile({'parents': [{'id': upload_folder}]})
            gfile.SetContentFile(upload_file)
            gfile.Upload()
        return True
    except FileNotUploadedError as e:
        return False


def download(download_folder: str):
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)

    file_list = drive.ListFile(
        {'q': "'{}' in parents and trashed=false".format(download_folder)}).GetList()

    for i, file in enumerate(sorted(file_list, key=lambda x: x['title']), start=1):
        print('Downloading {} file from GDrive ({}/{})'.format(file['title'], i, len(file_list)))
        file.GetContentFile(file['title'])
