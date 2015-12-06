"""Implements PageFileSystemStorage class """

import os
import django

from django.core.files.storage import FileSystemStorage

from pages.conf import settings


class PageBaseFileSystemStorage(FileSystemStorage):
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
        self.__log('PageFileSystemStorage initialized.')

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

# compatibility with django 1.7
if django.VERSION[:2] >= (1, 8):
    class PageFileSystemStorage(PageBaseFileSystemStorage):

        def get_available_name(self, name, max_length=None):
            # If the filename already exists, remove it as if it was a true file system
            if settings.PAGES_FILE_OVERWRITE_EXISTS:
                if self.exists(name):
                    self.__log('File ' + name + ' exists, rewrite used.')
                    os.remove(os.path.join(settings.MEDIA_ROOT, name))
            else:
                name = FileSystemStorage.get_available_name(self, name, max_length)
            return name
else:
    class PageFileSystemStorage(PageBaseFileSystemStorage):

        def get_available_name(self, name):
            # If the filename already exists, remove it as if it was a true file system
            if settings.PAGES_FILE_OVERWRITE_EXISTS:
                if self.exists(name):
                    self.__log('File ' + name + ' exists, rewrite used.')
                    os.remove(os.path.join(settings.MEDIA_ROOT, name))
            else:
                name = FileSystemStorage.get_available_name(self, name)
            return name
