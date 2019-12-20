### 1、Error

### 2、使用
1. 命令
```bash
# 删除本地分支
git branch -d <BranchName>
# 删除远程分支
git push origin -d <BranchName>
# 将某个远程主机的更新，全部取回本地
git fetch
# 查看远程分支和本地分支的对应关系
git remote show origin
# 删除远程已经删除过的分支
git remote prune origin
```
2. git命令自动补全功能
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
