#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
@File    :   image_created_at_updater.py
@Time    :   2024/03/13 16:49:57
@Author  :   <dongling01@baidu.com>
"""

import time
from pandas import DataFrame
from pymongo import MongoClient


class ImageCreatedAtUpdater(object):
    """
    ImageCreatedAtUpdater
    """

    def __init__(self, config):
        self.config = config

    def update_image_created_at(self, source: DataFrame) -> DataFrame:
        """
        update image_created_at
        """
        mongo_client = MongoClient(self.config.mongo_uri)
        mongo = mongo_client[self.config.mongodb_database][self.config.mongodb_collection]

        for source_index, source_row in source.iterrows():
            query = {
                "image_id": source_row['image_id'],
                "annotation_set_id": source_row['annotation_set_id'],
                "data_type": 'Image'
            }
            item = mongo.find_one(query)
            if item is None:
                continue

            update = {
                "$set": {
                    "image_created_at": item.get('created_at'),
                    "updated_at": time.time_ns(),
                }
            }
            query = {
                "image_id": source_row['image_id'],
                "annotation_set_id": source_row['annotation_set_id'],
                "data_type": 'Annotation',
            }
            _ = mongo.update_many(query, update)

        return source







