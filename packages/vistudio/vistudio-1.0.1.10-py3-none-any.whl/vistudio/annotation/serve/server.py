# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
#
"""

"""
import asyncio
import os
import yaml
import argparse
import bcelogger
from ray import serve
from ray.serve.handle import DeploymentHandle

from vistudio.annotation.config.config import Config
from vistudio.annotation.pipeline.generate_thumbnail_pipeline import GenerateThumbnailPipeline
from vistudio.annotation.pipeline.generate_webp_pipeline import GenerateWebpPipeline
from vistudio.annotation.pipeline.update_annotation_state_pipeline import UpdateAnnotationStatePipeline
from vistudio.annotation.pipeline.update_image_created_at_pipeline import UpdateImageCreatedAtPipeline


# 执行Pipelines
@serve.deployment()
class PipelineRun:
    """
    PipelineRun
    """
    def __init__(self, ppls, config):
        self.ppls = init_pipeline(ppls, config)
        self.config = config

        self.sleep_unit = 2
        self.wait_count = 2

        self.signal = []

    async def __call__(self, request):
        self.signal.append(1)

        try:
            annotation_set_id = request.get("annotation_set_id")
            pipeline_names = request.get("pipeline_names")
            if not isinstance(annotation_set_id, str) or not isinstance(pipeline_names, list):
                raise ValueError("Invalid request params")

            args = {"annotation_set_id": annotation_set_id}
            ppls = init_pipeline(pipeline_names, self.config, args)

            for ppl in ppls:
                bcelogger.info(f"start ppl run: {ppl}")
                ppl.run.remote()
        except Exception as e:
            bcelogger.error(f"request parse error: {e}")

        return "Hello PipelineRun"

    async def run(self):
        """
        定时触发 pipelines
        """
        i = 0
        while True:
            # 非阻塞触发pipelines
            for p in self.ppls:
                bcelogger.info("start ppl run")
                p.run.remote()

            # 不等待pipelines执行完，进入定时触发
            if i < 30:
                # 30个循环内， 间隔4s触发一次
                self.wait_count = 2
            else:
                # 30个循环后， 间隔8s、16s、……、10min(最大) 触发一次
                self.wait_count = min(300, 2 * self.wait_count)

            bcelogger.info(f"---start sleep, wait_cont is: {self.wait_count} ---")
            for _ in range(self.wait_count):
                if len(self.signal) > 0:
                    bcelogger.info("---over sleep---")
                    self.wait_count = 2
                    i = 0
                    self.signal.clear()
                    break

                await asyncio.sleep(self.sleep_unit)
            i += 1


@serve.deployment(num_replicas=1, ray_actor_options={"num_cpus": 1, "num_gpus": 0})
class PipelineDispatcher:
    """
    PipelineDispatcher：启动定时任务
    """
    def __init__(self, ppl: DeploymentHandle):
        self.__ppl = ppl
        self.__ppl.options(method_name="run").remote()

    async def __call__(self, http_request):
        request = await http_request.json()
        bcelogger.info(f"request: {request}")
        self.__ppl.remote(request)

        return "Hello PipelineTest"


def parse_args() -> Config:
    """
    获取环境变量
    """
    args = {
        "mongo_user": os.environ.get('MONGO_USER', 'root'),
        "mongo_password": os.environ.get('MONGO_PASSWORD', 'mongo123#'),
        "mongo_host": os.environ.get('MONGO_HOST', '10.27.240.45'),
        "mongo_port": int(os.environ.get('MONGO_PORT', 8719)),
        "mongo_database": os.environ.get('MONGO_DB', 'annotation'),
        "mongo_collection": os.environ.get('MONGO_COLLECTION', 'annotation'),
        "windmill_endpoint": os.environ.get('WINDMILL_ENDPOINT', 'http://10.27.240.45:8340')
    }
    config = Config(args)
    bcelogger.info(f"---config---:{config}")

    return config


def init_pipeline(pipeline_names, config, args=None):
    """
    初始化pipeline
    :param pipeline_names:
    :param config:
    :return:
    """
    ppls = []
    for n in pipeline_names:
        if n == "GenerateThumbnailPipeline":
            ppl = GenerateThumbnailPipeline.remote(config=config, parallelism=10)
        elif n == "GenerateWebpPipeline":
            ppl = GenerateWebpPipeline.remote(config=config, parallelism=10)
        elif n == "UpdateAnnotationStatePipeline":
            ppl = UpdateAnnotationStatePipeline.remote(config=config, parallelism=10, args=args)
        elif n == "UpdateImageCreatedTimePipeline":
            ppl = UpdateImageCreatedAtPipeline.remote(config=config, parallelism=10)
        else:
            bcelogger.error(f"not support pipeline: {n}")
            continue
        ppls.append(ppl)

    return ppls


def main(args):
    """
    启动serve
    """
    file_path = args.file_path
    try:
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
    except (FileNotFoundError, yaml.YAMLError) as e:
        bcelogger.error(f"Error reading file or parsing YAML: {e}")
        return

    pipeline_names = data.get('pipeline_names', [])
    config = parse_args()

    app = PipelineDispatcher.bind(PipelineRun.bind(pipeline_names, config))
    serve.run(app,
            route_prefix="/imageaggregation",
            name="pipeline_app")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--f",
        dest="file_path",
        required=True,
        default="",
        help="background pipelines",
    )

    args = parser.parse_args()
    main(args)




