# Packing List Checklist (Flask)

Simple Flask app to let one person (admin) add checklist entries and others check them off.

Quick start

1. Create virtualenv and install:

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

2. (Optional) Set admin password and secret:

```powershell
$Env:CHECKLIST_ADMIN_PW = 'yourpassword'
$Env:FLASK_SECRET = 'a-random-secret'
```

3. Run:

```powershell
python app.py
```

4. Visit http://127.0.0.1:5000/ to view checklist. Admin portal at /admin (login at /admin/login).

Default admin password: `changeme` (set `CHECKLIST_ADMIN_PW` in env to secure)
# packinglist
prob
