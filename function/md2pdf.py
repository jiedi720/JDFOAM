"""PDF 转换模块

该模块提供将 Markdown 文档转换为 PDF 文件的功能，使用 wkhtmltopdf 工具，
支持代码高亮、表格渲染等高级格式，生成美观的 PDF 文档。
功能包括：
- Markdown 到 HTML 的转换
- 自定义 CSS 样式注入
- 代码块语法高亮
- 表格和列表格式化
- 支持进度回调和日志输出
"""

import os
import markdown2
import pdfkit


def markdown_to_pdf(md_path, pdf_path, wkhtmltopdf_path=None, logger=None, progress_callback=None):
    """
    将 Markdown 文件转换为 PDF

    使用 wkhtmltopdf 工具将 Markdown 文件转换为高质量的 PDF 文档，
    转换过程包括：Markdown 解析 -> HTML 生成 -> CSS 样式注入 -> PDF 生成

    Args:
        md_path (str): Markdown 文件路径
        pdf_path (str): 输出 PDF 文件路径
        wkhtmltopdf_path (str): wkhtmltopdf 可执行文件路径
        logger (callable): 日志输出函数
        progress_callback (callable): 进度回调函数，接收0-100的进度值

    Returns:
        bool: 是否成功
    """
    # 检查 MD 文件是否存在
    if not md_path or not os.path.exists(md_path):
        if logger:
            logger("错误：未找到生成的 Markdown 文件！请确保已先执行合并为 Markdown")
        return False

    # 如果没有指定 pdf_path，则自动生成
    if not pdf_path:
        pdf_path = md_path.replace(".md", ".pdf")

    # 如果没有指定 wkhtmltopdf 路径，使用默认路径
    if not wkhtmltopdf_path:
        wkhtmltopdf_path = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"

    # 检查 wkhtmltopdf 是否存在
    if not os.path.exists(wkhtmltopdf_path):
        if logger:
            logger(f"错误：未找到 wkhtmltopdf，路径：{wkhtmltopdf_path}")
        return False

    if logger:
        logger(f"正在转换 PDF，请稍候...")

    # 更新进度：初始化
    if progress_callback:
        progress_callback(10)

    # 指定 wkhtmltopdf 的安装路径
    config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)

    try:
        # 更新进度：开始读取文件
        if progress_callback:
            progress_callback(20)

        with open(md_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

            # 更新进度：解析 Markdown
            if progress_callback:
                progress_callback(30)

            # 将 Markdown 转换为带有扩展功能的 HTML
            # 启用代码块、表格和换行符扩展
            html_body = markdown2.markdown(md_content, extras=["fenced-code-blocks", "tables", "break-on-newline"])

            # 更新进度：生成样式
            if progress_callback:
                progress_callback(50)

            # 注入精美样式，为 PDF 生成优化的 CSS
            full_html = f"""
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    body {{
                        font-family: 'Segoe UI', Arial, sans-serif;
                        padding: 40px;
                        line-height: 1.6;
                        color: #333;
                    }}
                    pre {{
                        background: #f6f8fa;
                        padding: 16px;
                        border-radius: 6px;
                        border: 1px solid #ddd;
                        white-space: pre-wrap;
                        font-size: 12px;
                    }}
                    code {{
                        font-family: 'Consolas', 'Courier New', monospace;
                        color: #000;
                    }}
                    h2 {{
                        border-bottom: 2px solid #eaecef;
                        padding-bottom: 5px;
                        margin-top: 40px;
                        color: #0366d6;
                    }}
                    a {{
                        color: #0366d6;
                        text-decoration: none;
                    }}
                    ul {{
                        background: #f1f8ff;
                        padding: 20px 40px;
                        border-radius: 8px;
                    }}
                </style>
            </head>
            <body>{html_body}</body>
            </html>
            """

            # 更新进度：开始转换
            if progress_callback:
                progress_callback(70)

            # 使用指定配置执行转换
            # 将 HTML 内容转换为 PDF 文件
            pdfkit.from_string(full_html, pdf_path, configuration=config)

            # 更新进度：转换完成
            if progress_callback:
                progress_callback(95)

            if logger:
                logger(f"成功！PDF 已生成在源目录：\n{pdf_path}")

            # 完成：更新进度到100%
            if progress_callback:
                progress_callback(100)

            return True

    except Exception as e:
        if logger:
            logger(f"PDF 转换失败: {str(e)}")
        return False