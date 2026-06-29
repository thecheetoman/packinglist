# Packing List Checklist

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

## Hosting on Render (Free Tier)

### Why PostgreSQL?
Render's filesystem is **ephemeral** — your SQLite database would reset on every deploy or after 15 minutes of inactivity (free tier). Switching to **PostgreSQL** keeps your data safe across restarts. Render's free PostgreSQL tier (1 GB) is plenty for this app.

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/packinglist.git
git push -u origin main
```

### Step 2: Create a PostgreSQL Database

1. Go to https://dashboard.render.com and click **New +** → **PostgreSQL**.
2. Fill in:
   - **Name**: `packinglist-db`
   - **Database**: `packinglist` (or leave default)
   - **User**: `packinglist` (or leave default)
   - **Region**: pick one close to you
3. Click **Create Database**.
4. Once created, copy the **Internal Database URL** (starts with `postgres://...`). You'll need this in the next step.

### Step 3: Deploy the Web Service

1. On the Render dashboard, click **New +** → **Web Service**.
2. Connect your GitHub repository.
3. Fill in:
   - **Name**: `packinglist`
   - **Region**: same as your database
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Instance Type**: **Free**
4. Click **Create Web Service**.

### Step 4: Set Environment Variables

After creation, go to your web service's **Environment** tab and add:

| Variable             | Value                        |
|----------------------|------------------------------|
| `DATABASE_URL`       | Paste the **Internal Database URL** from step 2 |
| `CHECKLIST_ADMIN_PW` | Your admin password           |
| `FLASK_SECRET`       | A random secret string        |

### Step 5: Deploy & Verify

Click **Manual Deploy** → **Deploy latest commit**. Wait for the build to finish, then visit the `.onrender.com` URL.

Your data will persist across restarts, spin-downs, and redeploys.

### Adding Location Pictures on Render

Upload images to `static/images/locations/` via the Render dashboard's **Shell** tab or include them in your repo (place them in `static/images/locations/` before pushing).

## Environment Variables

| Variable             | Default                           | Description                          |
|----------------------|-----------------------------------|--------------------------------------|
| `DATABASE_URL`       | `sqlite:///instance/checklist.db` | PostgreSQL connection string         |
| `CHECKLIST_ADMIN_PW` | `changeme`                        | Password for the Leads admin panel   |
| `FLASK_SECRET`       | `dev-secret`                      | Flask session secret (set a real one) |

## Database

- **Locally**: SQLite at `instance/checklist.db` (auto-created).
- **On Render**: PostgreSQL via `DATABASE_URL` environment variable.
- Tables are created automatically on first run. No manual setup needed.
