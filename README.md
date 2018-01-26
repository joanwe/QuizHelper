# QuizHelper
手机答题辅助工具,用的是搜狗的api,无需手机截图OCR,支持冲顶/芝士/西瓜/花椒/一直播,显示搜狗推荐答案及参考/百度搜索结果总数及各单项百度第一页出现次数
![Screenshots](https://github.com/joanwe/QuizHelper/blob/master/Screenshots.png)
# 使用步骤
1. 安装python3以及pip
2. 安装所需python包

```
pip3 install prettytable  
pip3 install aiohttp
pip3 install bs4
```
3. Win用cmd,Mac用终端先转到文件所在目录及用以下方式运行
```
python3 QuizHelper.py
```
4. 开始时数字键输入选择答题app
# 更新日志
+ 2018.01.26
 + 采用了异步IO(asyncio&aiohttp)的方式并发获取搜索数据
 + 细分代码模块,优化了首页出现次数算法
 + 添加了一直播黄金十秒入口
