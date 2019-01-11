import abc
import json
import socket
import sys
import six
import os
import commands
import logging
import ast
from conf import base_conf
from libs.common import utils
from libs.common import exception as myexception
import libs.paddlecloud.padddlecloud_api as api
import libs.local.docker_utils as docker_utils
import models.benchmark_server.helper as helper

sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from benchmark_server import benchmark_models as bm


def produce_new_file(old_path, new_path, replace_dict):
    """替换字符串存入新文件"""
    data = ''
    with open(old_path, 'r+') as f:
        for line in f.readlines():
            for key, value in replace_dict.items():
                line = line.replace(key, value)
            data += line

    with open(new_path, 'w+') as f:
        f.truncate()
        f.writelines(data)

class JobPloy(object):
    """job 调度策略，包括提交周期，检查周期，周期单位"""
    def __init__(self, submit_period, check_period, statistics_unit):
        self.submit_period =submit_period
        self.check_period = check_period
        self.statistics_unit = statistics_unit

    def __str__(self):
        return "submit_period={}," \
               "check_period={}," \
               "update_db_period={}".format(
            str(self.submit_period),
            str(self.check_period),
            str(self.statistics_unit)
        )


@six.add_metaclass(abc.ABCMeta)
class BaseJobClass(object):
    """基础job类，目前支持local，paddlecloud，qianmo
    """
    def set_ploy(self):
        """设置job的调度信息"""
        ploy_conf = self.conf["ploy"]
        jp = JobPloy(ploy_conf["submit_period"],
                     ploy_conf["check_period"],
                     ploy_conf["statistics_unit"])
        return jp

    @abc.abstractmethod
    def set_scrpt_files(self):
        """
        设置运行相关脚本文件
        :return:
        """

    @abc.abstractmethod
    def submit_job(self):
        """
        提交作业到集群
        :return:
        """

