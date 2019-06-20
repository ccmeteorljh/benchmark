export image_version=`cat /home/crim/run.log |grep 'my_job_image_version'|awk -F '=' '{print $2}'`
export model=`cat /home/crim/run.log |grep 'my_job_model'|awk -F '=' '{print $2}'`
export frame=`cat /home/crim/run.log |grep 'my_job_frame'|awk -F '=' '{print $2}'`
job_id=`cat /home/crim/run.log |grep 'job_id'|cut -d ' ' -f5|cut -d '=' -f2`
trainer_id=`cat /home/crim/run.log |grep 'PADDLE_TRAINER_ID'|cut -d'=' -f2`
export log_name=$model'_'$job_id'_'$trainer_id
training_role=`cat /home/crim/run.log |grep 'TRAINING_ROLE'|cut -d= -f2`
tmp_name=${log_name}"_"${frame}"_"${image_version}
rm /home/work/ljh_benchmark/logs/$tmp_name
cat /home/crim/run.log >> /home/crim/$log_name
cat /home/crim/end_hook.log >> /home/crim/$log_name
cat /home/crim/gpu_use_train.log >> /home/crim/$log_name
cat /home/crim/gpu_use_infer.log >> /home/crim/$log_name
cp /home/crim/$log_name /home/work/ljh_benchmark/logs/$tmp_name
python post_benchmark_log.py_holder