"""源码扫描与合并模块"""
import os


# 支持的文件扩展名白名单
ALLOWED_EXTENSIONS = {
    '.py', '.js', '.ts', '.jsx', '.tsx', '.vue', '.html', '.htm', '.css', '.scss', '.less',
    '.c', '.cpp', '.h', '.hpp', '.cc', '.cxx', '.java', '.go', '.rs', '.swift', '.kt',
    '.sql', '.sh', '.bash', '.zsh', '.ps1', '.bat', '.cmd', '.json', '.xml', '.yaml', '.yml',
    '.toml', '.ini', '.cfg', '.conf', '.md', '.txt', '.rst', '.tex', '.lua', '.rb', '.php',
    '.pl', '.pm', '.t', '.r', '.m', '.mm', '.cs', '.fs', '.fsx', '.vb', '.dart', '.scala'
}

# 默认排除的目录
EXCLUDE_DIRS = {
    '.git', '.idea', '.vscode', 'node_modules', 'venv', 'env', '__pycache__',
    'dist', 'build', '.pytest_cache', '.mypy_cache', 'htmlcov', '.tox',
    'site-packages', 'egg-info', '.eggs', 'bin', 'include', 'lib'
}


def is_binary_file(file_path):
    """检查文件是否为二进制文件"""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:
                return True
            chunk.decode('utf-8')
    except (UnicodeDecodeError, IOError):
        return True
    return False


def scan_directory(root_dir, exclude_dirs=None, progress_callback=None):
    """
    扫描目录，收集所有符合条件的源代码文件
    
    Args:
        root_dir: 根目录路径
        exclude_dirs: 要排除的目录集合
        progress_callback: 进度回调函数
        
    Returns:
        list: 文件路径列表
    """
    if exclude_dirs is None:
        exclude_dirs = EXCLUDE_DIRS
    
    files = []
    total_files = 0
    
    # 先统计总文件数
    for root, dirs, filenames in os.walk(root_dir):
        # 移除排除的目录
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                total_files += 1
    
    processed = 0
    
    for root, dirs, filenames in os.walk(root_dir):
        # 移除排除的目录
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in ALLOWED_EXTENSIONS:
                file_path = os.path.join(root, filename)
                
                # 检查是否为二进制文件
                if not is_binary_file(file_path):
                    files.append(file_path)
                
                processed += 1
                if progress_callback:
                    progress = int((processed / total_files) * 100) if total_files > 0 else 100
                    progress_callback(progress)
    
    return files


def combine_files_to_markdown(files, output_path, root_dir, progress_callback=None):
    """
    将多个文件合并为一个 Markdown 文档
    
    Args:
        files: 文件路径列表
        output_path: 输出文件路径
        root_dir: 项目根目录
        progress_callback: 进度回调函数
        
    Returns:
        bool: 是否成功
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as md_file:
            # 写入标题
            md_file.write("# 项目源码整合文档\n\n")
            md_file.write(f"**生成时间**: {os.path.getctime(output_path)}\n\n")
            md_file.write("---\n\n")
            
            # 写入目录
            md_file.write("## 目录\n\n")
            for i, file_path in enumerate(files, 1):
                rel_path = os.path.relpath(file_path, root_dir)
                md_file.write(f"{i}. [{rel_path}](#file-{i})\n")
            md_file.write("\n---\n\n")
            
            # 写入每个文件的内容
            total_files = len(files)
            for i, file_path in enumerate(files, 1):
                rel_path = os.path.relpath(file_path, root_dir)
                
                md_file.write(f'<a name="file-{i}"></a>\n\n')
                md_file.write(f"## {i}. {rel_path}\n\n")
                md_file.write(f"**完整路径**: `{file_path}`\n\n")
                md_file.write("```{language}\n".format(language=get_language_from_ext(file_path)))
                
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    md_file.write(content)
                
                md_file.write("\n```\n\n")
                md_file.write("---\n\n")
                
                if progress_callback:
                    progress = int((i / total_files) * 100) if total_files > 0 else 100
                    progress_callback(progress)
        
        return True
    except Exception as e:
        print(f"合并文件失败: {e}")
        return False


def get_language_from_ext(file_path):
    """根据文件扩展名获取代码语言标识"""
    ext = os.path.splitext(file_path)[1].lower()
    
    lang_map = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.jsx': 'jsx',
        '.tsx': 'tsx',
        '.vue': 'vue',
        '.html': 'html',
        '.htm': 'html',
        '.css': 'css',
        '.scss': 'scss',
        '.less': 'less',
        '.c': 'c',
        '.cpp': 'cpp',
        '.h': 'c',
        '.hpp': 'cpp',
        '.cc': 'cpp',
        '.cxx': 'cpp',
        '.java': 'java',
        '.go': 'go',
        '.rs': 'rust',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.sql': 'sql',
        '.sh': 'bash',
        '.bash': 'bash',
        '.zsh': 'bash',
        '.ps1': 'powershell',
        '.bat': 'batch',
        '.cmd': 'batch',
        '.json': 'json',
        '.xml': 'xml',
        '.yaml': 'yaml',
        '.yml': 'yaml',
        '.toml': 'toml',
        '.ini': 'ini',
        '.cfg': 'ini',
        '.conf': 'ini',
        '.md': 'markdown',
        '.txt': 'text',
        '.rst': 'rst',
        '.tex': 'tex',
        '.lua': 'lua',
        '.rb': 'ruby',
        '.php': 'php',
        '.pl': 'perl',
        '.pm': 'perl',
        '.t': 'perl',
        '.r': 'r',
        '.m': 'matlab',
        '.mm': 'objectivec',
        '.cs': 'csharp',
        '.fs': 'fsharp',
        '.fsx': 'fsharp',
        '.vb': 'vbnet',
        '.dart': 'dart',
        '.scala': 'scala'
    }
    
    return lang_map.get(ext, 'text')