class LocalJobClass(BaseJobClass):
    """本地集群的作业
    """
    def __init__(self, conf, args):
        self.conf = conf
        self.conf["code_branch"] = args.code_branch
        self.conf["image_id"] = args.image_id
        self.conf["job_type"] = args.job_type
        self.conf["ploy"] = self.set_ploy()
        self.conf["cluster_job_id"] = ""
        self.conf["cluster_type_id"] = 0
        self.conf["frame_id"] = int(self.conf["frame_id"] if "frame_id" in self.conf else "0")
        self.conf["eval_cmd"] = self.conf["eval_cmd"] \
            if "eval_cmd" in self.conf else "echo 'nothing to eval'"
        self.conf["infer_cmd"] = self.conf["infer_cmd"] \
            if "infer_cmd" in self.conf else "echo 'nothing to infer'"
        self.script_files = self.set_scrpt_files()

    def set_scrpt_files(self):
        """"""
        pass

    @classmethod
    def produce_scrpt_files(cls, job_instance):
        """
        根据配置设置作业的docker_start.sh 以及container_run.sh, before_hook.sh, end_hook.sh
        :param job_instance:
        :return:
        """
        job_cluster_conf = ast.literal_eval(job_instance.cluster_conf)
        frame = bm.Frame.VALUES_TO_NAMES[int(job_instance.frame_id)]
        model_path = str(job_instance.model_name)
        image_version = str(bm.Image.objects.filter(image_id=int(job_instance.image_id))[0].version)
        old_start_docker_path = os.path.join(base_conf.ROOT_PATH, "libs",
                                                  "local", "start_docker.sh")
        new_start_docker_path = os.path.join(base_conf.ROOT_PATH, "files", frame, "local",
                                              model_path, "start_docker.sh")
        old_cr_path = os.path.join(base_conf.ROOT_PATH, "libs",
                                                  "local", "container_run.sh")
        new_cr_path = os.path.join(base_conf.ROOT_PATH, "files", frame, "local",
                                              model_path, "container_run.sh")
        get_gpu_path = os.path.join(base_conf.ROOT_PATH, "libs", "local", "docker_utils.py")

        #生成专属job的before_hook.sh
        old_before_hook_path = os.path.join(base_conf.ROOT_PATH, "files", frame, "local",
                                              model_path, "before_hook.sh")
        new_before_hook_path = os.path.join(base_conf.ROOT_PATH, "files", frame, "local",
                                        model_path, "before_hook_%s_%s.sh"
                                % (job_instance.run_machine_type, job_instance.run_rpc_type))
        before_hook_redict = {"image_version_holder": image_version,
                              "frame_holder": frame,
                              "model_holder": str(job_instance.model_name)}
        produce_new_file(old_before_hook_path, new_before_hook_path, before_hook_redict)

        # 生成专属job的end_hook.sh
        old_end_hook_path = os.path.join(base_conf.ROOT_PATH, "files", frame, "local",
                                         model_path, "end_hook.sh")
        new_end_hook_path = os.path.join(base_conf.ROOT_PATH, "files", frame, "local",
                                        model_path, "end_hook_%s_%s.sh"
                                % (job_instance.run_machine_type, job_instance.run_rpc_type))
        post_log_path = os.path.join(base_conf.ROOT_PATH, "libs", "local", "post_benchmark_log.py")
        end_hook_redict = {"post_benchmark_log.py_holder": post_log_path}
        produce_new_file(old_end_hook_path, new_end_hook_path, end_hook_redict)

        # 生成专属job的start_docker.sh 和 container_run.sh
        start_docker_rpdict = {"container_run.sh_holder": new_cr_path,
                               "get_gpu.py_holder": get_gpu_path}
        container_run_rpdict = {"export env_holder": "",
                                "workdir_holder": job_cluster_conf["workdir"],
                                "run_cmd_holder": str(job_instance.run_cmd),
                                "eval_cmd_holder": str(job_instance.eval_cmd),
                                "infer_cmd_holder": str(job_instance.infer_cmd),
                                "before_hook_holder": str(new_before_hook_path),
                                "end_hook_holder": str(new_end_hook_path)}
        produce_new_file(old_start_docker_path, new_start_docker_path, start_docker_rpdict)
        produce_new_file(old_cr_path, new_cr_path, container_run_rpdict)
        return new_start_docker_path


    def submit_job(self):
        """"""
        frame = bm.Frame.VALUES_TO_NAMES[int(self.conf["frame_id"])]
        dockeImage = bm.DockerImage.VALUES_TO_NAMES[frame]
        self.conf["body"]["clusterConf"]["dockerImage"] = dockeImage

    @classmethod
    def localjob_run(cls, job_instance):
        """
        查询submit状态的作业，并提交到local集群中训练
        :param job_instance:
        :return:
        """
        job_cluster_conf = ast.literal_eval(job_instance.cluster_conf)
        gpu_num = int(job_cluster_conf["k8sGpuCards"]) \
            if "k8sGpuCards" in job_cluster_conf else 0
        #启动docker容器前先检查GPU卡是否满足作业需求
        cuda_visible_devices = docker_utils.check_enough_gpu(gpu_num)
        logging.info("job {} cuda_visible_devices={}".format(job_instance.job_name,
                                                             cuda_visible_devices))
        if not cuda_visible_devices:
            return False
        new_start_docker_path = cls.produce_scrpt_files(job_instance)
        try:

            _, out_put = commands.getstatusoutput("sh {0} {1} {2} {3} {4}".format(
                                                  new_start_docker_path,
                                                  job_instance.job_name,
                                                  job_cluster_conf["dockerImage"],
                                                  cuda_visible_devices,
                                                  job_instance.job_id))
            print("out_put is {}".format(out_put))

            if "docker" in out_put:
                logging.error(out_put)
                raise myexception.ResponseError(out_put)

            job_instance.cluster_job_id = out_put[0:12]
            job_cluster_conf["run_host"] = socket.gethostname()
            job_cluster_conf["CUDA_VISIBLE_DEVICES"] = cuda_visible_devices
            job_instance.cluster_conf = job_cluster_conf
            return True
        except Exception as exp:
            error_msg = "running local job {0} failed, respone is {1}".format(
                job_instance.job_name, str(exp))
            logging.error(error_msg)
            raise myexception.ResponseError(error_msg)


