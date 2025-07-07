

root用户

普通用户无法在root目录下创建目录，在HOME目录内不限

su命令-Switch User

su [-] [用户名]

-

-表示加载环境变量

sudo命令，为普通的命令授权，以root身份执行

Switch

为普通用户配置sudo认证

-

-

打开  /etc/sudoers

在文末添加：用户名 ALL=（ALL） ＋tab键  NOPASSWD：ALL

(48条消息) Linux给普通用户添加sudo权限_linux添加一个普通用户_binbin-create的博客-CSDN博客

用户、用户组管理

创建用户组：groupadd + 用户组名

删除用户组：groupdel + 用户组名

创建用户：useradd [-g -d] 用户名

-

-

-g指定用户组

-d指定用户HOME钆，不指定，home路(cid:1708)默认/home/用户名

删除用户：userdel [-r] 用户名

查看用户所属组：id 用户名

修改用户所属组：usermod

查看当前系统有哪些用户：getent passwd。查看哪些组：getent group

-

共7份信息，分别是密码x、用户组ID、组ID、描述信息、HOME目录、执行终端默认bash

查看权限管控信息

