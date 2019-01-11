import os
import sys
import argparse
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

print sys.path
from libs.common import log
from conf import base_conf
from libs.job_scheduler.runner import JobRunner


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--filename",
    type=str,
    default='system/paddle_cases/local/language_model',
    help="The cases files. (default: %(default)d)")

parser.add_argument(
    "--frame_id",
    type=int,
    default=0,
    help="run frame. (default: %(default)d)")

parser.add_argument(
    "--image_id",
    type=str,
    default='latest',
    help="run env of paddle. (default: %(default)d)")

parser.add_argument(
    "--code_branch",
    type=str,
    default='develop',
    help="run models repos code branch. (default: %(default)d)")

parser.add_argument(
    "--job_type",
    type=int,
    default=0,
    help="test or benchmark. (default: %(default)d)")

if __name__ == "__main__":
    logger = log.MyLog.get_log()
    args = parser.parse_args()
    logger.info("---------------------begin job----------------------")
    pbr = JobRunner(os.path.join(base_conf.ROOT_PATH, args.filename), args)
    pbr.run()
