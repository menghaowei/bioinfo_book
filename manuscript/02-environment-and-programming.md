# 分析环境的搭建与必要的编程技术 {#sec-ch02}

::: {.hero-book .book-chapter-summary}

## 本章提要 {#chapter-summary-02 .unnumbered}

本章帮你把生信分析的工作台搭起来：本地负责写代码、绘图和运行 AI agent，重计算交给服务器。我们先比较 Windows、Linux 和 macOS 三种本地平台，完成 WSL 与 macOS 的基础配置；再打通与服务器的连接，学习文件传输、基本 Linux 命令与 Shell 脚本，并用 VS Code 远程开发；然后在服务器上用 `apt` 安装软件，用 `conda` 与 Bioconda 搭建生信环境；接着掌握 R 与 Python 的最低必要基础，读懂 YAML 与 JSON 配置；最后装好 Claude Code、Codex、ZCode 等 AI agent，并建立项目目录、版本管理与排错的基本习惯。


:::

## 电脑、服务器与软件环境 {#sec-02-01}

选择并配置适合分析的本地工作环境。

### 生物信息学平台的构建 {#src-0090-build-up-bioinfo-platform-1}

[]{#build_up_platform}

生物信息学的分析平台由本地电脑和远端服务器两部分组成，两者分工不同。本地电脑主要承担三类工作：编辑代码，用 R 等工具绘制图形，以及运行 Claude Code、Codex、ZCode 这类 AI coding agent 辅助编程；而比对、定量这些吃算力的计算，几乎都在远端服务器上完成。因此，配置本地环境的关键不是性能，而是顺手：选择一个自己习惯的操作系统，把它配置成能写代码、能连服务器、能跑 AI agent 的工作台。本章就按这个思路展开：先选好并配置本地系统，再打通与服务器的连接和基本操作。

### Windows、Linux和macOS的选择 {#src-0090-build-up-bioinfo-platform-3}

选择本地主机系统时，评判标准与挑选服务器不同：本地不承担重计算，关键在于开发体验、与服务器环境的接近程度，以及个人的使用习惯。下面分平台简要分析。

#### Windows {#topic-02-platform-windows}

Windows 生态最普及，但与 Linux 服务器差异较大：大多数开源生信软件只提供 Linux 版本的二进制包或源代码，在 Windows 上直接编译安装历来困难。WSL 的出现改变了这一点——在 Windows 上可以获得十分接近 Linux 命令行的操作和兼容性体验（见下一节）。对已经在使用 Windows 的读者，没有必要为了生信专门更换电脑，配置好 WSL 即可。

#### Linux {#topic-02-platform-linux}

在本地直接使用 Linux 桌面（如 Ubuntu）的最大好处，是与服务器环境完全一致：同样的命令行、同样的软件安装方式，写好的脚本几乎可以原样搬上服务器。代价是日常办公和商业软件生态较弱，遇到问题需要一定的排查意愿。适合愿意把电脑完全当作开发工具使用的读者。

#### macOS {#topic-02-platform-macos}

macOS 基于 Unix，自带终端和一批常用命令行工具，与 Linux 服务器天然接近，编译安装开源软件通常也顺利；同时保留了完整的图形界面生态，作为本地主机兼顾开发与日常使用。需要注意的是，苹果芯片（Apple Silicon）的 CPU 架构与多数服务器（x86_64）不同，个别只提供 x86 版本的软件需要通过系统自带的兼容层运行。


### 在 Windows 下使用 Linux 命令行 {#src-0090-build-up-bioinfo-platform-147}

微软官方文档很好地解释了WSL（Windows Subsystem for Linux）是什么。

> 适用于 Linux 的 Windows 子系统可让开发人员按原样运行 GNU/Linux 环境 - 包括大多数命令行工具、实用工具和应用程序 - 且不会产生传统虚拟机或双启动设置开销。

#### 安装WSL {#src-0090-build-up-bioinfo-platform-153}

在Windows 10（21H2及以后）和Windows 11上，以管理员权限启动PowerShell，一条命令就可以完成安装：

```{.powershell data-book-role="code"}
wsl --install
```

`wsl --install`会自动启用所需功能、下载Linux内核并默认安装Ubuntu，完成后按提示重新启动计算机。之后可以用`wsl --list --online`查看可安装的发行版，用`wsl --install -d 发行版名称`安装其他发行版。

在更旧的Windows 10版本上，`wsl --install`不可用，需要手动启用功能（以下小节作为旧方法保留）。以管理员权限启动PowerShell，依序执行以下两个命令后重新启动计算机。

##### 启用“适用于 Linux 的 Windows 子系统”可选功能 {#src-0090-build-up-bioinfo-platform-157}


```{.powershell data-book-role="code"}
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
```

##### 启用“虚拟机平台”可选功能 {#src-0090-build-up-bioinfo-platform-163}


```{.powershell data-book-role="code"}
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
```

##### 设置WSL2为默认版本 {#src-0090-build-up-bioinfo-platform-169}

使用`wsl --install`安装时默认已经是WSL2，通常无需这一步；只有在旧系统上手动启用功能后，才需要以管理员权限启动PowerShell执行以下命令，把之后安装的发行版默认设为WSL2。


```{.powershell data-book-role="code"}
wsl --set-default-version 2
```

##### 安装发行版 {#src-0090-build-up-bioinfo-platform-177}

访问[Microsoft Store的Linux发行版页面](https://aka.ms/wslstore)，选择一个你中意的发行版即可，或者直接在应用商店搜索`Linux`，可以找到更多发行版；也可以按上一小节的方法，在命令行用`wsl --install -d 发行版名称`直接安装。


![Microsoft Store 中的 Linux 分发版的视图](../assets/02-computing-and-programming/010-store.png){#fig-02-computing-and-programming-010}


##### 创建账户和密码 {#src-0090-build-up-bioinfo-platform-183}

安装完成发行版后首次启动时会要求你创建用户名和密码。


![Windows 控制台中的 Ubuntu 解包](../assets/02-computing-and-programming/011-ubuntuinstall.png){#fig-02-computing-and-programming-011}


#### Windows Terminal {#src-0090-build-up-bioinfo-platform-189}

> Windows 终端可启用多个选项卡（在多个 Linux 命令行、Windows 命令提示符、PowerShell 和 Azure CLI 等之间快速切换）、创建键绑定（用于打开或关闭选项卡、复制粘贴等的快捷方式键）、使用搜索功能，以及使用自定义主题（配色方案、字体样式和大小、背景图像/模糊/透明度）。

在应用商店搜索`Windows Terminal`后安装即可。


![Windows Terminal：可在同一窗口管理 PowerShell、命令提示符与 WSL 等多种会话](../assets/02-computing-and-programming/012-ce36916b-bbee-4d15-8a3e-193a0e1ae26e.png){#fig-02-computing-and-programming-012}

### mac系统的基础配置 {#topic-02-macos-setup}

macOS 的基础配置比 Windows 简单得多，基本不太需要专门折腾。系统自带的 Terminal 已经可以完成绝大多数工作，习惯图形界面的读者可以安装 iTerm2 等第三方终端，获得分页、分屏和搜索等增强功能。由于原生兼容 Unix，Linux 下的很多命令和工具在 macOS 上可以直接使用；需要安装命令行软件时，建议先安装 Homebrew 包管理器，再通过 `brew install` 安装。macOS 的劣势主要在少数商业软件和与服务器架构的差异上（见上一节），但作为本地主机，它是开箱即用程度最高的选择之一。

## 连接远端服务器 {#sec-02-02}

打通本地与服务器之间的链路：连接、传输文件、执行命令，再用 VS Code 直接在远端目录里工作。如今的服务器几乎全部运行 Linux，常见的有 Ubuntu Server LTS、Debian，以及接替 CentOS 的 Rocky Linux 和 AlmaLinux。

### 使用ssh连接 {#src-0090-build-up-bioinfo-platform-197}

SSH命令是连接服务器很重要的工具。Linux和macOS都自带`ssh`命令；Windows长期以来不自带SSH命令，从Windows 10开始情况改善，较新的Windows 10和Windows 11已经预装OpenSSH客户端，在PowerShell中直接运行`ssh`就可以使用。OpenSSH服务器端则仍需要手动安装：在任务栏搜索框中输入“可选功能”，结果中会出现“添加可选功能”，点击即可进入。也可以通过“Windows设置→应用→可选功能”进入。


![Windows“管理可选功能”页面：已安装功能列表与“添加功能”入口](../assets/02-computing-and-programming/013-c575c9fa-1e74-4fc5-99e4-465792565047.png){#fig-02-computing-and-programming-013}

点击“添加功能”进入到添加功能的页面，选择需要的组件（例如“OpenSSH 服务器”；较早系统上未预装客户端时也可在此安装“OpenSSH 客户端”），点击“安装”按钮即可开始安装，不长的一段时间后就安装完毕了。

连接服务器的基本命令是 `ssh 用户名@服务器地址`，首次连接时系统会提示确认并保存主机指纹，之后输入密码即可登录。


假设服务器地址是 192.168.1.100，你的用户名是 meng，连接时输入：

```{.bash data-book-role="code"}
ssh meng@192.168.1.100
```

首次连接会提示确认主机指纹（fingerprint），输入 `yes` 回车后指纹会被保存，之后不会再询问。接着输入密码——屏幕上不显示任何字符是正常现象，输完直接回车。登录成功后，提示符会变成服务器上的样子，输入 `exit` 或按 `Ctrl+D` 即可退出返回本地。

每次都输密码既麻烦也不够安全，更推荐密钥登录。密钥成对存在：私钥留在本地，公钥放到服务器。用下面的命令生成一对密钥：

```{.bash data-book-role="code"}
ssh-keygen -t ed25519
```

一路回车即可，密钥会保存在 `~/.ssh/` 目录下：`id_ed25519` 是私钥，`id_ed25519.pub` 是公钥。生成时可以设置一个私钥口令（passphrase），多一层保护；留空则使用时不需要再输口令。然后把公钥传到服务器上：

```{.bash data-book-role="code"}
ssh-copy-id meng@192.168.1.100
```

这一次仍需要输入密码。之后再用 `ssh` 登录，服务器会用公钥验证你的身份，不再询问密码。要注意，私钥等于你在这台服务器上的钥匙，不要通过聊天工具或网盘发送，也不要提交进代码仓库。

如果经常连接多台服务器，可以为每台服务器起一个别名。编辑（没有就新建）本地家目录下的 `~/.ssh/config` 文件：

```{.text data-book-role="data" data-code-title="SSH 配置"}
Host lab
    HostName 192.168.1.100
    User meng
    Port 22
    IdentityFile ~/.ssh/id_ed25519

Host compute
    HostName 10.0.0.8
    User wangmeng
```

保存后，`ssh lab` 就等于 `ssh meng@192.168.1.100`，`scp`、`rsync` 和后面 VS Code 的远程连接也都能直接使用这些别名。服务器端口不是默认的 22 时，用 `Port` 指定；`IdentityFile` 在你有多对密钥时尤其有用。

### 文件的上传与下载 {#topic-02-file-transfer}

分析数据经常需要在本地与服务器之间往来：把原始数据传上去，把结果图表取回来。常用方式有两类：图形界面的 sftp 软件（如 FileZilla）适合零散文件的可视化拖拽；命令行的 `scp` 与 `rsync` 适合批量和脚本化传输，其中 `rsync` 还支持增量同步，是大目录反复备份的首选。

FileZilla 是常用的图形界面 sftp 软件，官网 filezilla-project.org 提供各平台安装包。安装后在顶部依次填写主机（`sftp://192.168.1.100`）、用户名、密码和端口 22，点击“快速连接”。左侧是本地文件树，右侧是服务器文件树，双击进入目录，把文件在两侧之间拖拽即完成上传和下载。它适合传输零散文件和查看目录结构；批量的、要写进脚本的传输，还是命令行更可靠。

`scp` 的用法和 `cp` 类似，远处的那一份用“用户名@服务器:路径”表示：

```{.bash data-book-role="code"}
scp reads.fastq.gz meng@192.168.1.100:~/project/data/
scp meng@192.168.1.100:~/project/results/volcano.pdf ./
scp -r result_dir meng@192.168.1.100:~/project/results/
```

第一行上传，第二行下载，第三行加 `-r` 递归传输整个目录。`rsync` 比 `scp` 更适合大目录和反复同步：它只传输有变化的部分，中断后重跑也不浪费。常用参数组合是 `-avP`：

```{.bash data-book-role="code"}
rsync -avP reads_dir/ meng@192.168.1.100:~/project/data/reads_dir/
```

`-a` 保留权限和时间戳并递归处理目录，`-v` 显示过程，`-P` 显示进度并支持断点续传。这里有个容易踩的坑：

::::: {.callout-warning .book-warning title="注意｜路径末尾的斜杠"}

`rsync` 中，`reads_dir` 表示“这个目录本身”，`reads_dir/` 表示“目录里的内容”。源路径多一个斜杠，目标下的层级就会差一层。传完之后最好 `ls` 检查一下目标目录的结构是否符合预期，再删本地或旧的一份。

:::::

### 基本的linux操作 {#src-0090-build-up-bioinfo-platform-13}

[]{#src-0090-build-up-bioinfo-platform-15}

登录服务器后，所有操作都在 Linux 命令行中完成。本节将围绕文件与文本的查找、查看、筛选和传递，介绍最常用的命令，以及路径、环境变量等基本概念。

先熟悉命令行的样子。一行命令通常由三部分组成：命令名、选项和参数。例如 `ls -l ~/data` 中，`ls` 是命令，`-l` 是选项（列出详细信息），`~/data` 是参数（要列的目录）。Linux 严格区分大小写，命令一律小写。

三个习惯能显著提高效率：按 `Tab` 键补全命令和路径，既快又不会拼错；按 `↑` 键翻出执行过的命令；`Ctrl+C` 中断当前正在运行的命令。用法记不清时，`man 命令名` 或 `命令 --help` 随时能查，例如 `man ls`。

#### 文件与目录 {#topic-02-linux-files}

| 命令 | 作用 | 常用形式 |
|:----- |:----- | ----- |
| pwd | 显示当前目录 | pwd |
| cd | 切换目录 | cd ~/data；cd .. 返回上级 |
| ls | 列出目录内容 | ls -l 长格式；ls -a 含隐藏文件；ls -lh 大小易读 |
| mkdir | 新建目录 | mkdir -p a/b/c 连建多级 |
| rmdir | 删除空目录 | rmdir a |
| cp | 复制 | cp file.txt backup/；cp -r dir1 dir2 复制目录 |
| mv | 移动或重命名 | mv old.txt new.txt |
| rm | 删除 | rm temp.txt；rm -r dir 删除目录 |
| chmod | 修改权限 | chmod 755 run.sh |

: 文件与目录的常用命令 {#tbl-02-environment-and-programming-03}

路径的写法先约定好：`/` 开头是绝对路径，从根目录算起；不以 `/` 开头是相对路径，从当前目录算起。`~` 代表家目录，`.` 是当前目录，`..` 是上一级。文件名里的空格和中文在命令行中容易出问题，生信分析的文件名建议只用英文字母、数字、下划线和点。

删除要格外小心：

::::: {.callout-warning .book-warning title="注意｜rm 没有回收站"}

命令行下的删除立即生效，没有回收站可以找回。`rm -r` 会连目录带内容一起删除，路径写错损失无法挽回。推荐两个习惯：删除前先用 `ls` 确认路径真实存在、指向预期的对象；拿不准时先用 `mv` 把待删内容移进一个 `trash/` 目录，确认无误后再统一清理。

:::::

权限方面，Linux 给每个文件定义三类人（属主、属组、其他人），各有读 `r`、写 `w`、执行 `x` 三种权限。`chmod 755 run.sh` 用三位数字分别设置三类人的权限：7 = 4+2+1，即读写执行；5 = 4+1，即读和执行。脚本想用 `./run.sh` 直接运行，就需要有执行权限；更省事的做法是统一用 `bash run.sh` 执行，完全不用关心权限位。

#### 查看文件内容 {#topic-02-linux-view}

| 命令 | 作用 | 常用形式 |
|:----- |:----- | ----- |
| cat | 一次性输出整个文件 | cat samples.tsv |
| less | 分页浏览大文件 | less run.log |
| head | 看文件开头 | head -n 20 counts.txt |
| tail | 看文件末尾 | tail -n 20 counts.txt |
| wc | 统计行数、词数、字节数 | wc -l counts.txt |
| diff | 比较两个文件的差异 | diff old.txt new.txt |

: 查看与统计文件的常用命令 {#tbl-02-environment-and-programming-04}

生信数据文件常常大到不能直接打开。`cat` 适合小文件；大文件用 `less` 分页查看：空格键翻页，`b` 往回翻，`/关键词` 搜索，`q` 退出。`head` 和 `tail` 是确认文件内容的捷径——拿到新文件，先 `head` 看格式对不对；下载完大文件，`tail` 看结尾是否完整。`wc -l` 数行数，是检查“文件里到底有多少条记录”的最快方法，后面章节会反复用到。

#### 文本的筛选与处理 {#topic-02-linux-text}

这一组命令把文本当作流来加工，是命令行真正的核心。

| 命令 | 作用 | 常用形式 |
|:----- |:----- | ----- |
| grep | 按模式筛选行 | grep SRR1 samples.tsv |
| cut | 按列截取字段 | cut -f 1,3 samples.tsv |
| sort | 排序 | sort -k2,2n counts.txt |
| uniq | 去除相邻的重复行 | sort names.txt \| uniq -c |
| paste | 按列拼接 | paste names.txt values.txt |
| sed | 流编辑 | sed 's/,/\t/g' data.csv |

: 筛选与处理文本的常用命令 {#tbl-02-environment-and-programming-05}

`grep` 负责找行：`grep control samples.tsv` 输出所有含 control 的行，`-v` 反选（排除匹配的行），`-i` 忽略大小写，`-n` 显示行号。`cut` 按列取字段，默认按制表符分隔（`-d` 可换分隔符），`-f 1,3` 取第 1、3 列。`sort` 默认按字典序，`-n` 按数值排，`-r` 逆序，`-k2,2n` 表示按第 2 列的数值排序。`uniq` 只合并相邻的重复行，所以总是跟在 `sort` 后面；`sort | uniq -c` 先排序再计数，是统计“每个值出现了多少次”的标准做法。`sed` 最常用的是替换：`sed 's/旧文本/新文本/g'`，结尾的 `g` 表示一行内全部替换。

举个例子。samples.tsv 是一个样本表：每行一个样本，制表符分隔，共三列——样本名、分组、测序文件。统计对照组（control）有多少个样本、把所有样本名列出来，分别只需一条命令链：

```{.bash data-book-role="code"}
grep control samples.tsv | wc -l
cut -f 1 samples.tsv | tail -n +2
```

第二条里 `tail -n +2` 表示从第 2 行输出到结尾，正好用来去掉表头。

#### 管道与重定向 {#topic-02-linux-pipe}

::::: {.callout-note .book-core title="核心知识｜管道：让每个程序只做一件事"}

上面的例子里，竖线 `|` 把一个命令的输出直接送给下一个命令当输入，这就是管道（pipe）。Unix 的设计哲学是让每个程序把一件事做好，再用管道把它们串起来，组合出复杂的处理流程。重定向则把输出存进文件：`>` 覆盖写入，`>>` 追加写入。

:::::

把前面的命令串起来，完成一个小任务——统计样本表里各组的样本数，并保存成文件：

```{.bash data-book-role="code"}
cut -f 2 samples.tsv | tail -n +2 | sort | uniq -c > group_count.txt
```

这条命令链逐段是：取出第 2 列（分组），去掉表头，排序，计数，最后写入 `group_count.txt`。读命令链就从左到右一段一段看——这也是全书阅读分析命令的基本方法。

#### 压缩、归档与查找 {#topic-02-linux-archive}

测序数据动辄几个 GB，传输和保存都离不开压缩。`tar` 把多个文件打成一个包，`gzip` 负责压缩，两者结合就是最常见的 `.tar.gz`：

```{.bash data-book-role="code"}
tar -czvf project.tar.gz project/
tar -xzvf project.tar.gz
gzip reads.fastq
gunzip reads.fastq.gz
```

`-c` 创建、`-x` 解开、`-z` 走 gzip、`-v` 显示过程、`-f` 指定文件名。测序数据更常见的 `.fastq.gz` 文件通常不必先解压，用 `zcat` 配合管道就能直接查看或送入下一步处理。

`find` 按条件递归查找文件：

```{.bash data-book-role="code"}
find . -name "*.fastq.gz" -type f
```

从当前目录起找出所有 `fastq.gz` 文件，常与管道配合，把找到的文件交给下一步处理。`ln -s` 创建软链接（符号链接），给文件或目录起一个稳定的别名：

```{.bash data-book-role="code"}
ln -s /data/project/reads ~/reads
```

数据换目录时只需要重建链接，脚本里的路径不用改。

#### 进程与会话 {#topic-02-linux-process}

跑在服务器上的任务需要看得见、管得住。

| 命令 | 作用 |
|:----- |:----- |
| ps aux | 查看所有进程 |
| top | 动态查看 CPU、内存占用 |
| w | 查看谁在登录、在做什么 |
| kill PID | 结束指定进程 |
| passwd | 修改自己的密码 |

: 进程与账户相关的常用命令 {#tbl-02-environment-and-programming-06}

`ps aux` 列出全部进程；`top` 实时刷新资源占用，按 `q` 退出。卡住的任务先用这两条找到进程号（PID），再 `kill` 结束它。`w` 看当前有哪些人登录，`last` 看历史登录记录，服务器行为异常时它们是第一手线索。

远程命令行还有个现实问题：本地断网或合上电脑，`ssh` 一断，正在跑的任务也跟着死掉。`tmux` 把会话保管在服务器上：

```{.bash data-book-role="code"}
tmux new -s mapping
tmux detach
tmux attach -t mapping
```

三条命令依次是：新建名为 mapping 的会话（脱离用 `Ctrl+B` 再按 `D`）、脱离会话、重新接回。脱离后任务继续在服务器上运行，下次登录 attach 回去就是原来的现场。跑比对、定量这类耗时任务前，先建 `tmux` 会话再启动，是服务器的标准工作习惯。

#### 环境变量 {#topic-02-linux-env}

环境变量是 shell 里带名字的全局值，习惯上全大写。最常用的一个叫 `PATH`：

```{.bash data-book-role="code"}
echo $PATH
```

`PATH` 是一串用冒号隔开的目录。你输入一个命令时，shell 就按顺序在这些目录里找同名程序——这就是为什么装好的软件有时会 `command not found`：它所在的目录不在 `PATH` 里。安装 Anaconda 时选择初始化（init），其实就是往 `~/.bashrc` 里写了一段把 conda 目录加入 `PATH` 的配置。

自己也可以设置环境变量：`export EDITOR=vim` 只在当前会话有效；要长期生效，就把这行写进 `~/.bashrc`，再 `source ~/.bashrc` 重新加载。`~/.bashrc` 是每次启动 shell 都会执行的配置文件，软件安装器都往里追加内容——环境出问题时先读它，多一分把握。

### Shell 脚本与批量处理 {#sec-02-03}

将单条命令组织为可检查的批处理。

分析中大量重复的操作，不该一条条手敲。把命令按顺序写进一个文件，交给 `bash` 执行，就是 Shell 脚本。它最大的价值不是省事，而是把分析过程变成可以检查、可以重跑、可以交给别人复核的文字记录。

::::: {.callout-note .book-core title="核心知识｜脚本是分析过程的可核查记录"}

命令行的历史留在终端里，脚本把每一步固化成文件。配合本章最后的版本管理，任何人——包括 AI agent 和几个月后的你——都能逐行检查分析做了什么、为什么这样做。这正是 AI 时代做分析需要的判断力基础。

:::::

新建 `run_fastqc.sh`，写入下面的内容：

```{.bash .numberLines data-book-role="code"}
#!/bin/bash
set -e
# 为 data 目录下的所有 fastq.gz 文件运行质控
for fq in data/*.fastq.gz; do
    echo "正在处理 $fq"
    fastqc "$fq" --outdir results/fastqc/
done
echo "全部完成"
```

逐行看：第 1 行 `#!/bin/bash` 声明用 `bash` 解释执行；`#` 开头的是注释，写清楚脚本做什么；`set -e` 让任何一条命令出错就立即停止，避免错误被后面的步骤掩盖；`for` 循环把 `data/` 下每个 `fastq.gz` 文件依次赋给变量 `fq`，`$fq` 取出变量的值，拼接后缀时推荐写成 `${fq}`，不会有歧义；`echo` 输出进度，让你随时知道脚本跑到哪一步。

执行脚本：

```{.bash data-book-role="code"}
bash run_fastqc.sh
```

也可以先 `chmod +x run_fastqc.sh` 加执行权限，再 `./run_fastqc.sh` 运行，效果相同。入门阶段统一用 `bash` 运行即可，少关心一件事。

脚本还可以接收参数：`$1`、`$2` 依次是执行时跟在脚本名后的第一、第二个参数。例如把单个文件的质控写成 `check_one.sh`：

```{.bash data-book-role="code"}
fastqc "$1" --outdir results/fastqc/
```

用 `bash check_one.sh data/S1.fastq.gz` 就能质控任意指定的文件。同一段处理逻辑要在不同数据上反复使用时，参数化比复制整个脚本再改名干净得多。

两个习惯值得从第一天养成：每个脚本开头写两三行注释，说明用途、输入和输出；先在小数据上跑通，确认无误再放大到全部样本。脚本是给别人看的，也是给几个月后的自己看的——AI agent 读它、改它，同样依赖这些注释和清晰的结构。

### 使用vscode连接 {#topic-02-vscode-remote}

VS Code 的 Remote-SSH 扩展可以把远端服务器变成本地开发环境：在本地编辑器中直接打开服务器上的目录，文件树、终端和代码补全都在本地呈现，修改实时同步到服务器。对习惯图形界面的读者，这是比纯命令行更友好的工作方式。

安装与连接的完整步骤如下。

1. 从官网 code.visualstudio.com 下载并安装 VS Code，安装选项保持默认。
2. 打开 VS Code，进入扩展面板（左侧栏四个方块图标，快捷键 Ctrl+Shift+X），搜索 Remote - SSH，点击 Install 安装。
3. 按 `F1`（或 `Ctrl+Shift+P`）打开命令面板，输入 Remote-SSH，选择 `Remote-SSH: Connect to Host` → `Add New SSH Host`，输入例如 `meng@192.168.1.100`。
4. 再次执行 `Remote-SSH: Connect to Host`，选择刚添加的主机，会新开一个窗口，按提示输入密码（配置过密钥登录则直接连上）。
5. 连接后选择 File → Open Folder，打开服务器上的项目目录（例如 `~/project`），左侧文件树显示的就是服务器上的文件。

连接成功后，窗口左下角会显示绿色的 SSH: 主机名。之后新建、编辑、保存文件都直接作用于服务器；按 ``Ctrl+` `` 打开的集成终端也是服务器上的 Shell，与 `ssh` 登录后的环境完全一致。编辑本地脚本再用 `scp` 传上去的往返流程，从此可以省去。

上面第 3 步添加的主机实际写入了 `~/.ssh/config` 文件；反过来，`config` 里已有的 `Host` 别名（例如上一节的 `lab`）会直接出现在 `Connect to Host` 的候选列表里。装好密钥登录再使用 Remote-SSH，体验最顺。

## 在服务器安装软件 {#sec-02-server-software}

[]{#src-0090-build-up-bioinfo-platform-209}

软件安装是配置服务器的主要工作。Linux 各发行版都自带包管理器：Ubuntu、Debian 一系用 `apt`，Red Hat 一系（Rocky Linux、AlmaLinux 等）用 `dnf`，命令名不同、用法相近，都是“刷新索引、搜索、安装”三板斧。本书的服务器以 Ubuntu 为例，其他发行版对照使用即可。

### 用 apt 安装软件 {#src-0090-build-up-bioinfo-platform-25}

apt（Advanced Packaging Tool）是Debian系Linux发行版的默认包管理工具，用于对包括系统本身在内的升级、安装等管理操作。


Ubuntu 的官方源中收录了不少常用生信软件，例如 `samtools`、`bwa`、`bedtools` 等，一条 `apt install` 命令即可完成安装，无需手动编译。不过官方源里的版本通常偏旧、更新较慢，而且需要管理员权限；遇到版本太旧或没有收录的软件，就轮到下一节的 conda 出场。

::::: {.callout-tip .book-example title="示例与练习｜用 apt 安装 R"}

以 R 语言为例，两条命令即可完成安装（需要管理员权限，命令前加 `sudo`）：

```{.bash data-book-role="code"}
sudo apt update
sudo apt install r-base
```

第一条刷新软件源索引——`apt` 的惯例是安装前先 `update`，让它知道各软件的最新版本；第二条安装 R 本体。装完确认版本：

```{.bash data-book-role="code"}
R --version
```

看到版本号输出，安装就完成了。Ubuntu 源里同样收录了 `r-bioc-*` 系列的 Bioconductor 包，但版本随发行版固定；需要新版 R 或最新的 R 包时，再考虑下一节的 conda。

:::::

#### apt和apt-get命令 {#topic-02-31}

`apt`是2014年正式发布的新的apt包管理工具的命令，相较于`apt-get`系列命令它更为简洁易用。

| apt 命令 | 取代的命令 | 命令的功能 |
|:----- |:----- | ----- |
| apt install | apt-get install | 安装软件包 |
| apt remove | apt-get remove | 移除软件包 |
| apt purge | apt-get purge | 移除软件包及配置文件 |
| apt update | apt-get update | 刷新存储库索引 |
| apt upgrade | apt-get upgrade | 升级所有可升级的软件包 |
| apt autoremove | apt-get autoremove | 自动删除不需要的包 |
| apt full-upgrade | apt-get dist-upgrade | 在升级软件包时自动处理依赖关系 |
| apt search | apt-cache search | 搜索应用程序 |
| apt show | apt-cache show | 显示包的详细信息 |

: apt 取代的 apt-get 系列命令 {#tbl-02-environment-and-programming-01}

| 新的apt命令 | 命令的功能 |
| ----- | ----- |
| apt list | 列出包含条件的包（已安装，可升级等） |
| apt edit-sources | 编辑源列表 |

: 新的 apt 命令 {#tbl-02-environment-and-programming-02}


#### apt镜像设置 {#topic-02-56}

apt默认的镜像在国内的访问速度是较慢的，所以设置一个国内的镜像是必要的。这里推荐北京外国语大学的开源软件站。其帮助信息完善，例如Ubuntu的[镜像设置帮助文档](https://mirrors.bfsu.edu.cn/help/ubuntu/)。

可以在文档中选择你具体使用的Ubuntu版本以获取对应的软件源地址。备份原先的软件源配置文件后即可更改配置文件。修改完成后执行`sudo apt update`命令刷新索引即可生效。


![北外镜像站的 Ubuntu 软件源帮助页面：选择系统版本后即可获得对应的 `sources.list` 配置](../assets/02-computing-and-programming/001-4bcc5c9c-49e7-465a-91f8-4e1ed8512e7c.png){#fig-02-computing-and-programming-001}

## conda 与 Bioconda {#sec-02-conda}

系统包管理器之外，生信分析还需要一个能装大量生信软件、能为不同项目隔离环境的工具，这就是 conda。

### conda 与 Bioconda {#topic-02-conda-bioconda}

::::: {.callout-note .book-core title="核心知识｜Anaconda、conda 与 Bioconda"}

Anaconda是Anaconda公司开发的一个Python发行版，集成的除了Python本体外，还包括大量科学计算的常用模块，以及Anaconda公司开发的Python模块和环境管理器conda。conda对环境和包管理的易用性要超过Python本地自带的功能，而且还可以管理非Python的模块（Perl、Java、R……）。对于生信分析人员，Bioconda这个conda源更是收入了大量生信分析软件，大大降低了生信软件的安装复杂度，一条命令即可，不需要手动编译和root权限。

:::::


在你已经添加了相应软件源的情况下，安装包只要用下面的命令即可(这里演示的是IPython的安装)。


```{.bash data-book-role="code"}
conda install ipython
```

conda默认会从Anaconda公司的官方服务器下载模块，而且默认只有官方defaults源一个。其他常用源像conda-forge和Bioconda也需要用户自己添加。另外，官方defaults源对较大规模机构（200人以上）的商业使用有授权限制，社区目前的普遍做法是优先使用完全开放的conda-forge源。这个时候手动添加常用源的国内镜像就十分有必要。


### Anaconda的安装 {#src-0090-build-up-bioinfo-platform-221}

这些镜像网站本身也会提供Anaconda的安装包。直接从镜像站下载安装包就免去官网下载可能的卡顿。需要特别提到的是，镜像站除了提供标准版的Anaconda安装包外还会提供Miniconda的安装包。这是一个精简的版本，体积相比标准版要小不少，只包括Python和conda管理器，包需要自行通过`conda`和`pip`安装。在一些磁盘有限的情况下可以选择Miniconda。此外还有社区维护的Miniforge发行版：默认使用conda-forge源，安装后开箱即用，近年来越来越多人直接以它作为安装入口。

Anaconda给Mac提供的是pkg和sh安装包，给Windows提供的是exe安装包，而给Linux只提供sh安装包。pkg和exe双击安装即可，而sh安装包需要通过命令行执行，即使通过图形界面启动sh安装包，很多设置也要在随之启动的终端下进行。

在这里也要特别提醒的是pkg和exe安装过程中会有一步让你设置是否要将Anaconda的路径加入到环境变量中，建议勾上（安装器默认不勾选，官方更推荐从开始菜单中的Anaconda专用终端启动，两种方式都可用）。而sh安装的最后一步也会询问是否进行初始化（init），要记得输入`yes`。这些选上之后，只要重启终端环境变量即可生效，就可以正常使用conda管理和相关的包。


### Anaconda镜像的设置 {#src-0090-build-up-bioinfo-platform-229}

目前国内最完善的公开Anaconda镜像就是清华大学的[TUNA镜像](https://mirrors.tuna.tsinghua.edu.cn/anaconda/)。不过国内部分地区访问清华大学镜像有时候不稳定，可以考虑使用北京外国语大学的镜像，其[帮助页面](https://mirrors.bfsu.edu.cn/help/anaconda/)内容由运行维护该站的清华大学TUNA协会同步维护，与清华源基本保持一致，但访问的稳定性很多时候更为优秀。帮助信息提到的存放`.condarc`配置文件的用户目录，在Linux下使用`cd ~`命令进入；在Windows下使用`cd $env:USERPROFILE`命令进入，或者在资源管理器地址栏输入`%USERPROFILE%`后回车进入。

我们依然推荐你通过上面的链接详细查阅他们的帮助信息，写入在`custom_channels`范围的镜像地址在使用时只有指定`-c`参数才会生效。例如如果按帮助页面的信息设置Anaconda配置文件，使用`conda install seqkit`命令会安装失败，需要使用`conda install -c bioconda seqkit`命令。


按北外镜像帮助页面的推荐，在家目录下创建或编辑 `.condarc` 文件，写入下面的内容：

```{.yaml data-book-role="data" data-code-title="~/.condarc"}
channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.bfsu.edu.cn/anaconda/pkgs/main
  - https://mirrors.bfsu.edu.cn/anaconda/pkgs/r
  - https://mirrors.bfsu.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.bfsu.edu.cn/anaconda/cloud
  pytorch: https://mirrors.bfsu.edu.cn/anaconda/cloud
```

`default_channels` 把 `defaults` 源的几个频道指到北外镜像，`custom_channels` 把 `conda-forge` 等频道指向镜像站的 `cloud` 目录。如果你只用 conda-forge，帮助页面还提供一个更精简的版本：`channels` 只留 `conda-forge` 并加一行 `nodefaults`，不再依赖 `defaults` 源。修改配置后执行一次 `conda clean -i` 清除缓存的源索引，新镜像即可生效。

Bioconda 频道不在上面这份配置的 `channels` 列表里——这正是前面 `-c bioconda` 的由来。想让 bioconda 成为默认频道，可以在 `channels` 里按 `conda-forge`、`bioconda`、`defaults` 的顺序逐行加入（conda 从上往下按优先级查找），也可以始终用 `-c` 显式指定，效果相同。

### Anaconda环境的管理 {#src-0090-build-up-bioinfo-platform-237}

::::: {.callout-note .book-core title="核心知识｜为不同项目隔离环境"}

为了防止不同的依赖之间相互冲突造成bug，除了最核心的常用组件，通常会为了每一类项目单独建立一个独立的环境。使得不同项目之间的模块可以版本不同。比如有时需要不同版本的Python或者R。

:::::


#### 创建环境 {#topic-02-329}

你可以指定环境的名称，后面再指定环境中要安装的一个或几个包及其版本，也可以只有名称没有其他参数。这时新建的环境里就不会预装任何包


```{.bash data-book-role="code"}
conda create -n py3 python=3.12
```

指定环境名称的创建方式会把环境相关文件放在Anaconda的安装目录下，但是有时候你需要将环境相关文件放在指定的路径。这个时候你就可以通过`-p`参数来指定conda环境的路径。比如下面就是一个指定环境目录为`/home/test_conda`并指定环境中的Python版本号为3.12的例子。


```{.bash data-book-role="code"}
conda create -p /home/test_conda python=3.12
```


环境建好后用 `conda activate py3` 进入——装包、跑程序都在这个环境里进行；`conda deactivate` 退出，`conda env list` 随时查看已建了哪些环境。进入环境后，提示符前会多出 `(py3)`，看到它就知道自己身在哪个环境。

#### 删除环境 {#topic-02-345}

我们同样可以通过参数来指定特定名称或路径的环境。


```{.bash data-book-role="code"}
conda remove -n py3 --all
conda remove -p /home/test_conda --all
```


### Micromamba {#src-0090-build-up-bioinfo-platform-264}

早期 conda 最大的痛点是经典求解器计算依赖和扫描各个源的速度都较慢，已安装的包较多时安装过程会明显变慢。Micromamba 用 C++ 重写了这一过程，再加上多线程并行，速度提升了一个数量级；conda 官方从 23.10 版起也把同源的 libmamba 作为默认求解器，所以现在直接使用 `conda` 通常已经够快。

Micromamba 的独特之处在于它是单个静态可执行文件：不依赖 Python、不依赖 conda，也不需要管理员权限。在服务器上没有装 Anaconda、或者没有 root 权限时，它是搭生信环境最省事的入口；容器和集群环境中也大量使用它。官方安装脚本一条命令即可完成（macOS 也可以 `brew install micromamba`）：

```{.bash data-book-role="code"}
"${SHELL}" <(curl -L micro.mamba.pm)
```

脚本会把可执行文件安装到 `~/.local/bin`（确认它在 `PATH` 中即可），并自动配置好 shell 集成；重新打开终端就能使用 `micromamba` 命令，环境默认存放在 `~/micromamba`。也可以从项目的 [releases 页面](https://github.com/mamba-org/micromamba-releases)直接下载单文件。

它的用法与 `conda` 几乎一致，把命令名换掉即可；软件源同样读取 `~/.condarc`，上一节的镜像配置直接生效。例如创建一个装有 fastqc 和 seqkit 的环境并进入：

```{.bash data-book-role="code"}
micromamba create -n bio -c conda-forge -c bioconda fastqc seqkit
micromamba activate bio
```

项目开源在 [GitHub](https://github.com/mamba-org/mamba)，完整文档见 [mamba.readthedocs.io](https://mamba.readthedocs.io/)。


## R 数据处理与绘图基础 {#sec-02-04}

具备阅读差异分析代码和处理结果表的能力。

### R and Rstudio {#src-0090-build-up-bioinfo-platform-300}

R语言也是生信分析中一个极为重要的编程语言。R语言官方的软件源CRAN中有着大量数据分析和生信领域的相关包。Bioconductor项目更是集中了大多数生信领域的R包。

#### R-base的安装和CRAN镜像设置 {#src-0090-build-up-bioinfo-platform-303}

R-base的安装包可以通过CRAN的镜像站点获得，推荐使用[北外的CRAN镜像](https://mirrors.bfsu.edu.cn/CRAN/)。Windows和macOS用户根据自己的操作系统点击对应链接，可以进入获取二进制安装包的页面。


![CRAN 的 R 下载页面：按操作系统选择安装入口](../assets/02-computing-and-programming/015-68cfe7a0-c604-448b-ba4e-b5d4d7662919.png){#fig-02-computing-and-programming-015}

![“R for Windows”页面：`base` 子目录提供 R 的基础安装包](../assets/02-computing-and-programming/016-5ec3d53f-9a6b-46f4-978c-25d005b35ea4.png){#fig-02-computing-and-programming-016}

![“R for macOS”页面：提供当前版本签名公证过的 .pkg 安装包](../assets/02-computing-and-programming/019-e67610e2-b16a-4c9d-ae9d-e8bbd0698714.png){#fig-02-computing-and-programming-019}


Linux用户如果有管理员权限，建议使用系统的包管理器安装。如果没有管理员权限也不要紧，使用Anaconda即可。使用`conda install -c conda-forge r-base`命令就可以完成R-base的安装。

而CRAN的镜像设置需要进入R的用户home目录，可以在R的交互模式下通过命令`path.expand("~")`获取。


![在 R 中用 `path.expand("~")` 获取用户主目录](../assets/02-computing-and-programming/018-9abb65cf-e93e-4722-a9f7-3c346e09c565.png){#fig-02-computing-and-programming-018}


获取R语言环境的home路径后，进入到该路径。查看路径下是否已经存在`.Rprofile`，如果没有则新建一个空白的即可。随后在`.Rprofile`文件末尾加入`options("repos" = c(CRAN="https://mirrors.bfsu.edu.cn/CRAN/"))`，保存后会在新启动的R环境中生效。

#### Rtools {#src-0090-build-up-bioinfo-platform-321}

Bioconductor和CRAN上提供的R包绝大部分都提供Windows平台下的二进制包，安装过程无需编译。但因为二进制包的更新一般晚于源码包的更新，且个别R包不提供二进制包，所以还是存在需要编译安装的情况。这个时候就需要R官方所提供的编译器集合Rtools。

访问[Rtools页面](https://cran.r-project.org/bin/windows/Rtools/)即可获得安装包。Rtools与R的版本配套更新，页面最上方始终提供当前R版本对应的安装包（写作本节时为Rtools45，配套R 4.5及更新版本），且只提供64位版本。如果你使用较老的R版本，可以访问[历史版本页面](https://cran.r-project.org/bin/windows/Rtools/history.html)下载对应的Rtools。


![Rtools 官方页面：最上方提供当前 R 版本对应的安装包](../assets/02-computing-and-programming/020-d3b3bee0-3edf-4c48-b876-19fce8883633.png){#fig-02-computing-and-programming-020}


从R 4.2起，Windows上的R会根据安装时写入的注册信息自动发现Rtools，安装后无需配置即可在需要时调用相关编译器。只有使用R 4.1及更早版本搭配Rtools40等旧版Rtools时，才需要按下述旧方法手工配置路径：参照上一节中的`path.expand("~")`获取R的用户home目录，然后在该目录下编辑`.Renviron`文件，添加下面的内容。


```{.text data-book-role="data"}
PATH="D:\Program Files\rtools40\usr\bin;${PATH}"
# 上面分号前的内容是旧版Rtools安装目录下编译器所在路径，
# 应根据实际安装目录进行修改。
# 分号后的内容表示之前已有的PATH环境变量内容，
# 以免覆盖原有环境变量内容。
```

配置完成后保存文件，然后重启R的交互环境。可以在交互环境中使用语句`Sys.which("make")`验证Rtools是否可用，如果成功则会出现Rtools目录下`make.exe`的路径（R 4.2及更新版本自动发现Rtools时，同样可以用这个语句验证）。以后在出现源码包版本高于二进制包版本，或R包无二进制包版本的情况，R就会提示你是否进行编译安装。你可以使用语句`install.packages("Rcpp", type = "source")`源码编译安装`Rcpp`包测试一下。


![在 R 中用 `Sys.which("make")` 验证 Rtools 已可用](../assets/02-computing-and-programming/017-6da0a303-f5d0-4cc3-96a4-3601c649742e.png){#fig-02-computing-and-programming-017}

#### RStudio {#topic-02-rstudio}

R 自带的交互界面只够验证安装，日常写代码推荐使用 RStudio——它是事实上的标准 R 开发环境，免费版对入门完全够用。桌面版从 [posit.co](https://posit.co/download/rstudio-desktop/) 下载安装。它与 R 的关系如同编辑器与解释器：RStudio 只是个外壳，背后调用的还是你装好的 R。

RStudio 界面分四块：左上是脚本编辑器，代码写成 `.R` 文件保存；左下是 R 控制台，单条命令在这里立即执行；右上显示环境与历史，能看到当前每个变量的值；右下是文件、绘图、帮助面板，画出的图就显示在这里。新手常分不清编辑器和控制台：推荐的工作方式是在编辑器里写代码，按 `Ctrl+Enter` 把当前行或选中部分送到控制台执行——代码始终留在文件里，而不是散落在会话历史中。

服务器上还有 RStudio Server：R 和 RStudio 都装在服务器上，浏览器打开就能用，本地零安装。数据量大时，它比“下载结果再本地画图”省事得多，不少课题组的服务器预装了它。

RStudio 的 Project 功能值得从第一天用起来：File → New Project 新建项目后，工作目录固定在项目文件夹，脚本、数据、图形都收在同一处。这与本章最后要讲的项目目录组织是同一件事——一个项目一个目录，从 R 这边先养成习惯。

## Python 与结构化配置的最低必要知识 {#sec-02-05}

能读懂基础脚本及后续 Snakemake 中的 Python 表达式。

### Python 基础速览 {#topic-02-python-basics}

本节提供 Python 的入门参考：变量、循环、函数与模块的最小知识集合，足以读懂后续章节的示例代码和 Snakemake 工作流中的 Python 表达式。

不需要专门安装：装好 Anaconda 后，终端输入 `python` 即进入交互环境，输入 `exit()` 退出。在交互环境里逐行试代码，是学语言最快的方式，下面所有例子都可以直接照抄运行。

#### 变量与数据类型 {#topic-02-python-vars}

Python 里用 = 给变量赋值，常见类型有整数、浮点数、字符串和布尔值：

```{.python data-book-role="code"}
n_samples = 6                # 整数
depth = 32.5                 # 浮点数
sample_name = "SRR1234567"   # 字符串
is_paired_end = True         # 布尔值
```

字符串用单引号或双引号都行。拼接字符串最方便的是 f-string：在引号前加 `f`，变量放进花括号：

```{.python data-book-role="code"}
report = f"样本 {sample_name} 共 {n_samples} 个，测序深度 {depth}X"
print(report)
```

处理文件名时常用的字符串方法：`sample_name.split("_")` 按下划线切成列表，`".".join(parts)` 用点连回字符串，`sample_name.replace("R1", "R2")` 替换子串，`sample_name.startswith("SRR")` 判断前缀。

#### 列表与字典 {#topic-02-python-containers}

列表（list）按顺序存一组值，用方括号，元素从 0 开始编号：

```{.python data-book-role="code"}
samples = ["S1", "S2", "S3"]
samples.append("S4")     # 末尾追加
print(samples[0])        # 第 1 个元素：S1
print(samples[-1])       # 最后 1 个元素：S4
print(len(samples))      # 元素个数：4
```

字典（dict）存“键→值”的对应关系，用花括号，生信配置里到处都是它：

```{.python data-book-role="code"}
groups = {"S1": "control", "S2": "treatment", "S3": "control"}
print(groups["S2"])          # treatment
groups["S4"] = "treatment"   # 新增一项
```

#### 循环与分支 {#topic-02-python-flow}

`for` 遍历列表或字典，`if` 按条件分支。注意 Python 靠缩进表示代码块，冒号后换行缩进四个空格：

```{.python .numberLines data-book-role="code"}
for sample in samples:
    if groups[sample] == "treatment":
        print(f"{sample} 是处理组")
    else:
        print(f"{sample} 是对照组")
```

配合 `range` 可以批量生成数字：`for i in range(1, 9)` 会依次取 1 到 8。

#### 函数 {#topic-02-python-functions}

函数把一段逻辑打包复用，`def` 定义，`return` 返回结果：

```{.python data-book-role="code"}
def get_sample_id(filename):
    """从文件名提取样本 ID，如 S1_L001_R1_001.fastq.gz → S1"""
    sample_id = filename.split("_")[0]
    return sample_id

print(get_sample_id("S1_L001_R1_001.fastq.gz"))
```

函数名后的三引号字符串是文档说明，写清输入输出，别人和 AI agent 都能读懂。这与前面 Shell 脚本一节的思路一致——语言不同，把过程写成可复用、可检查的文字相同。

#### 文件读写与模块 {#topic-02-python-files}

读文件用 `with open`，它保证文件用完自动关闭：

```{.python data-book-role="code"}
with open("samples.tsv") as f:
    header = f.readline().strip()
    for line in f:
        fields = line.strip().split("\t")
        print(fields[0], fields[1])
```

逐行读取，`strip()` 去掉行尾换行符，`split("\t")` 按制表符切列——这两步是处理表格文件的标准开场。写入文件加上模式参数：`with open("out.txt", "w") as f: f.write("...")`。

Python 的功能大量以模块形式提供，import 导入使用。`os.path` 处理路径、`csv` 读写表格、`subprocess` 在脚本里调用外部命令，后续章节会陆续见到。

本节不求覆盖 Python 全貌，目标是“读得懂”：看到一段脚本，能说出每个变量是什么、循环在遍历什么、结果写到哪里。写不出来的部分先照抄照跑，也可以让 AI agent 逐行解释——但读懂每一行的责任在你，这正是判断力的练习。

### Jupyter {#src-0090-build-up-bioinfo-platform-270}

Jupyter是一个非营利开源项目，2014年从IPython项目诞生。从诞生以来不断发展，基于网页支持跨几乎所有编程语言的交互式数据分析与科学计算。最早的项目是IPython Notebook，随着发展改名Jupyter Notebook。而现在Jupyter项目的核心是JupyterLab。如果你之前是Jupyter Notebook的用户，迁移到JupyterLab的学习成本很低。第一眼看上去最大的变化可能就是多标签和侧边栏。JupyterLab如今已经发展到4.X版本，经典的Jupyter Notebook仍在并行维护，扩展生态相当成熟。

#### 安装JupyterLab {#src-0090-build-up-bioinfo-platform-274}

安装JupyterLab非常简单，PyPI和Anaconda都有收录。这里再度建议大家使用前面小节介绍的独立包管理器micromamba进行安装


```{.bash data-book-role="code"}
pip install jupyterlab # pypi安装
conda install jupyterlab # anaconda安装
micromamba install jupyterlab # micromamba安装
```

#### 内核安装 {#src-0090-build-up-bioinfo-platform-284}

JupyterLab安装时只支持Python，如果需要支持其他语言，需要自己安装相应的内核。例如R语言需要安装R包`IRkernel`，然后在R交互模式中使用`IRkernel::installspec()`命令注册内核到JupyterLab。而Julia语言则需要安装Julia包`IJulia`，然后通过`build IJulia`命令来注册内核。

#### 本地和远程使用 {#src-0090-build-up-bioinfo-platform-288}

JupyterLab的本地启动十分简单，启动一个终端（Windows下可以选择PowerShell，或者通过Windows Terminal使用某个终端），切换到你需要进行分析的目录。Jupyter只可以读取启动时的目录及其子目录下的文件。当进入到需要的目录时，在终端中使用`jupyter lab`命令就可以启动JupyterLab。默认浏览器这时会自动启动，并打开JupyterLab的页面。

而远程使用服务器上的应用会复杂一些。需要先在本地的终端中使用`ssh`命令，把服务器上JupyterLab监听的端口映射到本地计算机。执行完下面的命令后，会登录远程服务器，再使用`jupyter lab`即可启动远程服务器上的JupyterLab。在本地浏览器中访问`127.0.0.1:1234`即可连接服务器的8888端口。（username是你在服务器上的用户名，serverip为服务器IP地址。1234为希望的本地端口，8888则为远程服务器的端口。）


```{.bash data-book-role="code"}
ssh username@serverip -L 127.0.0.1:1234:127.0.0.1:8888
```


::::: {.callout-warning .book-warning title="注意｜以实际启动端口为准"}

这里还需要提醒大家，有时候因为服务器上已经有其他用户，或者你之前启动了一个JupyterLab还未关闭，远程端口可能不会是8888。所以这里其实更推荐大家，先用ssh登录远程服务器（可以使用某些ssh软件比如MobaXterm，也可以用`ssh`命令）启动JupyterLab，通过启动时的提示信息查看端口号，由此更改上面映射命令中的远程服务器端口。

:::::

### 结构化配置：YAML 与 JSON {#topic-02-structured-config}

配置文件是分析流程的常见输入：样本表、软件参数、工作流规则经常以 YAML 或 JSON 等结构化格式描述。读懂它们，是修改他人流程、编写 Snakemake 规则的基础。

YAML 用“缩进 + 冒号”表达结构，可读性最好，是 Snakemake 等各类流程配置文件的主流格式。一个生信项目常见的 `samples.yaml` 长这样：

```{.yaml data-book-role="data" data-code-title="samples.yaml"}
project: rnaseq_demo
genome: hg38
threads: 8
samples:
  S1:
    condition: control
    fastq: data/S1.fastq.gz
  S2:
    condition: treatment
    fastq: data/S2.fastq.gz
```

顶层的 `project`、`genome`、`threads` 是键值对；`samples` 下面缩进一层，是嵌套的字典，每个样本又是一层。列表用短横线表示：

```{.yaml data-book-role="data" data-code-title="对比组合"}
comparisons:
  - treatment_vs_control
  - knockout_vs_wt
```

YAML 的规则极少：冒号后要有一个空格；层级关系完全靠缩进表达，同层元素必须对齐；字符串一般不需要引号。

::::: {.callout-warning .book-warning title="注意｜缩进用空格，不要用 Tab"}

YAML 只认空格缩进，编辑器插入 Tab 是配置报错的第一原因，报错信息里的 `found character that cannot start any token` 多半指它。让编辑器把 Tab 转为空格（VS Code 默认如此），这个坑就绕开了。

:::::

JSON 表达同样的结构，规则是：花括号表对象，方括号表数组，键加双引号，元素间逗号分隔。上面两份 YAML 合成一份 JSON 是：

```{.json data-book-role="data" data-code-title="config.json"}
{
  "project": "rnaseq_demo",
  "genome": "hg38",
  "threads": 8,
  "samples": {
    "S1": {"condition": "control", "fastq": "data/S1.fastq.gz"},
    "S2": {"condition": "treatment", "fastq": "data/S2.fastq.gz"}
  },
  "comparisons": ["treatment_vs_control", "knockout_vs_wt"]
}
```

JSON 没有 YAML 好读，但它是程序间交换数据的标准格式，网页、API 和各类软件的结果文件大量使用。生信实践中两者各就其位：人手写、人手改的配置用 YAML，程序输出和互相传递用 JSON。

读取它们都有现成工具：Python 中 `import json` 与 `import yaml`（后者随 Anaconda 提供）之后，`json.load(open("config.json"))` 一行就能把文件读成字典，之后按上一节字典的方式取值。改配置文件改的是参数值，不碰代码——这正是配置文件存在的意义。

## 本地AI agent的配置与安装 {#sec-02-ai-agents}

在本地装好 AI agent，让它们参与代码编写与排错。

Claude Code、Codex、ZCode 等命令行 AI agent 可以在终端里读写代码、执行命令、完成多步骤任务，是 AI 时代生信分析的重要本地工具。使用它们的前提是完成订阅（coding plan）与 API 设置，并清楚它们擅长什么、可能在什么地方出错——这与全书的判断力主题一致。

### coding plan 和 API 设置 {#topic-02-coding-plan}

AI coding agent 的使用方式有两类，先分清楚：

- coding plan（订阅计划）：按月或按年订阅，如 Anthropic 的 Claude Pro/Max、OpenAI 的 ChatGPT Plus/Pro、智谱的 GLM Coding Plan。订阅后客户端内直接使用，按对话量计限额，成本可控，适合日常高频使用。
- API key（按量付费）：在平台申请一串密钥，程序调用时验证身份，按实际用量计费。偶尔调用很便宜，跑大批量任务时要留心费用。

本书推荐入门读者从 coding plan 开始：费用固定，配置也最简单。各家 plan 支持的客户端不同——Claude Pro/Max 用于 Claude Code，ChatGPT Plus/Pro 用于 Codex，GLM Coding Plan 则可以同时驱动 Claude Code 和 ZCode（配置方法见下面两节）。

API key 本质是账户的钥匙，保管规则只有一条：绝不泄露。不要把 key 写进脚本或配置文件再提交到 Git，不要贴进聊天群或论坛。正规服务不会向你索取 key，凡是索要的，一律当作骗局。

::::: {.callout-warning .book-warning title="注意｜环境变量是存放密钥的正确位置"}

程序从环境变量读取密钥（如 `ANTHROPIC_API_KEY`）是通行做法：key 不出现在代码里，也就不会被提交进仓库。上一节环境变量的知识在这里直接用上。本地机器自用时，把 `export` 语句写进 `~/.bashrc`（或各家客户端自己的配置文件）即可。

:::::

### Claude Code {#topic-02-claude-code}

Claude Code 是 Anthropic 推出的命令行 AI agent，能在终端里读写代码、执行命令、跨文件完成多步修改，是生信分析中最常被提到的 coding agent 之一。

安装需要 Node.js 18 及以上版本（可用 `conda install -c conda-forge nodejs` 安装，或从官网下载），然后一条命令完成安装：

```{.bash data-book-role="code"}
npm install -g @anthropic-ai/claude-code
```

进入项目目录，输入 `claude` 即启动，首次按提示登录 Anthropic 账号（Claude Pro/Max 订阅即可使用）。

国内读者也可以用 GLM Coding Plan 驱动 Claude Code：订阅后在智谱开放平台获取 API key，编辑（没有则新建）`~/.claude/settings.json`，写入：

```{.json data-book-role="data" data-code-title="~/.claude/settings.json"}
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "你的智谱 API Key",
    "ANTHROPIC_BASE_URL": "https://open.bigmodel.cn/api/anthropic"
  }
}
```

保存后重新启动 `claude`，请求即走 GLM 通道。具体步骤以智谱官方文档为准：[在 Claude Code 中使用 GLM Coding Plan](https://docs.bigmodel.cn/cn/guide/develop/claude)。

### Codex {#topic-02-codex}

Codex CLI 是 OpenAI 的开源命令行 AI agent，定位与 Claude Code 相同。安装方式二选一：

```{.bash data-book-role="code"}
npm install -g @openai/codex
brew install codex
```

Codex 在 Git 仓库内工作效果最好：它能读提交历史、理解项目结构，改动前后可以用 `git diff` 清楚对照。所以在项目目录里 `git init` 之后再启动 `codex`，是推荐姿势。首次启动按提示登录 ChatGPT 账号（Plus/Pro 订阅），或配置 OpenAI API key。

### ZCode {#topic-02-zcode}

ZCode 是智谱推出的桌面版 AI coding 客户端，把 agent 对话、文件编辑和终端集成进图形界面，不习惯命令行的读者上手最容易。到官网 [zcode.z.ai](https://zcode.z.ai/) 下载 macOS 或 Windows 客户端安装，启动后用 GLM Coding Plan 或 API key 登录即可使用。安装说明见[官方文档](https://zcode.z.ai/cn/docs/install)，项目本身开源在 [GitHub](https://github.com/zai-org/ZCode)。

三款工具功能定位相近，选一到两款深入即可。真正重要的不是选哪个，而是后面各章反复强调的用法：让 agent 做事，同时检查它做的每一步——读它改的代码，看它跑的命令，验证它给的结果。

## AI时代的版本管理 {#sec-02-06}

形成可维护的工作习惯，遇到错误能够定位原因。

### 项目目录的组织 {#topic-02-project-structure}

生信项目最忌讳“文件摊一桌”。推荐从第一个项目起就固定目录骨架：

```{.text data-book-role="data" data-code-title="项目目录骨架"}
rnaseq_project/
├── data/
│   ├── raw/          # 原始测序数据，只读不动
│   └── clean/        # 过滤清洗后的数据
├── scripts/          # 分析脚本
├── results/          # 分析结果
│   ├── tables/
│   └── figures/
├── samples.tsv       # 样本表：项目的事实清单
└── README.md         # 项目说明
```

一条命令建好骨架：

```{.bash data-book-role="code"}
mkdir -p rnaseq_project/{data/{raw,clean},scripts,results/{tables,figures}}
```

几条原则。原始数据进 `raw/` 后不再修改，所有处理都产生新文件写到下游目录，出错时才能随时回到起点。样本表 `samples.tsv` 一行一个样本，记录样本名、分组、文件路径；脚本都从它读信息，而不是把样本名硬写进代码——加样本改表不改脚本。`README.md` 哪怕只写三行：项目做什么、数据从哪来、按什么顺序跑。数据、脚本、结果分开存放，“哪个文件能不能重新生成”一目了然：`results` 里的都能由 `scripts` 加 `data` 再生，丢了不心疼。

### 版本管理与 Git {#topic-02-git}

AI agent 会大量改你的代码，改坏了怎么办？答案是版本管理。Git 记录每次提交的完整快照，任何时候都能对照、回退，配合远程仓库还能异地备份。对“AI 改代码”的工作流，`git diff` 让每一次 AI 修改都清晰可见——这是人审查 AI 工作的基本工具，也是本节放在 AI agent 之后的原因。

最小工作流只需四条命令：

```{.bash data-book-role="code"}
git init
git add scripts/ samples.tsv
git commit -m "添加样本表与质控脚本"
git log --oneline
```

依次是：在项目目录初始化仓库，把文件纳入跟踪，提交一版快照并附说明，查看提交历史。日常循环就是 `add`、`commit`、`diff`：改一批，提交一次。commit message 是写给未来的自己和协作者（以及 AI）的，“update”“fix”这类消息等于没写。

生信仓库必须配一个 `.gitignore`，把大文件和生成物挡在仓库外：

```{.text data-book-role="data" data-code-title=".gitignore"}
data/
results/
*.fastq.gz
*.bam
```

测序数据动辄数 GB，放进 Git 仓库会让它膨胀到无法使用；`results` 能由脚本再生，也不必跟踪。Git 管代码、脚本和配置，数据另用 `rsync` 或网盘备份，两者不要混。

远程备份：在 GitHub（或单位 Git 服务）建一个私有仓库，按页面提示 `git remote add origin ...` 之后 `git push -u origin main`，以后每次提交随手 `push`。换了电脑或仓库丢失，整份 `clone` 回来——“代码永远有多份”是研究数据安全里成本最低的一条。

### 排错的基本思路 {#topic-02-troubleshooting}

分析出错是常态，排错能力比不出错更值得练。一套固定的动作能解决大部分问题。

第一，读报错。从输出里找 `error` 而不是 `warning`——`warning` 是提醒，`error` 才是失败原因。程序崩掉时，最后几行通常就是关键信息；找不到就把整段输出从头读，第一条 error 之后的内容往往是连锁反应，修好它，后面自然消失。把报错原文复制下来，不要凭印象转述。

第二，最小复现。整个流程报错，就把出错那一步单独拿出来，用最小的输入跑一遍：全部样本失败，先拿一个样本试；脚本失败，先把循环里那一条命令手动敲一遍。问题缩到最小，原因往往自己浮出来。

第三，查输入。很多“程序坏了”其实是数据不对：`head` 看文件开头格式，`wc -l` 数行数，和上一步的输出对一对。传输出错、表头变了、路径少了一层，都排在“软件有 bug”前面。

第四，问对问题。向同事或 AI agent 求助时带上三样东西：完整报错原文、你执行的命令、期望结果与实际结果。AI agent 很擅长解释报错、给出排查步骤，但它也会自信地猜——每一条建议都要自己验证过再往前走。

最后，把解决过程记下来，一行就够：“某报错，原因是 X，改法 Y”。同样的错第二次遇到时，你会感谢第一次的记录。
