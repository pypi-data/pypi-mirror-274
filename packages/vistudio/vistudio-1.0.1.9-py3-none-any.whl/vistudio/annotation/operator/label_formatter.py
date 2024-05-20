#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
"""
@File    :   label_formatter.py
"""

from typing import Union, Dict

import logit
from windmillcomputev1.filesystem import init_py_filesystem

from vistudio.annotation.api.annotation import parse_annotation_set_name
import ray


class LabelFormatter(object):
    """
    LabelFormatter
    """

    def __init__(self,
                 labels: Union[Dict] = dict,
                 annotation_format: str = "",
                 annotation_set_id: str = None,
                 annotation_set_name: str = None,
                 filesystem: Union[Dict] = None
                 ):
        self.labels = labels
        self.annotation_set_id = annotation_set_id
        self.annotation_set_name = annotation_set_name
        self.annotation_format = annotation_format
        self._py_fs = init_py_filesystem(filesystem)

    def _get_max_label_id(self):
        """
        _get_max_label_id
        :return:
        """
        if len(self.labels) == 0:
            return 0
        else:
            return max(self.labels.keys(), key=lambda x: int(x))

    @staticmethod
    def _build_labels(label_names: list(), max_label_id: int) -> dict():
        labels = dict()
        for index, label_name in enumerate(label_names):
            label_id = int(max_label_id) + index + 1
            labels[str(label_id)] = label_name
        return labels

    def _get_import_labels(self, ds: "Dataset") -> dict():
        need_import_labels = dict()
        if self.annotation_format == 'imagenet':
            label_names = ds.select_columns(cols=['label']).unique(column='label')
            max_label_id = self._get_max_label_id()
            need_import_labels = self._build_labels(label_names=label_names, max_label_id=max_label_id)
        elif self.annotation_format == 'cityscapes':
            label_id_set = set()
            file_uris = ds.unique(column='item')
            label_color_files = [file_uri for file_uri in file_uris if file_uri.endswith(".txt")]
            label_color_series = ray.data.read_text(paths=label_color_files, filesystem=self._py_fs).to_pandas()['text']
            for label_id, label_name in label_color_series.items():
                need_import_labels[str(label_id + 1)] = label_name.split()[-1]
        elif self.annotation_format == 'coco':
            labels_ds = ds.select_columns(cols=['categories'])
            for row in labels_ds.iter_rows():
                for label in row['categories']:
                    label_id = label.get('id')
                    need_import_labels[str(label_id)] = label.get('name')

        elif self.annotation_format == 'cvat':
            labels_list = ds.flat_map(lambda row: row['labels']).unique(column='name')
            max_label_id = self._get_max_label_id()
            need_import_labels = self._build_labels(label_names=labels_list, max_label_id=max_label_id)

        return need_import_labels

    def labels_to_vistudio_v1(self, ds: "Dataset") -> list():
        """
        labels_to_vistudio_v1
        :return:
        """
        need_import_labels = self._get_import_labels(ds=ds)
        not_in_labels = {key: value for key, value in need_import_labels.items() if
                         key not in self.labels and value not in self.labels.values()}

        logit.info("import labels.not_in_labels:{}".format(not_in_labels))

        annotation_labels = list()
        if len(not_in_labels) == 0:
            return annotation_labels
        client_annotation_set_name = parse_annotation_set_name(self.annotation_set_name)
        for label_id, label_name in not_in_labels.items():
            label_dict = {
                "workspace_id": client_annotation_set_name.workspace_id,
                "project_name": client_annotation_set_name.project_name,
                "annotation_set_name": self.annotation_set_name.split("/")[-1],
                "local_name": str(label_id),
                "display_name": label_name,
                "color": self.random_color()
            }
            annotation_labels.append(label_dict)

        def get_local_name_as_int(label_dict):
            return int(label_dict["local_name"])

        sorted_labels = sorted(annotation_labels, key=get_local_name_as_int)

        return sorted_labels

    @staticmethod
    def random_color():

        """生成随机的十六进制颜色代码。

        返回：
          表示十六进制颜色代码的字符串（例如 #00FF00）。
        """
        import colorsys
        import random
        h, s, v = random.uniform(0, 1), random.uniform(0.5, 1), random.uniform(0.5, 1)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        hex_color = "#" + "".join([f"{x:02x}" for x in (int(r * 255), int(g * 255), int(b * 255))])
        return hex_color
