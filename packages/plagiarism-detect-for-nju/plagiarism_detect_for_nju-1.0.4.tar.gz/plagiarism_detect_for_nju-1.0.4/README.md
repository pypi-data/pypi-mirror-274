# 查重工具

本工具可以根据从`hustoj`后台导出的竞赛log文件, 自动分离出每个人的最后一次ac提交并存储, 之后使用`jplag`查重.

## 用法

```text
usage: plag4nju4cprog [-h] [-d DIR] [-s SUFFIX] [-a] [-o] [-r] [-p] [-n NTOKS] [-j JAR_PATH] log

plagiarism detect from hustoj's logfile, multi-process

positional arguments:
  log                   log file u want to cut

options:
  -h, --help            show this help message and exit
  -d DIR, --dir DIR     target directory u want to place the cut files in. default to the same name as the log file
  -s SUFFIX, --suffix SUFFIX
                        suffix you want to add. i have no idea what this will do.
  -a, --all             whether to include all pairs in result
  -o, --old             use old method for cpp code
  -r, --remove          remove existing directory if set to true
  -p, --parallel        turn on to parallel
  -n NTOKS, --ntoks NTOKS
                        how many identical tokens will be recognized as copy. higher means more tolerant. default to 100
  -j JAR_PATH, --jar_path JAR_PATH
                        where jplag jar is. u need to manage java environment yourself. default to "./jplag.jar"
```

## JPlag

jplag仓库: [jplag](https://github.com/jplag/JPlag).

需要自己下载。作者自己用4.3.0测试过，更新的版本需要自己测试。

## 怎么看报告

运行后会首先创建文件夹存储切分出来的代码文件, 在这个文件夹下随后会产生一个`results-%dtoks`的文件夹, 名字的意思是在`%d`的敏感度下查重的结果. 文件夹里面会有若干个以题目编号为名字的`zip`格式文件, 每个代表那一题的查重结果.

访问[这个网站](https://jplag.github.io/JPlag/), 把`zip`文件拖进去就可以看查重结果了.
