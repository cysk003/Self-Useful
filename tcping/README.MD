本文链接：https://www.8a.hk/news/content/2785.html

Ubuntu安装并使用TCP测试工具TCPing

发布时间：2022/8/26 13:28:40
香港云服务器
image.png
TCPing是基于TCP协议的一种Ping命令，用来测试数据包能否通过TCP协议到到达目标主机（其实就是抄上面的描述）。他又一大特点，就是可以监听某个端口的状态，在禁Ping的时候，也可以检测网络连通率。
安装
1、TCPing依赖项：tcptraceroute
apt install -y tcptraceroute
2、下载TCPing到/usr/bin目录
wget http://www.vdberg.org/~richard/tcpping -O /usr/bin/tcping
3、赋予TCPing工具执行权限
chmod +x /usr/bin/tcping
使用
tcping [目标主机IP] [端口]（默认是：80）
如：
tcping www.baidu.com 443# 或tcping www.baidu.com