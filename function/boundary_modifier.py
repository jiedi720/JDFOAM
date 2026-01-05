"""边界类型修改模块"""


def generate_boundary_sed_commands(boundary_names):
    """
    根据边界名称生成 sed 命令，用于修改边界类型
    
    Args:
        boundary_names: 边界名称列表
        
    Returns:
        list: sed 命令列表
    """
    sed_commands = []
    for name in boundary_names:
        # 根据名称决定 type。如果名字含 'wall'，则 type 改为 wall，否则保持 patch
        target_type = "wall" if "wall" in name.lower() else "patch"
        
        # 精准匹配：只替换该边界名对应花括号区块内的 type
        sed_cmd = f"sed -i '/{name}/,/}}/ s/type[[:space:]]\\+patch;/type            {target_type};/' constant/polyMesh/boundary"
        sed_commands.append(sed_cmd)
    
    # 兜底处理 defaultFaces
    sed_commands.append("sed -i '/defaultFaces/,/}/ s/type[[:space:]]\\+patch;/type            wall;/' constant/polyMesh/boundary")
    
    return sed_commands