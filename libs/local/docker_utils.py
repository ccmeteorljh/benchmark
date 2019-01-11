import os
import numpy as np
import argparse
import commands
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument(
    "--gpu_num",
    type=int,
    default=1,
    help="the num of gpu you wanted (default: %(default)d)")

def check_enough_gpu(gpu_num):
    """
    检查GPU是否满足job运行条件
    :param gpu_num:
    :return:
    """
    os.system('nvidia-smi -q -d Memory |grep -A4 GPU|grep Free >gpu_num_tmp')
    memory_gpu = [int(x.split()[2]) for x in open('gpu_num_tmp', 'r').readlines()]
    memory_gpu_with_index = enumerate(memory_gpu)
    memory_gpu_sorted = filter(lambda x: x[1] >= 22902, memory_gpu_with_index)
    if len(memory_gpu_sorted) < gpu_num:
        return False
    index = [x[0] for x in memory_gpu_sorted][:gpu_num]
    index_str = [str(x) for x in index]
    index_str = ','.join(index_str)
    os.system('rm -f gpu_num_tmp')
    return index_str


def check_container_status(container_id):
    """
    检查容器状态
    :param container_id:
    :return:
    """
    cmd = "docker ps -a|grep {}".format(container_id)
    _, out_put = commands.getstatusoutput(cmd)
    if not out_put:
        return "running"
    if 'Exited' in out_put:
        os.system("docker rm {}".format(container_id))
        return "success"
    elif 'Up' in out_put:
        return "running"
    else:
        print("no support output {}".format(out_put))
        return 'fail'


if __name__ == '__main__':
    args = parser.parse_args()
    index_str = check_enough_gpu(args.gpu_num)
    if not index_str:
        print("Not_enough_gpu_cards")
        exit(0)
    else:
        print(index_str)
