#Bilibili排行榜获取爬虫1.0
<br>
##1、相关支持
- PyQuery（需下载）
- selenium（需下载）
- re
- json
- Chrome浏览器和ChromeDriver（需下载）

##2、使用方法
输入bilibili排行榜网址即可，例如 https://www.bilibili.com/ranking?spm_id_from=333.11.banner_link.1#!/all/0/0/3/ 输入其他网址不保证运行。

##3、注意事项
可能会出现输入网址后按回车直接进入浏览器打开的情况（在Pycharm是这样的），只需要在输入完网址后输入一个空格再回车就能正常运行。

##4、数据保存
爬取结果保存在data.json。**注意：每次重新运行都会删除原有数据文件并重新生成，如果需要保留结果则只需要在运行完后重命名或者移到其他位置。**