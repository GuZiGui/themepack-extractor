# themepack-extractor
# Windows ThemePack Extractor

一个精简的 Python 脚本，用于提取 Windows `.themepack` 主题包中的高清壁纸。

##  功能特点
- 自动识别 `.themepack` (本质为 .cab 压缩包) 并解压
- 过滤并提取所有图片文件 (jpg, png, bmp, gif)
- 自动处理同名文件冲突，避免覆盖

##  使用方法
1. 确保已安装 Python 3 环境。
2. 在终端中运行以下命令：
   ```bash
   python extract_themepack.py "你的文件路径.themepack"
