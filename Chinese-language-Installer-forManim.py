import os
import sys
import platform
import subprocess
import requests
from pathlib import Path
import shutil

def get_system_font_dir():
    """获取系统字体目录"""
    system = platform.system()
    if system == "Windows":
        return "C:\\Windows\\Fonts"
    elif system == "Darwin":  # macOS
        return "/Library/Fonts"
    elif system == "Linux":
        # 对于Linux，我们使用用户字体目录而不是系统目录，避免权限问题
        return os.path.expanduser("~/.local/share/fonts")
    else:
        raise OSError(f"不支持的操作系统: {system}")

def install_font(font_url, font_name):
    """下载并安装字体"""
    font_dir = get_system_font_dir()
    
    # 创建字体目录（如果不存在）
    Path(font_dir).mkdir(parents=True, exist_ok=True)
    
    # 字体文件路径
    font_path = os.path.join(font_dir, font_name)
    
    # 检查字体是否已安装
    if os.path.exists(font_path):
        print(f"字体 {font_name} 已安装，跳过...")
        return True
    
    try:
        # 下载字体
        print(f"正在下载 {font_name}...")
        response = requests.get(font_url, stream=True)
        response.raise_for_status()
        
        # 保存字体文件
        with open(font_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"字体 {font_name} 安装成功！")
        
        # Linux系统需要更新字体缓存
        if platform.system() == "Linux":
            subprocess.run(["fc-cache", "-f", "-v"], check=True)
            print("字体缓存已更新")
            
        return True
        
    except Exception as e:
        print(f"安装 {font_name} 失败: {str(e)}")
        # 清理可能不完整的文件
        if os.path.exists(font_path):
            os.remove(font_path)
        return False

def install_matplotlib_font_config():
    """配置Matplotlib使用中文字体"""
    try:
        import matplotlib
        import matplotlib.pyplot as plt
        
        # 配置matplotlibrc文件
        matplotlib.rcParams["font.family"] = ["SimHei", "WenQuanYi Micro Hei", "Heiti TC", "Arial Unicode MS"]
        matplotlib.rcParams["axes.unicode_minus"] = False  # 解决负号显示问题
        
        # 保存配置
        plt.rcParams.update(matplotlib.rcParams)
        
        print("Matplotlib 字体配置已更新")
        return True
    except ImportError:
        print("未安装Matplotlib，跳过Matplotlib字体配置")
        return False
    except Exception as e:
        print(f"配置Matplotlib字体失败: {str(e)}")
        return False

def main():
    print(f"检测到操作系统: {platform.system()}")
    print(f"系统字体目录: {get_system_font_dir()}")
    
    # 中文字体列表 (名称, 下载链接)
    chinese_fonts = [
        ("SimHei.ttf", "https://github.com/StellarCN/scp_zh/raw/master/fonts/SimHei.ttf"),
        ("WenQuanYi Micro Hei.ttc", "https://github.com/StellarCN/scp_zh/raw/master/fonts/WenQuanYi%20Micro%20Hei.ttc"),
        ("NotoSansCJK-Regular.ttc", "https://github.com/googlefonts/noto-cjk/raw/main/Sans/OTC/NotoSansCJK-Regular.ttc")
    ]
    
    # 安装字体
    print("\n开始安装中文字体...")
    for font_name, font_url in chinese_fonts:
        install_font(font_url, font_name)
    
    # 配置Matplotlib
    print("\n配置Matplotlib字体...")
    install_matplotlib_font_config()
    
    print("\n字体安装完成！请重启Jupyter Notebook以使字体生效。")
    print("如果仍然有中文显示问题，可以尝试清除浏览器缓存或重新启动计算机。")

if __name__ == "__main__":
    main()