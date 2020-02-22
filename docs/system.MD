### 1. 问题解决
#### 1. ssh免密码登录配置方法
```bash
ssh-keygen -t rsa
# 方法一 ssh-copy-id
ssh-copy-id userb@host-server
# 方法二 copy id_rsa.pub to server authorized_keys文件中
cat ~/.ssh/id_rsa.pub | ssh -p 22 user@host ‘cat >> ~/.ssh/authorized_keys’
```
#### 2. 文件权限
```bash
# 添加人员
useradd -m duchao
# 添加组
groupadd gname
# 将人员添加进组 append
usermod -a -G gname duchao
gpasswd -a duchao
# 将人员移除出组 
gpasswd -d duchao
# 修改文件所属组
chown -R duchao:gname 文件
# 修改文件权限
chmode -R 0777 文件
# 查看组成员
cat /etc/group | grep gname
# 查看用户所属的组使用命令
groups duchao
```
