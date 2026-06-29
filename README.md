# Packing List Checklist ts read me by ai

A Flask web app for managing a packing checklist with two modes: **Tools** and **Screws & Parts**. Users sign in with a username and check off items. Leads (admins) add and manage items via a password-protected panel.

## Quick Start (Local)

```powershell
# 1. Create virtual environment and install dependencies
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# 2. (Optional) Set environment variables
$Env:CHECKLIST_ADMIN_PW = 'your-password'
$Env:FLASK_SECRET = 'a-random-secret-string'

# 3. Run
python app.py
```

Open http://127.0.0.1:5000 in your browser. You'll be prompted to enter a username to join.

## Usage

### Regular Users
- Enter any username on the join page to sign in (or register if new).
- Switch between **Tools** and **Screws & Parts** using the dropdown in the header.
- Browse the list, click an item to see its full details (including the **where-to-put picture**).
- On the detail page, click **Check / Uncheck** to toggle an item. Checked items show who checked them.

### Leads (Admins)
- Visit `/leads/login` and enter the admin password (default: `changeme`).
- Once logged in, the header shows **BUILD LEAD MODE**.
- Go to `/leads` to add new tools or screws/parts, each with a location, find-spot, and quantity.
- Leads cannot check off items — that's for regular users only.

## Adding Location Pictures

Each item has a **Where to put** field that shows a picture on the detail page.
To add pictures for locations:

```powershell
# 1. Create the static folder
mkdir static
mkdir static\images
mkdir static\images\locations

# 2. Drop your images in there (PNG, JPG, or WebP)
#    Name them to match the location exactly, e.g.:
#    static/images/locations/Drawer 1.png
#    static/images/locations/Drawer 2.png
#    static/images/locations/Drawer 3.png
#    static/images/locations/Shelf A.png
#    static/images/locations/Shelf B.png
#    static/images/locations/Cabinet.png
#    static/images/locations/Closet.png
#    static/images/locations/Under Bed.png
#    static/images/locations/Other.png
```

The app will automatically display the matching image for an item's location on the detail page. If no image exists for a location, it shows a placeholder.

### Customising the Location Images

Edit the `LOCATIONS` list in `app.py` to add, remove, or rename locations:

```python
LOCATIONS = ['Drawer 1', 'Drawer 2', 'Drawer 3', 'Shelf A', 'Shelf B',
             'Cabinet', 'Closet', 'Under Bed', 'Other']
```

## Hosting the Website

### Option A: PythonAnywhere (easiest — free tier works)

1. Create an account at https://www.pythonanywhere.com.
2. Go to the **Dashboard &rarr; Files** tab and upload your project files (or clone from GitHub).
3. Go to **Dashboard &rarr; Web** and **Add a new web app**.
   - Choose **Manual configuration**, then **Python 3.x**.
4. In the **Code** section:
   - Set **Source code** to the path of your project folder (e.g. `/home/yourname/packinglist`).
   - Set **Working directory** to the same path.
5. Install dependencies by opening a **Bash console** and running:
   ```bash
   pip install --user -r /home/yourname/packinglist/requirements.txt
   ```
6. Create a WSGI file — click the **WSGI configuration file** link and replace its contents with:
   ```python
   import sys
   sys.path.insert(0, '/home/yourname/packinglist')
   from app import app as application
   ```
7. In the **Environment variables** section (under Web), add:
   - `CHECKLIST_ADMIN_PW` = your admin password
   - `FLASK_SECRET` = a random secret string
8. **Reload** your web app from the green button.
9. Upload your location images to `static/images/locations/` via the Files tab.

### Option B: Railway / Render / Fly.io (cheap paid)

These platforms deploy from a GitHub repo. You'll need a `requirements.txt` (already included) and a `Procfile` for some of them:

Create a `Procfile`:
```
web: gunicorn app:app
```

If deploying, add `gunicorn` to `requirements.txt`:
```
gunicorn==23.0.0
```

Then connect your GitHub repo to the platform and set the environment variables (`CHECKLIST_ADMIN_PW`, `FLASK_SECRET`) in their dashboard.

### Option C: VPS (DigitalOcean, Linode, etc.)

```bash
# SSH into your server
git clone https://github.com/yourname/packinglist.git
cd packinglist

# Set up Python
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install gunicorn

# Run with Gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

Use a reverse proxy (nginx / Caddy) to serve the app on port 80/443.

## Environment Variables

| Variable             | Default      | Description                          |
|----------------------|--------------|--------------------------------------|
| `CHECKLIST_ADMIN_PW` | `changeme`   | Password for the Leads admin panel   |
| `FLASK_SECRET`       | `dev-secret` | Flask session secret (set a real one) |

## Database

SQLite database is stored at `instance/checklist.db`. It is created and migrated automatically on first run. No manual setup needed.
