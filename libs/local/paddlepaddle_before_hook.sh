pip uninstall -y paddlepaddle-gpu
pip uninstall -y paddlepaddle
#在执行过程中被替换image 版本
image_version=image_version_holder
echo "my_job_image_version=$image_version"
echo "my_job_frame=frame_holder"
echo "my_job_model=model_holder"
image_name="paddlepaddle_gpu-"$image_version"-cp27-cp27mu-linux_x86_64.whl"
image_name_withversion=$image_name'.cuda_holder'
wget http://10.62.51.15:8000/$image_name_withversion
wget http://10.62.51.15:8108/numpy-1.14.0-cp27-cp27mu-manylinux1_x86_64.whl
wget http://10.62.51.15:8108/matplotlib-2.2.3-cp27-cp27mu-manylinux1_x86_64.whl
mv $image_name_withversion $image_name
pip install matplotlib-2.2.3-cp27-cp27mu-manylinux1_x86_64.whl
pip uninstall -y numpy
pip install numpy-1.14.0-cp27-cp27mu-manylinux1_x86_64.whl
pip install $image_name
echo "end install paddle"