#/bin/bash

#error_message='Not_enough_gpu_cards'
#var=`python get_gpu.py_holder --gpu_num $3`
#if [ $var = $error_message ]
#then
#    echo $var
#else
#    nvidia-docker run --name $1 \
#    -v /home/work:/home/work \
#    -v /usr/bin/nvidia-smi:/usr/bin/nvidia-smi \
#    --net=host \
#    --privileged \
#    -d $2 \
#    /bin/bash \
#    -c "sh container_run.sh" > /tmp/$1 &
#    id=`cat /tmp/$1`
#    echo $id
#    #docker rm -f $1
#fi
if [[ $2 =~ "paddle" ]]
then
    cmd="export LD_LIBRARY_PATH=/home/work/cudnn/cudnn_v7/cuda/lib64/:/home/work/qa_test/lib/:/usr/lib64/mlnx_ofed/valgrind:/usr/lib/x86_64-linux-gnu:/usr/local/nvidia/lib:/usr/local/nvidia/lib64;sh container_run.sh_holder $3 $4"
else
    cmd="sh container_run.sh_holder $3 $4"
fi
nvidia-docker run --name $1 \
-v /home/work:/home/work \
-v /ssd1:/ssd1 \
-v /usr/bin/nvidia-smi:/usr/bin/nvidia-smi \
-v /usr/bin/ibdev2netdev:/usr/bin/ibdev2netdev \
-v /usr/bin/ib_write_bw:/usr/bin/ib_write_bw \
-v /usr/bin/ofed_info:/usr/bin/ofed_info \
-v /etc/libibverbs.d:/etc/libibverbs.d \
-v /usr/lib64/mlnx_ofed/valgrind:/usr/lib64/mlnx_ofed/valgrind \
--net=host \
--privileged \
-d $2 \
/bin/bash \
-c  "$cmd" > /tmp/$1 &
#等待容器启动时间10s,获得容器id
sleep 10
id=`cat /tmp/$1`
echo $id
#docker rm -f $1
