# QuizHelper
手机答题辅助工具,提取搜狗汪仔答题助手api,无需手机截图OCR,显示搜狗推荐答案及参考/百度搜索结果总数及词频计数,支持冲顶/芝士/西瓜/花椒/一直播/优酷疯狂夺金
![Screenshots](https://github.com/joanwe/QuizHelper/blob/master/Screenshots.png)
# Tips
1. 安装python3以及pip
2. 安装所需python包

```
pip3 install prettytable  
pip3 install aiohttp
pip3 install bs4
pip3 install websocket-client
```
3. 安装lxml解析器 [知乎搜索具体安装方法](https://www.zhihu.com/question/30047496/answer/108902875)
4. 终端先转到文件所在目录再输入以下命令

```
python3 QuizHelper.py
```
5. 开始时数字键输入选择答题app

# Update
* 2018.01.26
  - 采用了异步IO(asyncio&aiohttp)的方式并发搜索数据
  - 重构代码模块,修改了词频计数方式
  - 添加了一直播黄金十秒入口
* 2018.01.31
  * 修改了数据获取方式,使搜索结果和词频计数更加精确
  * 修复了推荐答案无法与搜狗同步显示的bug
* 2018.02.02
  * 更新了搜狗json数据的提取方式
  * 修复了因404响应导致程序奔溃的bug
* 2018.02.07
  * 添加了优酷疯狂夺金入口
  * 采用了从简单搜索websocket协议中获取问题及选择答案,比搜狗快了2~3秒
  * 添加了答题app开场时间及奖金提示
  * 推荐答案还是采用的搜狗答案
* 2018.02.08
  * 更新了搜狗汪仔答题api
  * 采用搜狗与简单搜索双擎模式,更快获取问题与答案
  * 因搜狗最近频繁更新,取消了新的答题入口及开场时间和奖金提示

# Next

- 欢迎有缘人在Issues中提出建议及改进,谢谢^^

  ​