class PaddleCloudJobClass(BaseJobClass):
    """paddlecloud job
       目前只支持paddle的作业
    """
    def __init__(self, conf, args):
        self.conf= conf
        self.conf["code_branch"] = args.code_branch
        self.conf["image_id"] = args.image_id
        self.conf["job_type"] = args.job_type
        self.conf["ploy"] = self.set_ploy()
        self.conf["cluster_job_id"] = ""
        self.conf["cluster_type_id"] = 1
        self.conf["frame_id"] = int(self.conf["frame_id"] if "frame" in self.conf else "0")
        self.conf["eval_cmd"] = self.conf["eval_cmd"] \
            if "eval_cmd" in self.conf else "echo 'nothing to eval'"
        self.conf["infer_cmd"] = self.conf["infer_cmd"] \
            if "infer_cmd" in self.conf else "echo 'nothing to infer'"
        self.script_files = self.set_scrpt_files()

    def set_scrpt_files(self):
        model_path = self.conf["conf_dir"] if "conf_dir" in self.conf else self.conf["model"]
        frame = bm.Frame.VALUES_TO_NAMES[self.conf["frame_id"]]
        cluster = bm.ClusterType.VALUES_TO_NAMES[self.conf["cluster_type_id"]]
        abs_file_path = os.path.join(base_conf.ROOT_PATH, "files/%s/%s/%s" %
                                     (frame, cluster, model_path))
        return utils.load_folder_files(abs_file_path, False, ('.py', '.sh'))

    def submit_job(self):
        # paddlecloud 上的作业需要传入thridparty config
        model_path = self.conf["conf_dir"] if "conf_dir" in self.conf \
            else self.conf["model"]
        job_conf_path = os.path.join(base_conf.ROOT_PATH, "files/%s/%s/%s/config.conf"
                        % (bm.Frame.VALUES_TO_NAMES[self.conf["frame_id"]],
                        bm.ClusterType.VALUES_TO_NAMES[self.conf["cluster_type_id"]],
                        model_path))
        with open(job_conf_path, 'r') as file_obj:
            jobconf = file_obj.read()

        self.conf["body"]["jobConf"] = jobconf

        # paddlecoud 配置train.py 等脚本文件
        for file in self.script_files:
            with open(file, 'r') as file_obj:
                train = file_obj.read()
                if 'train.py' in file:
                    if isinstance(self.conf["run_cmd"], str):
                        train = train.replace('cmd = "placeholder"', 'cmd = "%s"'
                                          % self.conf["run_cmd"])
                    else:
                        train = train.replace('"placeholder"', '%s'
                                              % self.conf["run_cmd"])
                    train = train.replace("run_env", "%s_%s"
                    %(self.conf["run_machine_tpye"], self.conf["run_rpc_type"]))
                #指定运行paddle特定版本
                if 'before_hook.sh' in file:
                    if self.conf["image_id"] != 'latest':
                        image_version = bm.Image.objects.filter(frame_id=
                                    self.frame_id).filter(image_id=self.conf["image_id"])[0].version
                    else:
                        image_version = helper.get_frame_latest_version(self.conf["frame_id"]).version
                    train = train.replace("image_version_holder", str(image_version))
                    train = train.replace("model_holder", self.conf["model"])
                    train = train.replace("frame_holder",
                                          bm.Frame.VALUES_TO_NAMES[self.conf["frame_id"]])
            api.save_file(train, file.split("/")[-1] if os.name == 'posix' else file.split("\\")[-1])

        response = json.loads(api.post_job(self.conf["body"]))
        try:
            self.conf["cluster_job_id"] = response["data"]["jobId"]
        except KeyError as ke:
            error_msg = "post job failed, respone is {}".format(str(response))
            raise myexception.ResponseError(error_msg)
        return response

    @property
    def job_type(self):
        """nothing"""
        return self.conf["job_type"]
