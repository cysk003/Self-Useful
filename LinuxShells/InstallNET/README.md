# 
# 一键DD系统，以及Error, Not found interfaces config.解决办法

萌咖一键网络重装为 debian9+/ubuntu16.04+

密码：MoeClub.org

#先切换到root权限
sudo -i运行:#Debian/Ubuntu:
apt-get update#RedHat/CentOS:
yum update#确保安装了所需软件:
#Debian/Ubuntu:
apt-get install -y xz-utils openssl gawk file#RedHat/CentOS:
yum install -y xz openssl gawk file#下载及说明:
wget --no-check-certificate -qO InstallNET.sh 'https://moeclub.org/attachment/LinuxShell/InstallNET.sh' && chmod a+x InstallNET.sh
Usage:        bash InstallNET.sh      -d/--debian [dist-name]                                -u/--ubuntu [dist-name]                                -c/--centos [dist-version]                                -v/--ver [32/i386|64/amd64]
                                --ip-addr/--ip-gate/--ip-mask                                -apt/-yum/--mirror                                -dd/--image                                -a/-m# dist-name: 发行版本代号
# dist-version: 发行版本号
# -apt/-yum/--mirror : 使用定义镜像
# -a/-m : 询问是否能进入VNC自行操作. -a 为不提示(一般用于全自动安装), -m 为提示.
#安装debian9 (-firmware 额外驱动支持)
bash <(wget --no-check-certificate -qO- 'https://moeclub.org/attachment/LinuxShell/InstallNET.sh') -d 9 -v 64 -a -firmware
#安装ubuntu16.04 (-firmware 额外驱动支持)
bash <(wget --no-check-certificate -qO- 'https://moeclub.org/attachment/LinuxShell/InstallNET.sh') -u 16.04 -v 64 -a -firmware
#安装ubuntu18.10 (-firmware 额外驱动支持)
bash <(wget --no-check-certificate -qO- 'https://moeclub.org/attachment/LinuxShell/InstallNET.sh') -u 18.10 -v 64 -a -firmware
#备用
https://www.ucblog.net/shell/InstallNET.sh
安装Debian9和Ubuntu16出现以下问题：
Auto Mode insatll [Debian] [stretch] [amd64].
[Debian] [stretch] [amd64] Downloading...
Error, Not found interfaces config.
解决
ssh运行下面 两个命令就可以dd了

命令1

mkdir /etc/network/interfaces.d

命令2

echo "# This file describes the network interfaces available on your system
# and how to activate them. For more information, see interfaces(5).

source /etc/network/interfaces.d/*

# The loopback network interface
auto lo
iface lo inet loopback

# The primary network interface
allow-hotplug ens3
iface ens3 inet dhcp

" > /etc/network/interfaces

重装后SSH登录，用户名root,密码：MoeClub.org

别忘记修改root密码

root@baidu:~# passwd
Enter new UNIX password:
连续输入两次新密码就可以