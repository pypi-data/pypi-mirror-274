#!/usr/bin/env python3
# -*- encoding: utf-8 -*-

"""
@File    :   annotation_state_updater.py
@Time    :   2024/03/13 16:49:57
@Author  :   <dongling01@baidu.com>
"""
import time
from pandas import DataFrame
from pymongo import MongoClient


class AnnotationStateUpdater(object):
    """
    AnnotationStateUpdater
    """

    def __init__(self, config):
        self.config = config

    def update_annotation_state(self, source: DataFrame) -> DataFrame:
        """
        update annotation_state
        """
        mongo_client = MongoClient(self.config.mongo_uri)
        mongo = mongo_client[self.config.mongodb_database][self.config.mongodb_collection]

        for source_index, source_row in source.iterrows():
            query = {
                "image_id": source_row['image_id'],
                "annotation_set_id": source_row['annotation_set_id'],
                "data_type": 'Annotation',
                "task_kind": 'Manual'
            }
            doc_count = mongo.count_documents(query)

            if doc_count == 0 and source_row['annotation_state'] == 'Unannotated':
                continue

            if doc_count == 0:
                update = {
                    "$set": {
                        "annotation_state": "Unannotated",
                        "updated_at": time.time_ns(),
                    }
                }
            else:
                update = {
                    "$set": {
                        "annotation_state": "Annotated",
                        "updated_at": time.time_ns(),
                    }
                }

            query = {
                "image_id": source_row['image_id'],
                "annotation_set_id": source_row['annotation_set_id'],
                "data_type": 'Image',
            }

            _ = mongo.update_one(query, update)

        return source