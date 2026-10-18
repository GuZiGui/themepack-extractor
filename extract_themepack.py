import os
import shutil
import subprocess
import sys
import tempfile

def extract_wallpapers(themepack_path, output_dir=None):
    if not os.path.exists(themepack_path):
        print(f"❌ 找不到文件：{themepack_path}")
        return
    
    # 自动生成输出目录
    base_name = os.path.splitext(os.path.basename(themepack_path))[0]
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(themepack_path)), f"{base_name}_提取结果")
    
    wallpaper_dir = os.path.join(output_dir, "Wallpapers")
    os.makedirs(wallpaper_dir, exist_ok=True)
    print(f"📂 输出目录：{output_dir}")

    # 创建临时工作目录修改后缀
    with tempfile.TemporaryDirectory() as temp_dir:
        cab_file = os.path.join(temp_dir, "theme.cab")
        shutil.copy2(themepack_path, cab_file)

        # 使用系统自带的 expand.exe 解压
        temp_extract_dir = os.path.join(temp_dir, "extracted")
        os.makedirs(temp_extract_dir, exist_ok=True)
        
        print("⏳ 正在解析主题包...")
        cmd = f'expand "{cab_file}" -F:* "{temp_extract_dir}"'
        try:
            # 运行 expand 命令
            subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError:
            # 如果系统 expand 失败，尝试使用 7-Zip 或 tar 作为备选
            print("⚠️ 系统自带解压工具失败，尝试使用 7-Zip 或 tar...")
            if shutil.which("7z"):
                subprocess.run(f'7z x "{cab_file}" -o"{temp_extract_dir}" -y', shell=True, check=True)
            elif shutil.which("tar"):
                subprocess.run(f'tar -xf "{cab_file}" -C "{temp_extract_dir}"', shell=True, check=True)
            else:
                print("❌ 未找到可用的解压命令（expand/7z/tar）。")
                return

        # 遍历提取的文件并筛选壁纸
        supported_exts = (".jpg", ".jpeg", ".png", ".bmp", ".gif")
        count = 0
        for root, _, files in os.walk(temp_extract_dir):
            for file in files:
                if file.lower().endswith(supported_exts):
                    src_path = os.path.join(root, file)
                    dest_path = os.path.join(wallpaper_dir, file)
                    
                    # 重名文件自动加后缀
                    base, ext = os.path.splitext(dest_path)
                    counter = 1
                    while os.path.exists(dest_path):
                        dest_path = f"{base}_{counter}{ext}"
                        counter += 1
                        
                    shutil.copy2(src_path, dest_path)
                    count += 1

        print(f"✅ 提取完成！共成功提取 {count} 张壁纸到：{wallpaper_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：python extract_themepack.py <你的文件.themepack>")
        sys.exit(1)
    extract_wallpapers(sys.argv[1])