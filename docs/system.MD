### 1. 问题解决
#### 1. ssh免密码登录配置方法
```bash
ssh-keygen -t rsa
# 方法一 ssh-copy-id
ssh-copy-id userb@host-server
# 方法二 copy id_rsa.pub to server authorized_keys文件中
cat ~/.ssh/id_rsa.pub | ssh -p 22 user@host ‘cat >> ~/.ssh/authorized_keys’
```
