"""MSH 文件解析模块"""
import os
import re


def get_boundary_names_from_msh(msh_file):
    """
    解析 .msh 文件以提取 PhysicalNames。
    返回边界名称列表，如 ['walls', 'inlet', 'outlet', 'atmosphere']。
    
    Args:
        msh_file: MSH 文件路径
        
    Returns:
        list: 边界名称列表
    """
    names = []
    if not os.path.exists(msh_file):
        print(f"错误: MSH 文件不存在 - {msh_file}")
        return names
    
    try:
        with open(msh_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            # 匹配 $PhysicalNames ... $EndPhysicalNames 之间的块
            block = re.search(r'\$PhysicalNames(.*?)\$EndPhysicalNames', content, re.DOTALL)
            if block:
                # 在块中查找双引号内的所有边界名称
                names = re.findall(r'"([^"]+)"', block.group(1))
            else:
                print(f"警告: 未在 {msh_file} 中找到 $PhysicalNames 块")
    except Exception as e:
        print(f"解析 MSH 失败: {e}")
    return names