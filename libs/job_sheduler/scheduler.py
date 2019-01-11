import os
import sys
import multiprocessing
import time

import datetime
import models.benchmark_server.helper as helper
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from benchmark_server import benchmark_models as bm

from libs.common import exception
from libs.job_scheduler import job
from libs.common import log
from libs.job_scheduler import log_extract
from libs.job_scheduler import build_in
#from libs.job_scheduler import visualdl_paint


logger = log.MyLog.get_log()

class ClockSubmitJobProcess(multiprocessing.Process):
    """class define for submitting job to cluster timing
    """
    def __init__(self, interval, path, Log, args):
        multiprocessing.Process.__init__(self)
        self.interval = interval
        self.path = path
        self.args = args

    def submit_job(self, job_conf):
        """
        post job to cluster and start scheduler thread
        :return:
        """
        if job_conf["cluster_type_id"] == 0:
            job_instance = job.LocalJobClass(job_conf, self.args)
        elif job_conf["cluster_type_id"] == 1:
            job_instance = job.PaddleCloudJobClass(job_conf, self.args)
        elif job_conf["cluster_type_id"] == 2:
            logger.info("qianmo job")
            job_instance = job.QianMoJobClass(job_conf, self.args)
        else:
            logger.error("not suport this cluster_type_id {}".format(job_conf["cluster_type_id"]))
            return
        try:
            job_instance.submit_job()
        except exception.ResponseError as rese:
            logger.error("job[%s] failed, exception msg is [%s]"
                          % (job_instance.conf["body"]["jobName"], str(rese)))

        else:
            logger.info("job[%s] submit successed!" % (job_instance.conf["body"]["jobName"]))
            #todo
            helper.insert_job(job_instance)

    def check_if_submit_job(self, job_conf):
        """
        check
        :param job_conf:
        :return:
        """
        latest_image = helper.get_frame_latest_version(job_conf["frame_id"]).image_id
        all_status = [value for _, value in bm.JobStatus.VALUES_TO_NAMES.items()]
        ended_status = ['success', 'fail', 'killed', 'deleted']
        middle_status = ["submit", "schedule", "running", "killing", "queue"]

        pcjs = helper.get_cluster_job_info(job_conf["body"]["jobName"],
                                all_status).filter(image_id=latest_image).filter(
                                cluster_type_id=job_conf["cluster_type_id"])
        # 如果当前frame下最新版本没有对应的job，直接启动一个该版本下的作业；否则检查是否满足规则
        if not pcjs:
            return True
        elif pcjs[0].status in middle_status:
            return False
        elif pcjs[0].status in ended_status:
            pcjs = pcjs[0]
            dt_job_create = pcjs.create_time
            dt_now = datetime.datetime.now()
            #Todo 校验failed状态的job，是否会上传日志
            if pcjs.status in ('killed', 'deleted'):
                bm.Job.objects.filter(job_id=pcjs.job_id).update(
                    log_extracted='fail')
                return True
            elif pcjs.log_extracted == "fail":
                return True
            elif pcjs.log_extracted == 'no':
                return False
            elif pcjs.log_extracted == 'yes':
                return (dt_now - dt_job_create).days >= job_conf["ploy"]["submit_period"]
        else:
            logger.info("unknowed job status {}".format(pcjs[0].status))

    def check_and_submit_job(self):
        """
        check to submit job
        :return:
        """
        job_conf_list = build_in.load_jobs_by_path(self.path, self.args)
        #update job status
        build_in.update_job_status()
        for job_conf in job_conf_list:
            if self.check_if_submit_job(job_conf["test"]):
                self.submit_job(job_conf["test"])

    def run(self):
        while True:
            logger.info("check if should submit a new job")
            self.check_and_submit_job()
            print("this epoch submit job done!")
            time.sleep(self.interval * 60)


class ClockExtractResultProcess(multiprocessing.Process):
    """class define for extract result paddle-cloud job timing
    """
    def __init__(self, interval):
        multiprocessing.Process.__init__(self)
        self.interval = interval

    def check_and_extract_log(self):
        """check to extract log
        """
        extract_jobs = helper.get_final_job_with_no_extractlog()
        for job_info in extract_jobs:
            try:
                job_result, log_dict = log_extract.LogExtractRe.log_extract(job_info)
            except exception.ResponseError as rse:
                logger.error(str(rse))
            else:
                if not job_result:
                    log_extracted_status = "fail"

                else:
                    log_extracted_status = "yes"

                result_dict = build_in.construct_job_result_dict(job_info, job_result, log_dict)
                helper.insert_result(**result_dict)

                bm.Job.objects.filter(job_id=job_info.job_id).update(
                    log_extracted=log_extracted_status)
                logger.info("job {} had extracted success!".format(job_info.cluster_job_id))

    def run(self):
        while True:
            logger.info("check if should extract log")
            self.check_and_extract_log()
            print("this epoch extract log done!")
            time.sleep(self.interval * 60)


class ClockVisualDLProcess(multiprocessing.Process):
    """class define for extract result paddle-cloud job timing
    """
    def __init__(self, interval):
        multiprocessing.Process.__init__(self)
        self.interval = interval

    def run(self):
        while True:
            logger.info("check if should paint visualDL")
            #visualdl_paint.get_all_result()
            print("this epoch visualDL paint done!")
            time.sleep(self.interval * 60)


class LocalJobRunProcess(multiprocessing.Process):
    """class define for local job run timing
    """
    def __init__(self, interval):
        multiprocessing.Process.__init__(self)
        self.interval = interval

    def run(self):
        while True:
            time.sleep(self.interval * 60)
            logger.info("check if run local job")
            submited_job= helper.get_cluster_job_info("", ["submit"]).filter(cluster_type_id=0)
            #todo sort submited_job by gpu_num in jobconf
            for job_instance in submited_job:
                try:
                    if job.LocalJobClass.localjob_run(job_instance):
                        bm.Job.objects.filter(job_id=job_instance.job_id).update(
                            status='running')
                        bm.Job.objects.filter(job_id=job_instance.job_id).update(
                            cluster_job_id=job_instance.cluster_job_id)
                        bm.Job.objects.filter(job_id=job_instance.job_id).update(
                            cluster_conf=job_instance.cluster_conf)
                        dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        bm.Job.objects.filter(job_id=job_instance.job_id).update(
                            update_time=dt)
                        # 作业启动到显卡占用可以被统计出来所需要一定的时间
                        time.sleep(30 * 60)
                        break
                except exception.ResponseError as rse:
                    bm.Job.objects.filter(job_id=job_instance.job_id).update(
                        status='fail')
                    logger.error("start container error! {}".format(job_instance.job_name))
                    dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    bm.Job.objects.filter(job_id=job_instance.job_id).update(
                        update_time=dt)

            print("this epoch local job run checking done!")
