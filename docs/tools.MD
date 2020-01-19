### 1. Jupyterhub
#### 1. 安装
```bash
docker run -d -ti --name jhub -p 8888:8888 ubuntu:16bp
docker exec -ti jhub bash
# 安装 jupyterlab jupyterhub
pip install jupyterlab
pip install jupyterhub
# 安装node10
curl -sL https://deb.nodesource.com/setup_10.x | bash -
apt-get install -y nodejs build-essential
# 安装configureable-http-proxy
npm install -g configurable-http-proxy
# 检查
jupyterhub -h
configurable-http-proxy -h
# 生成配置文件
mkdir /etc/jupyterhub
jupyterhub --generate-config -f /etc/jupyterhub/jupyterhub_config.py
# 启动
jupyterhub -f /etc/jupyterlab/jupyterhub_config.py
# 生成用户及密码
useradd -m duchao
passwd duchao
```
jupyterhub_config.py

* [CAS](https://github.com/cwaldbieser/jhub_cas_authenticator)
```bash
c.JupyterHub.port = 8888
c.Spawner.cmd = ['jupyter-labhub']
# admin 登录
c.Authenticator.admin_users = {'duchao'}
c.JupyterHub.load_groups = {"grow": ['duchao']}

# pip install jhub_cas_authenticator
c.JupyterHub.authenticator_class = 'jhub_cas_authenticator.cas_auth.CASAuthenticator'
c.CASAuthenticator.cas_service_url = ''
c.CASAuthenticator.cas_login_url = ''
c.CASAuthenticator.cas_service_validate_url = ''
```

### 2. an
```bash
conda list  # 查看安装了哪些包。
conda env list 或 conda info -e  # 查看当前存在哪些虚拟环境
conda update conda  # 检查更新当前conda
conda create -n py27 python=2.7
conda create -n py35 python=3.5
source active py27（py35） # 激活虚拟环境
conda install -n py35 [包名] # 将包安装到虚拟环境下
deactivate py35 # 关闭虚拟环境
conda remove -n py27 --all # 移除虚拟环
conda remove --name $py35 $package_name # 移除环境中的某个包
```
