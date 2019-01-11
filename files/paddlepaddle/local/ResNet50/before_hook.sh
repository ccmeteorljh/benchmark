pip uninstall -y paddlepaddle-gpu
pip uninstall -y paddlepaddle
#在执行过程中被替换image 版本
image_version=image_version_holder
echo "my_job_image_version=$image_version"
echo "my_job_frame=frame_holder"
echo "my_job_model=model_holder"
image_name="paddlepaddle_gpu-"$image_version"-cp27-cp27mu-linux_x86_64.whl"
image_name_87=$image_name'.cuda87'
wget http://xx.xx.xx.xx:8000/$image_name_87
wget http://xx.xx.xx.xx:8108/numpy-1.14.0-cp27-cp27mu-manylinux1_x86_64.whl
wget http://xx.xx.xx.xx:8108/matplotlib-2.2.3-cp27-cp27mu-manylinux1_x86_64.whl
mv $image_name_87 $image_name
pip install matplotlib-2.2.3-cp27-cp27mu-manylinux1_x86_64.whl
pip uninstall -y numpy
pip install numpy-1.14.0-cp27-cp27mu-manylinux1_x86_64.whl
pip install $image_name
echo "end install paddle"

cp -r /home/work/ljh_benchmark/models /home/crim
#替换这部分数据准备
sed -i '156d' /home/crim/models/fluid/PaddleCV/image_classification/reader.py
rm -rf /home/crim/models/fluid/PaddleCV/image_classification/data/ILSVRC2012
ln -s /home/work/ljh_benchmark/dataset/ILSVRC2012 /home/crim/models/fluid/PaddleCV/image_classification/data/ILSVRC2012
