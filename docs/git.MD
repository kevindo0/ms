### 1、Error

### 2、使用
#### 1. 命令
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
#### 2. git命令自动补全功能
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
#### 3. git stash
常用git stash命令：
* git stash save "save message": 执行存储时，添加备注，方便查找，只有git stash 也要可以的，但查找时不方便识别。
* git stash list: 查看stash了哪些存储
* git stash show: 显示做了哪些改动，默认show第一个存储,如果要显示其他存贮，后面加stash@{$num}，比如第二个 git stash show stash@{1}
* git stash show -p: 显示第一个存储的改动，如果想显示其他存存储，命令：git stash show  stash@{$num}  -p ，比如第二个：git stash show  stash@{1}  -p
* git stash apply: 应用某个存储,但不会把存储从存储列表中删除，默认使用第一个存储,即stash@{0}，如果要使用其他个，git stash apply stash@{$num} ， 比如第二个：git stash apply stash@{1} 
* git stash pop: 命令恢复之前缓存的工作目录，将缓存堆栈中的对应stash删除，并将对应修改应用到当前的工作目录下,默认为第一个stash,即stash@{0}，如果要应用并删除其他stash，命令：git stash pop stash@{$num} ，比如应用并删除第二个：git stash pop stash@{1}
* git stash drop stash@{$num}: 丢弃stash@{$num}存储，从列表中删除这个存储
* git stash clear: 删除所有缓存的stash

