# gameDownloadList
gameDownloadList




## 拉代码后 创建所有分支

``` 
vi t.txt
origin/1003480
origin/1003890
origin/1004240
origin/1004490
origin/1005240
origin/1005460
origin/1007040
origin/1007350
origin/1008510
origin/1008710
origin/10090
origin/1009290
origin/1009560
origin/1010750
origin/1011230
origin/1012030
origin/1012460
origin/1012560
origin/1012630
origin/HEAD -> origin
data
main


cat t.txt | grep -v "origin/HEAD" | awk  -F '/'  'BEGIN {}  { print $2 } END {}' | xargs -I {}   echo "aaa {} bbb {} ccccc" 


git branch -r | grep -v "origin/HEAD" | awk  -F '/'  'BEGIN {}  {print $2 } END {}' | xargs -I {}  /usr/bin/git checkout -b {} origin/{}



将本地所有分支与远程保持同步 git fetch --all --prune --tags
最后拉取所有分支代码 git pull --all


Git命令集十四——抓取命令
    Git中提供的fetch命令用于将远端的更新抓取到本地仓库中。 
1.git fetch <repository> <branchName>
    从指定的远端抓取指定分支的更新。

2.git fetch --all
    抓取所有远端的所有更新。

3.git fetch <repository> <branchName> --prune 
    抓取前删除远程上不在跟踪的引用。

4.git fetch <repository> <branchName> --tags
    抓取远程分支上的所有标签。

5.git fetch <repository> <branchName> --progress
    输出抓取进度。

6.git fetch <repository> <branchName> --ipv4
    使用IPv4地址。忽略IPv6地址。

7.git fetch <repository> <branchName> --ipv6
    使用IPv6地址，忽略iPV4地址。
 
```


## github 新版key 设置仓库使用指定key
```
ssh-keygen -t ed25519 -C "xxx@xx.com"


git config --local core.sshCommand "ssh -i /root/.ssh/id_ed25519"
```

 
