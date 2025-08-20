#!/usr/bin/env python3
"""
版本号更新脚本

用法:
    python scripts/update_version.py 0.1.4
    python scripts/update_version.py --current  # 显示当前版本
"""

import sys
import re
from pathlib import Path


def get_current_version():
    """获取当前版本号"""
    init_file = Path("src/work_tool_mcp/__init__.py")
    if not init_file.exists():
        raise FileNotFoundError(f"找不到文件: {init_file}")
    
    content = init_file.read_text(encoding="utf-8")
    match = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', content)
    if not match:
        raise ValueError("在 __init__.py 中找不到版本号")
    
    return match.group(1)


def update_version(new_version):
    """更新版本号"""
    # 验证版本号格式
    if not re.match(r'^\d+\.\d+\.\d+$', new_version):
        raise ValueError(f"版本号格式无效: {new_version}，应该是 x.y.z 格式")
    
    init_file = Path("src/work_tool_mcp/__init__.py")
    if not init_file.exists():
        raise FileNotFoundError(f"找不到文件: {init_file}")
    
    # 读取文件内容
    content = init_file.read_text(encoding="utf-8")
    
    # 替换版本号
    new_content = re.sub(
        r'(__version__\s*=\s*["\'])([^"\']+)(["\'])',
        f'\\g<1>{new_version}\\g<3>',
        content
    )
    
    if new_content == content:
        raise ValueError("未找到版本号行进行更新")
    
    # 写回文件
    init_file.write_text(new_content, encoding="utf-8")
    print(f"✅ 版本号已更新为: {new_version}")
    print(f"📝 文件已更新: {init_file}")
    

def main():
    if len(sys.argv) == 1:
        print("用法:")
        print("  python scripts/update_version.py 0.1.4")
        print("  python scripts/update_version.py --current")
        sys.exit(1)
    
    if sys.argv[1] == "--current":
        try:
            current = get_current_version()
            print(f"当前版本: {current}")
        except Exception as e:
            print(f"❌ 错误: {e}")
            sys.exit(1)
    else:
        new_version = sys.argv[1]
        try:
            current = get_current_version()
            print(f"当前版本: {current}")
            update_version(new_version)
            print("\n📦 建议执行以下命令重新构建:")
            print("  uv build")
        except Exception as e:
            print(f"❌ 错误: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
