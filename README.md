
# 🕵️‍♂️ WordPress Honeypot

A fake but realistic WordPress site written in Python using `http.server`, designed to deceive attackers and capture their activity. It simulates vulnerable WordPress endpoints (like `wp-login.php`, `wp-admin`, and plugins) with intentional security flaws such as XSS, SQL Injection, and exposed secrets — perfect for research, detection, and monitoring.

---

## 📌 Features

- Simulated WordPress UI with realistic login page and admin dashboard
- Vulnerable endpoints:
  - **XSS**: `/search?q=<script>alert(1)</script>`
  - **SQLi**: `/product?id=1' OR 1=1--`
  - **Exposed secrets**: `/secrets.txt`
  - **Fake file upload backdoor**: `/wp-content/plugins/shell.php`
- Logs all HTTP requests with full headers and POST data
- Easy to run with no dependencies
---

## 🛠️ How to Run

```bash
sudo python3 web_honeypot.py
```

> ⚠️ Run with `sudo` only if port 80 is required.

---

## 🔍 Example Vulnerable Paths

| Endpoint                    | Type     | Description                             |
|----------------------------|----------|-----------------------------------------|
| `/wp-login.php`            | Auth     | Fake login page                         |
| `/wp-admin/`               | Panel    | Admin dashboard simulation              |
| `/product?id=1' OR 1=1--`  | SQLi     | Simulated SQL Injection link            |
| `/search?q=<script>`       | XSS      | Reflected XSS vulnerability             |
| `/wp-content/plugins/shell.php` | Upload   | Fake backdoor uploader                 |
| `/secrets.txt`             | InfoLeak | Exposed credentials & API key           |

---

## 📜 Sample Logged Request

```
192.168.0.5 GET /wp-login.php | Host: ... | User-Agent: ... | ...
```

---

## 📎 Credentials for Testing

- **Username:** admin  
- **Password:** P@ssw0rd123!

---

## ⚠️ Disclaimer

This honeypot is for **educational and research purposes only**. Do **NOT** expose it to the internet without proper monitoring. Unauthorized use or entrapment laws may apply in some jurisdictions.

---

## 📧 Contact

Made by [Abdullah Banwair](https://github.com/Rzfn2) — feel free to reach out!
