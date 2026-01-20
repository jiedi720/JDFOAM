"""源码扫描与合并模块

该模块提供完整的源代码文件扫描和合并功能，支持多种编程语言，
将项目中的所有源代码文件整合为一个 Markdown 文档，便于阅读和分享。
功能包括：
- 智能识别多种编程语言
- 过滤二进制文件和非文本文件
- 生成带目录的 Markdown 文档
- 支持进度回调和日志输出
"""

import os


# --- 配置部分 ---
# 排除不需要扫描的目录
exclude_dirs = {'.git', 'node_modules', '__pycache__', '.venv', 'dist', '.vscode', '.idea', 'venv', 'env', 'build'}
# 定义支持的后缀及其对应的 Markdown 代码块语言标识
include_extensions = {
    '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
    '.c': 'c', '.cpp': 'cpp', '.h': 'c', '.hpp': 'cpp', '.cc': 'cpp', '.cxx': 'cpp',
    '.java': 'java', '.go': 'go', '.rs': 'rust', '.swift': 'swift', '.kt': 'kotlin',
    '.html': 'html', '.htm': 'html', '.css': 'css', '.scss': 'scss', '.less': 'less',
    '.sh': 'bash', '.bash': 'bash', '.zsh': 'bash', '.ps1': 'powershell', '.bat': 'batch', '.cmd': 'batch',
    '.md': 'markdown', '.json': 'json', '.sql': 'sql',
    '.xml': 'xml', '.yaml': 'yaml', '.yml': 'yaml', '.toml': 'toml', '.ini': 'ini', '.cfg': 'ini', '.conf': 'ini',
    '.lua': 'lua', '.rb': 'ruby', '.php': 'php', '.pl': 'perl', '.pm': 'perl', '.t': 'perl',
    '.r': 'r', '.m': 'matlab', '.mm': 'objectivec', '.cs': 'csharp', '.fs': 'fsharp', '.fsx': 'fsharp',
    '.vb': 'vbnet', '.dart': 'dart', '.scala': 'scala', '.vue': 'vue', '.jsx': 'jsx', '.tsx': 'tsx',
    '.txt': 'text', '.rst': 'rst', '.tex': 'tex'
}


def detect_language(file_path, ext):
    """
    智能检测代码块语言标签

    根据文件扩展名和文件内容智能识别编程语言，用于 Markdown 代码块的语法高亮

    Args:
        file_path (str): 文件路径
        ext (str): 文件扩展名

    Returns:
        str: 对应的 Markdown 代码块语言标识
    """
    if ext in include_extensions:
        return include_extensions[ext]
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            head = f.read(1000).lower()
            if "foamfile" in head or "c++" in head: return "cpp"
            if head.startswith("#!"):
                if "python" in head: return "python"
                if "sh" in head: return "bash"
    except: pass
    return "text"


def is_text_file(file_path):
    """
    强化版文本检测（过滤乱码/二进制文件）

    通过多种方法检测文件是否为文本文件，避免将二进制文件误识别为文本文件
    1. 检查前 1024 字节是否包含空字符 \0 (二进制文件的典型特征)
    2. 尝试进行 utf-8 解码验证

    Args:
        file_path (str): 文件路径

    Returns:
        bool: 是否为文本文件
    """
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if not chunk:
                return True  # 空文件视为文本
            # 二进制文件（如 exe, pyc, jpg）通常包含 \0
            if b'\0' in chunk:
                return False
            # 尝试解码确认是否为文本
            chunk.decode('utf-8')
            return True
    except (UnicodeDecodeError, PermissionError, OSError):
        return False


