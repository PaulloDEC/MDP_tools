# AutoClapper 2.0 - Complete Setup Guide for New PCs

This guide will walk you through setting up AutoClapper 2.0 on a completely fresh PC with no Python or dependencies installed.

---

## Step 1: Install Python

1. **Download Python:**
   - Go to https://www.python.org/downloads/
   - Download the latest Python 3.x version (3.8 or newer)

2. **Install Python:**
   - Run the installer
   - ⚠️ **CRITICAL:** Check the box that says **"Add Python to PATH"** at the bottom of the first screen
   - ⚠️ **CRITICAL:** Check the box that says **"Install pip"** (usually checked by default)
   - Click "Install Now"
   - Wait for installation to complete

3. **Verify Python is installed:**
   - Open Command Prompt (press `Win + R`, type `cmd`, press Enter)
   - Type: `python --version`
   - You should see something like: `Python 3.12.0`
   - If you get an error, Python is not in your PATH - reinstall and make sure to check that box

4. **Verify pip is installed:**
   - In Command Prompt, type: `pip --version`
   - You should see something like: `pip 23.x.x from ...`
   - If you get an error, try: `python -m pip --version`

---

## Step 2: Copy AutoClapper Files

1. **Create a folder for AutoClapper:**
   - Choose a location (e.g., `C:\AutoClapper`)
   - Create the folder

2. **Copy all AutoClapper files into this folder:**
   - `app.py`
   - `autoclapper-interface.html`
   - `requirements.txt`
   - `start_autoclapper_simple.bat`
   - `README.md`
   - Any other files from the AutoClapper package

3. **Create the templates folder:**
   - Inside your AutoClapper folder, create a folder called `templates`
   - Place these files inside the `templates` folder:
     - `script_template.docx` (your Word template)
     - `clapper_blank.png` (your blank clapper image, 1920x1080)

Your folder structure should look like:
```
C:\AutoClapper\
├── app.py
├── autoclapper-interface.html
├── requirements.txt
├── start_autoclapper_simple.bat
├── README.md
├── templates\
│   ├── script_template.docx
│   └── clapper_blank.png
```

---

## Step 3: Install Python Dependencies

### Method A: Using requirements.txt (Recommended)

1. **Open Command Prompt:**
   - Press `Win + R`, type `cmd`, press Enter

2. **Navigate to your AutoClapper folder:**
   ```
   cd C:\AutoClapper
   ```
   (Replace with your actual path)

3. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **If that fails with an error about "externally-managed-environment":**
   ```
   pip install --break-system-packages -r requirements.txt
   ```

5. **If pip is not in your PATH:**
   ```
   python -m pip install -r requirements.txt
   ```

### Method B: Install Each Package Manually

If Method A doesn't work, install each package one by one:

```
pip install flask
pip install flask-cors
pip install python-docx
pip install Pillow
pip install openai-whisper
```

Or if pip isn't in PATH:

```
python -m pip install flask
python -m pip install flask-cors
python -m pip install python-docx
python -m pip install Pillow
python -m pip install openai-whisper
```

**If you see "externally-managed-environment" errors**, add `--break-system-packages` to each command:

```
pip install --break-system-packages flask
pip install --break-system-packages flask-cors
pip install --break-system-packages python-docx
pip install --break-system-packages Pillow
pip install --break-system-packages openai-whisper
```

### Verify Installation

After installing, verify each package:

```
python -c "import flask; print('Flask OK')"
python -c "import flask_cors; print('Flask-CORS OK')"
python -c "import docx; print('python-docx OK')"
python -c "import PIL; print('Pillow OK')"
python -c "import whisper; print('Whisper OK')"
```

If all five print "OK", you're good to go!

**Note:** The first time you use the "Attempt Auto Transcription" feature, Whisper will automatically download a ~140MB model file. This is normal and only happens once.

---

## Step 4: Run AutoClapper

