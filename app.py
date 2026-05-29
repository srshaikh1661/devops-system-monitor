from http.server import SimpleHTTPRequestHandler, HTTPServer
import psutil
import json

class MonitorHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        # Gather live Windows system stats using psutil
        cpu_usage = psutil.cpu_percent(interval=None)
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('C:\\').percent
        
        # Build a clean HTML visual container dashboard
        html_dashboard = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>DevOps System Monitor</title>
            <meta charset="UTF-8">
            <meta http-equiv="refresh" content="3">
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; background: #f0f2f5; text-align: center; padding: 40px; }}
                .container {{ background: white; max-width: 600px; margin: 0 auto; padding: 30px; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
                h1 {{ color: #1a202c; margin-bottom: 30px; }}
                .metric {{ margin: 20px 0; padding: 15px; border-radius: 8px; background: #f7fafc; }}
                .label {{ font-weight: bold; font-size: 14pt; color: #4a5568; }}
                .value {{ font-size: 24pt; font-weight: bold; color: #2b6cb0; margin-top: 5px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>💻 Live Server Health Monitor</h1>
                <div class="metric">
                    <div class="label">CPU Usage</div>
                    <div class="value">{cpu_usage}%</div>
                </div>
                <div class="metric">
                    <div class="label">RAM Usage</div>
                    <div class="value">{ram_usage}%</div>
                </div>
                <div class="metric">
                    <div class="label">Disk Space Used (C:)</div>
                    <div class="value">{disk_usage}%</div>
                </div>
                <p style="color: #a0aec0; font-size: 9pt;">Page auto-refreshes every 3 seconds</p>
            </div>
        </body>
        </html>
        """
        self.wfile.write(bytes(html_dashboard, "utf-8"))

# Listen on port 8001 so it doesn't conflict with your first project
server = HTTPServer(('0.0.0.0', 8001), MonitorHandler)
print("Monitoring system online on port 8001...")
server.serve_forever()