def scan_directory(root_dir, exclude_dirs_param=None, progress_callback=None, log_callback=None):
    """
    扫描目录，收集所有符合条件的源代码文件

    递归扫描指定目录下的所有文件，过滤出符合条件的源代码文件

    Args:
        root_dir (str): 根目录路径
        exclude_dirs_param (set): 要排除的目录集合（可选）
        progress_callback (callable): 进度回调函数
        log_callback (callable): 日志回调函数

    Returns:
        list: 文件路径列表，格式为 [(full_path, rel_path, ext), ...]
    """
    if exclude_dirs_param is None:
        exclude_dirs_param = exclude_dirs

    # 检查目录是否存在
    if not os.path.exists(root_dir):
        msg = f"错误: 目录不存在: {root_dir}"
        if log_callback:
            log_callback(msg)
        return []

    if not os.path.isdir(root_dir):
        msg = f"错误: 路径不是目录: {root_dir}"
        if log_callback:
            log_callback(msg)
        return []

    folder_name = os.path.basename(os.path.normpath(root_dir))
    output_filename = f"{folder_name}_source_code.md"
    output_path = os.path.join(root_dir, output_filename)

    valid_files = []
    msg = f"🔍 正在扫描并过滤乱码: {folder_name}"
    if log_callback:
        log_callback(msg)

    # 预扫描，计算需要处理的文件总数
    all_potential_files = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if d not in exclude_dirs_param]
        for file in files:
            if file == output_filename: continue  # 不扫描自己
            full_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()

            # 排除主目录下的 .txt 文件
            if ext == '.txt' and os.path.normpath(root) == os.path.normpath(root_dir):
                continue

            # 排除所有 .bat 文件
            if ext == '.bat':
                continue

            # 后缀匹配且通过文本特征检测
            if ext in include_extensions or (ext == ''):
                if is_text_file(full_path):
                    all_potential_files.append((full_path, os.path.relpath(full_path, root_dir), ext))

    total_files = len(all_potential_files)
    if total_files == 0:
        msg = "❌ 错误：未发现有效文本文件。"
        if log_callback:
            log_callback(msg)
        if progress_callback:
            progress_callback(100)
        return []

    msg = f"✅ 找到 {total_files} 个有效文件"
    if log_callback:
        log_callback(msg)

    # 返回文件列表（格式：[(full_path, rel_path, ext), ...]）
    return all_potential_files


def combine_files_to_markdown(files, output_path, root_dir, progress_callback=None):
    """
    将多个文件合并为一个 Markdown 文档

    将扫描到的源代码文件合并为一个带目录的 Markdown 文档，便于阅读和分享

    Args:
        files (list): 文件路径列表，格式为 [(full_path, rel_path, ext), ...]
        output_path (str): 输出文件路径
        root_dir (str): 项目根目录
        progress_callback (callable): 进度回调函数

    Returns:
        bool: 是否成功
    """
    try:
        total_files = len(files)
        if total_files == 0:
            return False

        with open(output_path, 'w', encoding='utf-8') as md_file:
            # 写入标题和目录
            folder_name = os.path.basename(os.path.normpath(root_dir))
            md_file.write(f"# {folder_name} 源代码整合文档\n\n")
            # 使用 time 模块获取更准确的时间
            import time
            md_file.write(f"**生成时间**: {time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}\n\n")
            md_file.write("## 目录\n\n")

            for _, rel_path, _ in files:
                anchor = rel_path.replace(' ', '-').replace('.', '').replace('/', '').replace('\\', '').lower()
                md_file.write(f"- [{rel_path}](#file-{anchor})\n")
            md_file.write("\n---\n\n")

            # 遍历写入文件内容
            for i, (full_path, rel_path, ext) in enumerate(files):
                # 更新进度条
                if progress_callback:
                    progress = int(((i + 1) / total_files) * 100)
                    progress_callback(progress)
                    # 处理事件循环，让UI有机会更新
                    try:
                        from PySide6.QtWidgets import QApplication
                        QApplication.processEvents()
                    except:
                        pass

                lang_tag = detect_language(full_path, ext)
                anchor_id = rel_path.replace(' ', '-').replace('.', '').replace('/', '').replace('\\', '').lower()

                md_file.write(f'<a name="file-{anchor_id}"></a>\n## {i + 1}. {rel_path}\n\n')
                md_file.write(f"**完整路径**: `{full_path}`\n\n")
                md_file.write(f"```{lang_tag}\n")

                # 读取时使用 errors='ignore' 兜底，防止极个别特殊字符导致崩溃
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as infile:
                    content = infile.read()
                    md_file.write(content)

                md_file.write("\n```\n\n[回到目录](#目录)\n\n---\n\n")

        return True
    except Exception as e:
        print(f"合并文件失败: {e}")
        return False