# benchmark
dltp benchmark
---
Benchmark
===
paddle
快速开始
---
以下是该库的简要目录结构及说明：

```
benchmark
├── conf                 # 日志服务器地址，数据库配置等
├── files                # 存放些job提交的必须文件(各个模型下启动docker的环境准备，数据下载等，或者paddlecoud上所需文件)
├── libs                 # 该自动化框架的库
|   |——— common          # 存放一些工具，日志定义，数据库连接类
|   |——— job_scheduler   # 作业调度，模型运行日志抽取，VisualDL画图等lib
|   |——— local           # 本地docker启动，GPU卡检查等工具
|   |——— paddlecloud     # paddlecloud依赖api
|   |——— qianmo          # 暂未开发
├── models               # 数据库部分
├── output               # 日志输出目录
├── system               # 具体的job配置文件以及启动脚本
|__ README.md            # 文档

```
如何构建、安装、运行

1、cd system   
2、python run_cases.py   

#### 参数列表如下：
* --filename         
`default='system/paddle_cases/local/language_model'   即，运行local模式下的模型`
* ----frame_id   
`default='0'  即，默认为paddlepaddle 深度学习框架；` 0：paddlepaddle，1：tensorflow，2：pytorch，3：theano，4：caffe
* --image_id      
`default='latest'  默认运行所选框架的最新版本，从数据库中读取；`
* --job_type        
` default='0', 设定本次job是benchmark例行运行，还是实验性测试`


测试
---
`python run_cases.py --filename system/paddle_cases`

如何贡献
---
贡献patch流程及质量要求

版本信息
---
本项目的各版本信息和变更历史可以在[这里][changelog]查看。
