from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import os
import urllib.parse

# === Constants ===
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "http_audit.log")
PORT = 80

# === Ensure Logging Directory ===
os.makedirs(LOG_DIR, exist_ok=True)

# === Logging Setup ===
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# === Helper for Common HTML Headers ===
def html_headers(handler):
    handler.send_response(200)
    handler.send_header('Content-type', 'text/html')
    handler.end_headers()

# === Honeypot Request Handler ===
class WordPressHoneypotHandler(BaseHTTPRequestHandler):
    def log_request_data(self, method, post_data=None):
        ip = self.client_address[0]
        path = self.path
        headers = str(self.headers).replace("\n", " | ")
        log_msg = f"{ip} {method} {path} | {headers}"
        if post_data:
            log_msg += f" | POST Data: {post_data}"
        logging.info(log_msg)

    def do_GET(self):
        self.log_request_data("GET")

        if self.path == "/wp-login.php":
            html_headers(self)
            self.wfile.write("""
            <html>
            <head>
                <title>Log In · WordPress</title>
                <link rel='stylesheet' href='https://s.w.org/wp-includes/css/buttons.min.css'>
                <style>
                    body { background: #f1f1f1; font-family: Arial, sans-serif; }
                    #login { width: 320px; margin: 100px auto; padding: 26px 24px; background: #fff; box-shadow: 0 1px 3px rgba(0,0,0,0.13); }
                    .button-primary { background: #2271b1; border-color: #2271b1; color: #fff; text-decoration: none; }
                    .button-primary:hover { background: #135e96; border-color: #135e96; }
                    img { width: 84px; height: 84px; margin: 0 auto 20px; display: block; }
                </style>
            </head>
            <body>
                <div id='login'>
                    <img src='https://s.w.org/about/images/logos/wordpress-logo-notext-rgb.png' alt='WordPress logo'>
                    <h1><a href='https://wordpress.org/'>WordPress</a></h1>
                    <form method='POST' action='/wp-login.php'>
                        <p><label for='user_login'>Username<br />
                        <input type='text' name='log' id='user_login' class='input' value='' size='20' /></label></p>
                        <p><label for='user_pass'>Password<br />
                        <input type='password' name='pwd' id='user_pass' class='input' value='' size='20' /></label></p>
                        <p class='submit'><input type='submit' name='wp-submit' id='wp-submit' class='button button-primary button-large' value='Log In' /></p>
                    </form>
                    <p id='nav'><a href='/wp-login.php?action=lostpassword'>Lost your password?</a></p>
                </div>
            </body>
            </html>
            """.encode())

        elif self.path == "/wp-admin/":
            html_headers(self)
            self.wfile.write("""
            <html><head><title>Dashboard · WordPress</title></head>
            <body>
            <h1>Dashboard</h1>
            <p>Welcome back, <strong>admin</strong>!</p>
            <p><a href='/wp-admin/edit.php'>Edit Posts</a></p>
            <p><a href='/wp-admin/plugins.php'>Manage Plugins</a></p>
            <p><a href='/wp-admin/themes.php'>Customize Theme</a></p>
            <p><a href='/secrets.txt'>Download Database Backup</a></p>
            </body></html>
            """.encode())

        elif self.path == "/wp-admin/edit.php":
            html_headers(self)
            self.wfile.write("""
            <html><head><title>Edit Posts</title></head><body>
            <h2>Posts</h2>
            <ul>
              <li><strong>Hello World</strong> - <a href='/wp-admin/edit.php?post=1'>Edit</a></li>
              <li>Sample Blog Post - <a href='/wp-admin/edit.php?post=2'>Edit</a></li>
              <li>Click here for sale: <a href='/product?id=1%27%20OR%201=1--'>/product?id=1' OR 1=1--</a></li>
              <li><a href='/search?q=%3Cscript%3Ealert(1)%3C/script%3E'>Try our search feature</a></li>
            </ul>
            </body></html>
            """.encode())

        elif self.path == "/wp-admin/plugins.php":
            html_headers(self)
            self.wfile.write("""
            <html><head><title>Plugins</title></head><body>
            <h2>Installed Plugins</h2>
            <ul>
              <li>SEO Pro - Active</li>
              <li>Contact Form 7 - Inactive</li>
              <li>Shell Uploader - Active <a href='/wp-content/plugins/shell.php'>[open]</a></li>
            </ul>
            </body></html>
            """.encode())

        elif self.path == "/wp-admin/themes.php":
            html_headers(self)
            self.wfile.write("""
            <html><head><title>Themes</title></head><body>
            <h2>Theme Manager</h2>
            <p>Active Theme: <strong>TwentyTwentyOne</strong></p>
            <p><img src='https://s.w.org/images/themes/twentytwentyone.png' width='300' /></p>
            </body></html>
            """.encode())

        elif self.path == "/secrets.txt":
            html_headers(self)
            self.wfile.write("""
            admin_username=admin
            admin_password=P@ssw0rd123!
            db_user=wordpress
            db_pass=wpsecret
            api_key=ABCD-1234-XYZ
            """.encode())

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"<html><body><h3>404 - Not Found</h3></body></html>")

    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        data = self.rfile.read(length).decode('utf-8', errors='ignore')
        post_parsed = urllib.parse.parse_qs(data)
        self.log_request_data("POST", post_data=post_parsed)

        if self.path == "/wp-login.php":
            html_headers(self)
            self.wfile.write(b"<html><body><h3>Error: The password you entered for the username is incorrect.</h3></body></html>")

        elif self.path == "/xmlrpc.php":
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<methodResponse><fault><value><string>Invalid method call</string></value></fault></methodResponse>")

        elif self.path == "/wp-login.php?action=lostpassword":
            html_headers(self)
            self.wfile.write(b"<html><body><h3>Password reset link sent to your email address.</h3></body></html>")

        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"<html><body><h3>404 - POST Not Found</h3></body></html>")

# === Start the Honeypot Server ===
def run(server_class=HTTPServer, handler_class=WordPressHoneypotHandler, port=PORT):
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, handler_class)
    print(f"[+] WordPress Honeypot running on port {port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
