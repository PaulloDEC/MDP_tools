# AutoClapper 2.0 - Quick Start Guide

## Getting Started (Easiest Way!)

### The One-Click Method

1. **Set up your templates folder** (one-time setup):
   - Create a folder named `templates` in your AutoClapper folder
   - Place these files inside:
     - `script_template.docx` (your Word template)
     - `clapper_blank.png` (your blank clapper image)

2. **Double-click `start_autoclapper.bat`**
   - That's it! The batch file handles everything automatically.
   - It will install dependencies, start the server, and open your browser.

3. **Keep the black window (Command Prompt) open** while using AutoClapper
   - Don't close it until you're done!

---

## Getting Started (Manual Method)

If you prefer to do things manually or need more control:

### Step 1: Install Python Dependencies

1. Open Command Prompt (press `Win + R`, type `cmd`, press Enter)
2. Navigate to your AutoClapper folder:
   ```
   cd C:\path\to\your\autoclapper\folder
   ```
3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

### Step 2: Set Up Template Folder

1. Create a folder named `templates` in your AutoClapper folder
2. Place these files inside the `templates` folder:
   - `script_template.docx` (your Word template)
   - `clapper_blank.png` (your blank clapper image)

Your folder structure should look like:
```
autoclapper/
├── app.py
├── autoclapper-interface.html
├── requirements.txt
├── templates/
│   ├── script_template.docx
│   └── clapper_blank.png
```

### Step 3: Start the Python Server

1. In Command Prompt (in your AutoClapper folder), run:
   ```
   python app.py
   ```

2. You should see output like:
   ```
   Script template path: C:\...\templates\script_template.docx
   Clapper template path: C:\...\templates\clapper_blank.png
   Starting AutoClapper 2.0 server on http://localhost:5000
    * Running on http://127.0.0.1:5000
   ```

3. **IMPORTANT**: Keep this Command Prompt window open! If you close it, the server stops.

### Step 4: Open the Web Interface

1. Double-click `autoclapper-interface.html` to open it in your web browser
   - OR navigate to `http://localhost:5000` in your browser
   - OR right-click the HTML file and choose "Open with" > your browser

2. You should now see the AutoClapper 2.0 interface

## Troubleshooting "Could not connect to backend" Error

This error means the HTML page can't reach the Python server. Here's how to fix it:

### Check 1: Is the Python server running?
- Look for the Command Prompt window where you ran `python app.py`
- It should be open and showing "Running on http://127.0.0.1:5000"
- If you closed it, open Command Prompt again and run `python app.py`

### Check 2: Is Python installed correctly?
Try running in Command Prompt:
```
python --version
```
You should see something like "Python 3.8.0" or newer.

### Check 3: Are the templates found?
When you start `python app.py`, check the output. It should show:
```
Script template path: C:\...\templates\script_template.docx
Clapper template path: C:\...\templates\clapper_blank.png
```

If it shows incorrect paths or can't find files, check that:
- The `templates` folder exists in the same folder as `app.py`
- Your template files are named exactly: `script_template.docx` and `clapper_blank.png`

### Check 4: Test the server directly
Open your web browser and go to:
```
http://localhost:5000/health
```

You should see JSON output showing template status. If this works, the server is running correctly.

## Common Issues

**Batch file won't run / "Windows protected your PC"**
- Right-click `start_autoclapper.bat` and choose "Run as administrator"
- Or: Right-click > Properties > Unblock (if there's an Unblock button)

**"pip is not recognized"**
- Python might not be installed or not in your PATH
- Download Python from python.org and reinstall, making sure to check "Add Python to PATH"

**"ModuleNotFoundError: No module named 'flask'"**
- The dependencies aren't installed
- Run `pip install -r requirements.txt` again

**"Template not found" errors**
- Check that your `templates` folder is in the correct location
- Check that filenames match exactly (case-sensitive)

**Generated files don't appear**
- Make sure the output directory path is correct (e.g., `C:\Output`)
- Check you have write permissions for that folder
- The folder will be created automatically if it doesn't exist

## Usage Flow

Once everything is running:

1. **Leave the Command Prompt open** (with `python app.py` running)
2. **Open the HTML file** in your browser
3. **Enter output directory** (e.g., `C:\Users\YourName\Documents\Scripts`)
4. **Fill in all the fields**
5. **Click "Create and Save Documents"**
6. **Check the status messages** for confirmation
7. **Find your files** in the output directory you specified

## Stopping the Server

When you're done:
- Go to the Command Prompt window where `python app.py` is running
- Press `Ctrl + C` to stop the server
- You can close the window

## Need Help?

If you're still having issues:
1. Make sure you completed all steps in order
2. Check that the Command Prompt window with the server is still open
3. Try closing and reopening the HTML file in your browser
4. Try restarting the Python server (Ctrl+C, then run `python app.py` again)
