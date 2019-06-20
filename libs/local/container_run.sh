#!/bin/bash

#获取作业运行状态
#0:running 1:exited
jobstatus(){
    if [ `grep -c "this job done" /home/crim/run.log` -gt 0 ]; then
        echo "Found!"
        return 1
    else
        return 0
    fi
}
mkdir /home/crim
echo ---------IN docker begin------
#todo 此处预留给有后续多环境benmark需求时候设置的一些环境变量
#设置容器环境
env_holder
#安装框架包，准备代码和数据
sh before_hook_holder >> /home/crim/run.log 2>&1

#进入到模型目录运行脚本
cd workdir_holder
pwd
export CUDA_VISIBLE_DEVICES=$1
#export FLAGS_fraction_of_gpu_memory_to_use=0.01
echo "job_id=$2" >> /home/crim/run.log
echo 'TRAINING_ROLE=trainer' >> /home/crim/run.log
echo 'PADDLE_TRAINER_ID=0' >> /home/crim/run.log
echo cuda_visible_devices=$1 >> /home/crim/run.log

#多卡下会hang住，需要unset该环境变量
unset NCCL_LAUNCH_MODE

#记录job开始时间
echo "myjob_start_time="$(date "+%Y%m%d-%H%M%S") >> /home/crim/run.log
gpu_id=`echo $CUDA_VISIBLE_DEVICES |cut -c1`


#>>>>>>>>>>>>>>>>>>>>train阶段开始>>>>>>>>>>>>>>>>>>>>>>>>

#train model
echo "begin trainning cmd" >> /home/crim/run.log 2>&1
#启动训练gpu_memory统计
nvidia-smi --id=$gpu_id --query-compute-apps=used_memory --format=csv -lms time_holder > /home/crim/gpu_use_train.log 2>&1 &
gpu_memory_train_pid=$!
run_cmd_holder >> /home/crim/run.log 2>&1
echo "myjob_train_end_time="$(date "+%Y%m%d-%H%M%S") >> /home/crim/run.log
#结束gpu_memory统计
kill -9 $gpu_memory_train_pid


#>>>>>>>>>>>>>>>>>>>>eval阶段开始>>>>>>>>>>>>>>>>>>>>>>>>
#eval model
echo "begin eval cmd" >> /home/crim/run.log 2>&1
eval_cmd_holder >> eval.txt
echo "myjob_eval_end_time="$(date "+%Y%m%d-%H%M%S") >> /home/crim/run.log
cat eval.txt >> /home/crim/run.log 2>&1


#>>>>>>>>>>>>>>>>>>>> GPU infer阶段开始>>>>>>>>>>>>>>>>>>>>>>>>
#infer model with gpu
nvidia-smi --id=$gpu_id --query-compute-apps=used_memory --format=csv -lms time_holder > /home/crim/gpu_use_infer.log 2>&1 &
gpu_memory_infer_pid=$!
echo "begin inference cmd with gpu" >> /home/crim/run.log 2>&1
infer_cmd_holder >> /home/crim/run.log 2>&1
echo "myjob_gpu_infer_end_time="$(date "+%Y%m%d-%H%M%S") >> /home/crim/run.log
kill -9 $gpu_memory_infer_pid


#>>>>>>>>>>>>>>>>>>>> CPU infer阶段开始>>>>>>>>>>>>>>>>>>>>>>>>
#infer model with cpu
unset CUDA_VISIBLE_DEVICES
echo "begin inference cmd with cpu" >> /home/crim/run.log 2>&1
infer_cmd_holder >> /home/crim/run.log 2>&1
echo "myjob_cpu_infer_end_time="$(date "+%Y%m%d-%H%M%S") >> /home/crim/run.log


#>>>>>>>>>>>>>>>>>>>>全部结束>>>>>>>>>>>>>>>>>>>>>>>>
echo "this job done" >> /home/crim/run.log

#检查作业是否执行完毕
while true
do
    jobstatus
    js=$?
    if [ $js -eq 1 ]; then
       echo "done"
       break
    else
       sleep 30
    fi
done

#记录job结束时间
echo "myjob_end_time="$(date "+%Y%m%d-%H%M%S") >> /home/crim/run.log
#上传日志文件
sh end_hook_holder >> /home/crim/end_hook.log 2>&1
echo ---------IN docker end------