1. **Double-click `start_autoclapper_simple.bat`**
   - A black Command Prompt window will open (don't close it!)
   - Your web browser should automatically open the AutoClapper interface

2. **If the browser doesn't open automatically:**
   - Open your web browser manually
   - Navigate to: `http://localhost:5000`

3. **Look for the green status indicator** at the top:
   - ✓ Green: "Server connected • Templates found" - you're ready!
   - ⚠️ Orange: "Template files missing" - check your templates folder
   - ✗ Red: "Server not connected" - the Python server isn't running

---

## Common Problems and Solutions

### "Python is not recognized..."
- **Problem:** Python is not installed or not in PATH
- **Solution:** Reinstall Python, making sure to check "Add Python to PATH"

### "pip is not recognized..."
- **Problem:** pip is not in PATH
- **Solution:** Use `python -m pip` instead of just `pip` for all commands

### "ModuleNotFoundError: No module named 'flask'" (or docx, PIL, etc.)
- **Problem:** Dependencies not installed
- **Solution:** Follow Step 3 again to install dependencies

### "error: externally-managed-environment"
- **Problem:** Your Python installation restricts package installation
- **Solution:** Add `--break-system-packages` flag to all pip commands

### Command Prompt closes immediately
- **Problem:** Python error or missing dependencies
- **Solution:** 
  1. Open Command Prompt manually
  2. Navigate to AutoClapper folder: `cd C:\AutoClapper`
  3. Run: `python app.py`
  4. Read the error message and fix the issue

### Browser shows "Could not connect to backend"
- **Problem:** Python server isn't running
- **Solution:** Make sure the Command Prompt window is open and showing the server running

### "Template files missing" warning
- **Problem:** Templates not in the right place
- **Solution:** 
  1. Check that `templates` folder exists in your AutoClapper folder
  2. Check that `script_template.docx` and `clapper_blank.png` are inside it
  3. Check the filenames are exactly correct (case-sensitive)

### Port 5000 already in use
- **Problem:** Another program is using port 5000
- **Solution:** 
  1. Close other programs
  2. Or edit `app.py`, find `port=5000` near the bottom, change to `port=5001`
  3. Then access at `http://localhost:5001` instead

---

## Transferring to Additional PCs

Once you have AutoClapper working on one PC, transferring to others is easy:

1. **Copy the entire AutoClapper folder** to the new PC
2. **Install Python** on the new PC (Step 1)
3. **Install dependencies** on the new PC (Step 3)
4. **Run `start_autoclapper_simple.bat`**

You don't need to reconfigure anything - just install Python and dependencies.

---

## Quick Reference: Essential Commands

**Navigate to AutoClapper folder:**
```
cd C:\AutoClapper
```

**Install all dependencies:**
```
pip install -r requirements.txt
```

**Install dependencies (if pip not in PATH):**
```
python -m pip install -r requirements.txt
```

**Install dependencies (externally-managed environment):**
```
pip install --break-system-packages -r requirements.txt
```

**Check Python version:**
```
python --version
```

**Check pip version:**
```
pip --version
```

**Test if dependencies are installed:**
```
python -c "import flask, flask_cors, docx, PIL; print('All dependencies OK')"
```

**Start server manually:**
```
python app.py
```

---

## Support

If you encounter issues not covered in this guide:

1. Check the error message in the Command Prompt window
2. Make sure Python 3.8+ is installed with pip
3. Make sure all dependencies are installed
4. Make sure the templates folder exists with both template files
5. Try running `python app.py` directly to see detailed error messages

---

## Summary Checklist

- [ ] Python 3.8+ installed with "Add to PATH" checked
- [ ] pip is working (`pip --version`)
- [ ] All AutoClapper files copied to a folder
- [ ] `templates` folder created with both template files
- [ ] Flask installed (`pip install flask`)
- [ ] Flask-CORS installed (`pip install flask-cors`)
- [ ] python-docx installed (`pip install python-docx`)
- [ ] Pillow installed (`pip install Pillow`)
- [ ] Whisper installed (`pip install openai-whisper`)
- [ ] `start_autoclapper_simple.bat` runs without errors
- [ ] Browser opens and shows green "Server connected" status

If all boxes are checked, AutoClapper 2.0 is ready to use!
