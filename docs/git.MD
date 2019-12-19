### 1、Error

### 2、使用
1. git命令自动补全功能
```bash
# 下载git-completion.bash 并放到home 目录下：
curl https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash -o ~/.git-completion.bash
# 将如下行放到.bash_profile.sh 文件中
if [ -f ~/.git-completion.bash ]; then 
	. ~/.git-completion.bash 
fi
# 生效配置
source ~/.bash_profile
```