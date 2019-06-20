pip uninstall -y torch
#在执行过程中被替换image 版本
image_version=image_version_holder
echo "my_job_image_version=$image_version"
echo "my_job_frame=frame_holder"
echo "my_job_model=model_holder"
image_name="torch-"$image_version"-cp36-cp36m-manylinux1_x86_64.whl"
curl -O "http://10.62.51.15:8208/pytorch_images/$image_name"
pip install $image_name
echo "end install pytorch"