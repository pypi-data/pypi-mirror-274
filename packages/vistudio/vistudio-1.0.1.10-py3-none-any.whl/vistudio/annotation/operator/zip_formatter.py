#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   label_formatter.py
"""
import os.path
from typing import Union, Dict

from windmillcomputev1.filesystem import blobstore, upload_by_filesystem

from vistudio.annotation.operator.reader import zip_extensions


class ZipFormatter(object):
    """
    LabelFormatter
    """

    def __init__(self,
                 filesystem: Union[Dict] = dict,
                 annotation_format: str = None
                 ):
        self.filesystem = filesystem
        self.bs = blobstore(filesystem)
        self.annotation_format = annotation_format

    def unzip_and_upload(self, file_uris: list()) -> str:
        """
        unzip_and_upload
        :param file_uris:
        :return:
        """
        data_uri = None
        for file_uri in file_uris:
            file_name = file_uri.split("/")[-1]
            if not (file_name.lower().endswith(zip_extensions)):
                return file_uris
            directory_path = "/".join(file_uri.split("/")[:-1]).replace("s3://", "")
            filename_without_extension = ''
            if self.annotation_format == 'cvat':
                filename_without_extension = file_name.split(".")[0]

            import shutil
            dest_file = os.path.join(os.path.join(directory_path, filename_without_extension), file_name)
            if not os.path.exists(os.path.dirname(dest_file)):
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)

            self.bs.download_file(path=file_uri, file_name=dest_file)
            shutil.unpack_archive(dest_file, os.path.join(directory_path, filename_without_extension))
            os.remove(dest_file)

            top_directory = os.path.join(directory_path, os.listdir(directory_path)[0])

            file_path = os.path.join(directory_path, file_name).rsplit("/", 1)[0]
            dest_path = "/".join(file_uri.split("/")[:-1])

            upload_by_filesystem(filesystem=self.filesystem, file_path=file_path, dest_path=dest_path)
            shutil.rmtree(file_path)
            # shutil.rmtree(top_directory)
            data_uri = "s3://" + top_directory

        return data_uri
