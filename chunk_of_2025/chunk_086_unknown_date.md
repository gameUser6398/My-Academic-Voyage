

wget https://repo.anaconda.com/miniconda/Miniconda3-py310_24.1.2-0-Linux-x86_64.sh
bash Miniconda3-py310_24.1.2-0-Linux-x86_64.sh

Managing environments — conda 24.4.1.dev85 documentation

(8 条消息) 请问大神们，pip install 和conda install有什么区别吗？ - 知乎 (zhihu.com)

conda包管理
创建环境：conda create -n py38_torch python=3.8

1.

添加源：conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main

重置所有源：conda config --remove-key channels

克隆已有环境：conda create -n py39_torch --clone py38_torch

2.

torch安装_安装torch-CSDN博客

conda安装torch、cuda
安装torch库等：
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

来自 <https://pytorch.org/get-started/locally/>

pip安装torch、cuda
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

来自 <https://pytorch.org/get-started/locally/>

Python | Conda pack 进行环境打包 - 知乎 (zhihu.com)

