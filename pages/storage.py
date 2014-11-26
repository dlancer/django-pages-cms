"""Implements PageFileSystemStorage class """

import os

from django.core.files.storage import FileSystemStorage

from conf import settings


class PageFileSystemStorage(FileSystemStorage):
    def __log(self, log):
        if self.logger:
            self.logger.log(log)

    def __init__(self, location=None, logger=None):
        # Get location from Settings, if not mentioned  PAGES_STORAGE_FILESYSTEM must be set in settings.py
        if not location:
            location = settings.PAGES_STORAGE_FILESYSTEM_LOCATION
        self.logger = logger
        # Initialize super class
        FileSystemStorage.__init__(self, location=location)
        self.file_permissions_mode = settings.PAGES_STORAGE_FILESYSTEM_FILE_PERMISSION_MODE
        # add log
        self.__log('PageFileSystemStorage Initialized')

    def get_available_name(self, name):
        # if file name exists
        if self.exists(name):
            # Remove the existing file
            self.delete(name)
        # Return the input name as output
        return name

    # override default behavior where default mode is 'rb'
    def open(self, name, mode='r'):
        return FileSystemStorage.open(self, name, mode)

    def _open(self, name, mode):
        self.__log('Opening file ' + name + ' in mode=' + mode)
        return FileSystemStorage._open(self, name, mode)

    def exists(self, name):
        fExist = os.path.exists(self.path(name))
        if fExist:
            self.__log('File ' + name + ' exists.')
        else:
            self.__log('File ' + name + ' does not exist.')
        return fExist

    def delete(self, name):
        FileSystemStorage.delete(self, name)
        self.__log('File ' + name + ' deleted.')
