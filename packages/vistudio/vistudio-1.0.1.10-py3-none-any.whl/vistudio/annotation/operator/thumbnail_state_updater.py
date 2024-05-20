#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
@File    :   thumbnail_state_updater.py
@Time    :   2024/03/13 16:49:57
@Author  :   <dongling01@baidu.com>
"""
import time
from pandas import DataFrame
from pymongo import MongoClient


class ThumbnailStateUpdater(object):
    """
    ThumbnailStateUpdater
    """

    def __init__(self, config):
        self.config = config

    def update_thumbnail_state(self, source: DataFrame) -> DataFrame:
        """
        update thumbnail_state
        """
        mongo_client = MongoClient(self.config.mongo_uri)
        mongo = mongo_client[self.config.mongodb_database][self.config.mongodb_collection]

        for source_index, source_row in source.iterrows():
            if source_row['height'] == -1:
                update = {
                    "$set": {
                        "image_state.thumbnail_state": "Error",
                        "updated_at": time.time_ns(),
                    }
                }
            else:
                update = {
                    "$set": {
                        "image_state.thumbnail_state": "Completed",
                        "width": source_row['width'],
                        "height": source_row['height'],
                        "updated_at": time.time_ns(),
                    }
                }

            query = {
                "image_id": source_row['image_id'],
                "annotation_set_id": source_row['annotation_set_id'],
                "data_type": "Image"
            }
            _ = mongo.update_many(query, update)

        return source



