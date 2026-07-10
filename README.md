# FRC Team 2658 Packing System

Flask dynamic checklist website used for packing up for FRC competitions

## Quick Start (Local)
Requires python 3.12
python 3.14 is stinky and flask doesnt work on that yet

```powershell
# 1. Create virtual environment and install dependencies
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt

# 2. Create your .env file, it must have these entries
CHECKLIST_ADMIN_PW = 'your-password'
FLASK_SECRET = 'a-random-secret-string' <- Flask needs this for secure data transmission n stuff. just slam your keyboard lowk
LOG_ON_PASSWORD = 'random password required to join website'

# 3. Run
python app.py
```

Open http://localhost:5000 in your browser. You'll be prompted to enter a username to join.

## Usage

### Regular Users
- Enter a name and use a password from a lead.
- Switch between Tools list and Screws & Parts list using dropdown
- Browse list, view in detail
- Check and uncheck items, people can see who checked off an item

### Leads (Admins)
- Visit a leads page to add and remove items
- Clear database

## Adding Location Pictures

Each item has a Where to put field that shows a picture on the detail page.
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

The application will automatically display the matching image for an item's location on the detail page. If no image exists for a location, it shows a placeholder.

### Customising the Location Images

Edit the `LOCATIONS` list in `app.py` to add, remove, or rename locations:

```python
LOCATIONS = ['Drawer 1', 'Drawer 2', 'Drawer 3']
```

### im hungry