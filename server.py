"""纯静态文件服务器 — 路由映射 frontend/ 和 output/"""
import http.server
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080


class Router(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # 解码 URL 编码（中文路径）
        import urllib.parse
        path = urllib.parse.unquote(path, errors='surrogatepass')
        # 首页
        if path == "/" or path == "/index.html":
            return os.path.join(BASE, "frontend/index.html")
        # 共享文件 和 库文件
        if path.startswith("/lib/") or path.startswith("/shared/"):
            return os.path.join(BASE, "frontend", path.lstrip("/"))
        # 输出文件 (algo, sql, index.json)
        if path.startswith("/algo/") or path.startswith("/sql/") or path == "/index.json" or path.startswith("/progress"):
            p = os.path.join(BASE, "output", path.lstrip("/"))
            # clean URL: 自动补 .html
            if not os.path.splitext(p)[1] and not os.path.exists(p):
                p += ".html"
            return p
        # 其他 frontend 文件
        return os.path.join(BASE, "frontend", path.lstrip("/"))

    def log_message(self, fmt, *args):
        # 简洁日志
        print(f"  {args[0]}", flush=True)


print(f"🚀 服务运行中 → http://localhost:{PORT}")
print(f"   按 Ctrl+C 停止\n")
http.server.HTTPServer(("0.0.0.0", PORT), Router).serve_forever()
