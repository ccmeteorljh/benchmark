pip uninstall -y tensorflow-gpu
pip uninstall -y tensorflow
#在执行过程中被替换image 版本
image_version=image_version_holder
echo "my_job_image_version=$image_version"
echo "my_job_frame=frame_holder"
echo "my_job_model=model_holder"
image_name="tensorflow_gpu-"$image_version"-cp27-cp27mu-manylinux1_x86_64.whl"
curl -O "http://10.62.51.15:8208/tensorflow_images/$image_name"
pip install $image_name
echo "end install tensorflow"
pip install requests
echo "end install requests"