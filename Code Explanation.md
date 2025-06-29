# 📘 WordPress Honeypot — Code Explanation

---

## `class WordPressHoneypotHandler(BaseHTTPRequestHandler)`

This is the main class that handles incoming HTTP requests. It inherits from `BaseHTTPRequestHandler` and processes both GET and POST requests made to the honeypot server.

---

## `def log_request_data(self, method, post_data=None):`

**Purpose:** Logs incoming request metadata including client IP, HTTP method, path, headers, and optionally POST data.

**Logic:**

```python
ip = self.client_address[0]
path = self.path
headers = str(self.headers).replace("\n", " | ")
log_msg = f"{ip} {method} {path} | {headers}"
if post_data:
    log_msg += f" | POST Data: {post_data}"
logging.info(log_msg)
```

**Explanation:**

* Captures and logs attacker interaction details.
* Formats headers to be single-line for better log readability.
* Appends POST data if present.

---

## `def html_headers(handler):`

**Purpose:** Sends a generic HTTP 200 OK response with `Content-type: text/html`.

```python
handler.send_response(200)
handler.send_header('Content-type', 'text/html')
handler.end_headers()
```

**Explanation:**
Used to simplify sending standard HTML headers before serving any HTML page content.

---

## `def do_GET(self):`

**Purpose:** Handles all incoming GET requests and serves fake WordPress pages based on `self.path`.

```python
if self.path == "/wp-login.php":
    html_headers(self)
    self.wfile.write(b"...login page HTML...")

elif self.path == "/wp-admin/":
    html_headers(self)
    self.wfile.write(b"...dashboard HTML...")

...
```

**Explanation:**

* Uses conditional statements to simulate multiple fake WordPress paths.
* Includes vulnerable-looking links (`SQLi`, `XSS`) to lure attackers.
* All served HTML is static but mimics real WordPress interfaces.

---

## `def do_POST(self):`

**Purpose:** Handles all POST requests, typically for login attempts and form submissions.

```python
length = int(self.headers.get('Content-Length', 0))
data = self.rfile.read(length).decode('utf-8', errors='ignore')
post_parsed = urllib.parse.parse_qs(data)
self.log_request_data("POST", post_data=post_parsed)
```

**Explanation:**

* Extracts and decodes the POST body.
* Logs the payload to monitor brute-force or malicious attempts.
* Responds with generic error messages to maintain deception.

---

## `elif self.path == "/secrets.txt":`

**Purpose:** Simulates a leaked file containing sensitive credentials.

```python
self.wfile.write(b"""
admin_username=admin
admin_password=P@ssw0rd123!
db_user=wordpress
db_pass=wpsecret
api_key=ABCD-1234-XYZ
""")
```

**Explanation:**

* Creates a honeypot trap.
* If the attacker downloads this file, it can trigger alerts or monitoring mechanisms.

---

## `def run(...)`

**Purpose:** Boots the HTTP server and binds it to port 80 (or another port if specified).

```python
server_address = ('0.0.0.0', port)
httpd = server_class(server_address, handler_class)
httpd.serve_forever()
```

**Explanation:**

* Listens on all interfaces.
* Runs indefinitely, handling every incoming connection using `WordPressHoneypotHandler`.

---

Let me know if you'd like this turned into a printable PDF or pushed to a GitHub Markdown-ready version.
