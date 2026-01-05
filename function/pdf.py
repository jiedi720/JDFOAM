"""PDF 转换模块"""
import os
import pdfkit


# wkhtmltopdf 默认路径配置
WKHTMLTOPDF_PATHS = [
    r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe",
    r"C:\Program Files (x86)\wkhtmltopdf\bin\wkhtmltopdf.exe",
    r"C:\wkhtmltopdf\bin\wkhtmltopdf.exe",
]


# GitHub 风格的 CSS 样式
GITHUB_CSS = """
<style>
    body {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
        font-size: 14px;
        line-height: 1.6;
        color: #24292e;
        background-color: #ffffff;
        margin: 0;
        padding: 20px;
    }
    
    h1, h2, h3, h4, h5, h6 {
        margin-top: 24px;
        margin-bottom: 16px;
        font-weight: 600;
        line-height: 1.25;
    }
    
    h1 {
        font-size: 2em;
        padding-bottom: 0.3em;
        border-bottom: 1px solid #eaecef;
    }
    
    h2 {
        font-size: 1.5em;
        padding-bottom: 0.3em;
        border-bottom: 1px solid #eaecef;
    }
    
    code {
        padding: 0.2em 0.4em;
        margin: 0;
        font-size: 85%;
        background-color: rgba(27, 31, 35, 0.05);
        border-radius: 3px;
        font-family: Consolas, "Liberation Mono", Menlo, Courier, monospace;
    }
    
    pre {
        padding: 16px;
        overflow: auto;
        font-size: 85%;
        line-height: 1.45;
        background-color: #f6f8fa;
        border-radius: 3px;
    }
    
    pre code {
        background-color: transparent;
        padding: 0;
        font-size: 100%;
    }
    
    blockquote {
        padding: 0 1em;
        color: #6a737d;
        border-left: 0.25em solid #dfe2e5;
    }
    
    table {
        border-spacing: 0;
        border-collapse: collapse;
    }
    
    table th, table td {
        padding: 6px 13px;
        border: 1px solid #dfe2e5;
    }
    
    table tr {
        background-color: #ffffff;
        border-top: 1px solid #c6cbd1;
    }
    
    table tr:nth-child(2n) {
        background-color: #f6f8fa;
    }
    
    a {
        color: #0366d6;
        text-decoration: none;
    }
    
    a:hover {
        text-decoration: underline;
    }
    
    hr {
        height: 0.25em;
        padding: 0;
        margin: 24px 0;
        background-color: #e1e4e8;
        border: 0;
    }
</style>
"""


def find_wkhtmltopdf():
    """查找 wkhtmltopdf 可执行文件"""
    for path in WKHTMLTOPDF_PATHS:
        if os.path.exists(path):
            return path
    return None


def markdown_to_pdf(md_path, pdf_path, wkhtmltopdf_path=None, logger=None):
    """
    将 Markdown 文件转换为 PDF
    
    Args:
        md_path: Markdown 文件路径
        pdf_path: 输出 PDF 文件路径
        wkhtmltopdf_path: wkhtmltopdf 可执行文件路径
        logger: 日志输出函数
        
    Returns:
        bool: 是否成功
    """
    try:
        if logger:
            logger("正在准备 PDF 转换...")
        
        # 自动查找 wkhtmltopdf
        if not wkhtmltopdf_path:
            wkhtmltopdf_path = find_wkhtmltopdf()
        
        if not wkhtmltopdf_path:
            if logger:
                logger("错误: 未找到 wkhtmltopdf，请安装并配置路径")
            return False
        
        if not os.path.exists(wkhtmltopdf_path):
            if logger:
                logger(f"错误: wkhtmltopdf 不存在于 {wkhtmltopdf_path}")
            return False
        
        if logger:
            logger(f"使用 wkhtmltopdf: {wkhtmltopdf_path}")
        
        # 读取 Markdown 内容
        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # 添加 CSS 样式
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    {GITHUB_CSS}
</head>
<body>
{md_content}
</body>
</html>
"""
        
        # 配置 pdfkit
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        
        options = {
            'encoding': 'UTF-8',
            'quiet': '',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'enable-local-file-access': None
        }
        
        if logger:
            logger("正在转换为 PDF...")
        
        # 转换为 PDF
        pdfkit.from_string(html_content, pdf_path, options=options, configuration=config)
        
        if logger:
            logger(f"PDF 已生成: {pdf_path}")
        
        return True
        
    except Exception as e:
        if logger:
            logger(f"PDF 转换失败: {e}")
        return False