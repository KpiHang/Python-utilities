

## other2utf8.py
文件编码转为utf-8格式，使用方式：
1. 查看文件编码格式：
```shell
$ python other2utf8.py ~/Desktop/test.txt
本文件编码为：GB2312
```
2. 更改文件编码为utf-8：
```shell
$ python other2utf8.py ~/Desktop/test.txt --change

本文件编码为：GB2312
编码已经转为：utf-8。
```
再次查看确认：
```shell
$ python other2utf8.py ~/Desktop/test.txt
本文件编码为：utf-8
```