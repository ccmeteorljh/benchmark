pip uninstall -y tensorflow-gpu
pip uninstall -y tensorflow
#在执行过程中被替换image 版本
image_version=image_version_holder
echo "my_job_image_version=$image_version"
echo "my_job_frame=frame_holder"
echo "my_job_model=model_holder"
image_name="tensorflow_gpu-"$image_version"-cp27-cp27mu-manylinux1_x86_64.whl"
curl -O "http://xx.xx.xx.xx:xxxx/tensorflow_images/$image_name"
pip install $image_name
echo "end install tensorflow"
pip install requests
echo "end install requests"

cp -r /ssd1/ljh_benchmark/tensorflow/models /home/crim
#替换这部分数据准备
ln -s /ssd1/ljh_benchmark/tensorflow/dataset/ILSVRC2012/tf_records /home/crim/models/tf_records
