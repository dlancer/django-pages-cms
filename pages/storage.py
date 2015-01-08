"""Implements PageFileSystemStorage class """

import os

from django.core.files.storage import FileSystemStorage

from pages.conf import settings


class PageFileSystemStorage(FileSystemStorage):
    def __log(self, log):
        if self.logger:
            self.logger.log(log)

    def __init__(self, location=None, logger=None):
        # Get location from Settings, if not mentioned PAGES_FILE_LOCATION must be set in settings
        if not location:
            location = settings.PAGES_FILE_LOCATION
        self.logger = logger
        # Initialize super class
        FileSystemStorage.__init__(self, location=location)
        self.file_permissions_mode = settings.PAGES_FILE_UPLOAD_PERMISSIONS
        if getattr(settings, 'FILE_UPLOAD_DIRECTORY_PERMISSIONS', False):
            self.directory_permissions_mode = settings.PAGES_FILE_UPLOAD_DIRECTORY_PERMISSIONS

        # add log
        self.__log('PageFileSystemStorage Initialized')

    # override default behavior where default mode is 'rb'
    def open(self, name, mode='r'):
        return FileSystemStorage.open(self, name, mode)

    def _open(self, name, mode='rb'):
        self.__log('Opening file ' + name + ' in mode=' + mode)
        return FileSystemStorage._open(self, name, mode)

    def exists(self, name):
        exist = os.path.exists(self.path(name))
        if exist:
            self.__log('File ' + name + ' exists.')
        else:
            self.__log('File ' + name + ' does not exist.')
        return exist

    def delete(self, name):
        FileSystemStorage.delete(self, name)
        self.__log('File ' + name + ' deleted.')
