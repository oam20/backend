# .exe File Deployment Guide

## Overview

This guide explains how to set up the .exe file download system where:
1. User submits the form
2. .exe file downloads automatically
3. User runs the .exe file
4. Popup window appears (like System Requirements Lab)
5. System details are collected and sent to database

## Step 1: Build the .exe File

### Option A: Using the Batch Script (Windows)

1. Open Command Prompt in the project directory
2. Run:
   ```bash
   build_exe.bat
   ```

### Option B: Using Python Script

1. Install PyInstaller:
   ```bash
   pip install pyinstaller
   ```

2. Run the build script:
   ```bash
   python build_exe.py
   ```

### Option C: Manual Build

```bash
pyinstaller --onefile --windowed --name=SystemCollector --add-data="get_system_details.py;." --hidden-import=requests --hidden-import=psutil --hidden-import=tkinter system_collector_gui.py
```

The .exe file will be created in the `dist/` folder as `SystemCollector.exe`

## Step 2: Host the .exe File

You need to host the `SystemCollector.exe` file so users can download it. Options:

### Option A: GitHub Releases
1. Create a GitHub repository
2. Upload `SystemCollector.exe` to Releases
3. Get the direct download URL

### Option B: Your Web Server
1. Upload `SystemCollector.exe` to your web server
2. Make it accessible via HTTPS
3. Update the URL in `form-example.html`

### Option C: Cloud Storage
- Upload to Google Drive, Dropbox, or OneDrive
- Get a direct download link
- Update the URL in the form

### Option D: CDN/File Hosting
- Use services like:
  - jsDelivr
  - unpkg
  - Your own CDN

## Step 3: Update the Form

Update `form-example.html` with your .exe file URL:

```javascript
// Line ~190 - Update this URL
const EXE_URL = 'https://your-server.com/SystemCollector.exe';
// Or use relative path if hosting on same domain
const EXE_URL = '/SystemCollector.exe';
```

## Step 4: How It Works

### User Flow:

1. **User fills form** → Employee ID, Email, Department
2. **User clicks Submit** → Form validates and sends basic data
3. **Form downloads .exe** → `SystemCollector.exe` downloads automatically
4. **User runs .exe** → Popup window appears (like System Requirements Lab)
5. **System collects data** → Collects all Windows system details
6. **Data sent to API** → Sends complete system details to your API
7. **Success message** → Window closes with success message

### Technical Flow:

```
Form Submit
    ↓
Send basic data to API (optional - can skip this)
    ↓
Download SystemCollector.exe
    ↓
User runs .exe
    ↓
GUI window opens (System Requirements Lab style)
    ↓
Collect system details (using get_system_details.py)
    ↓
Send complete data to API with system_details
    ↓
Show success message
    ↓
Close window
```

## Step 5: Testing

1. Build the .exe file
2. Test locally:
   ```bash
   dist\SystemCollector.exe
   ```
3. Test with parameters:
   ```bash
   dist\SystemCollector.exe "EMP001,user@example.com,IT,https://backend-blue-beta.vercel.app"
   ```
4. Verify it collects and sends data correctly

## Step 6: Distribution

### Option A: Direct Download from Form
- Host .exe on your server
- Form automatically downloads it on submit
- User runs it

### Option B: Manual Download Link
- Provide a download link on your website
- User downloads and runs manually
- .exe prompts for Employee ID, Email, Department

### Option C: Both
- Form downloads .exe automatically
- Also provide manual download link as backup

## Customization

### Change Window Title
Edit `system_collector_gui.py`:
```python
self.root.title("Your Custom Title")
```

### Change Version Number
Edit `system_collector_gui.py`:
```python
version_label = tk.Label(..., text="v 1.0.0", ...)
```

### Add Icon
1. Create an `.ico` file
2. Update build command:
   ```bash
   pyinstaller --icon=icon.ico ...
   ```

### Customize Colors
Edit the color values in `system_collector_gui.py`:
- `#4CAF50` - Green (success/checkmarks)
- `#2196F3` - Blue (progress)
- `#333333` - Dark grey (text)

## Troubleshooting

### .exe file is too large
- Use `--onefile` creates a single file (larger)
- Use `--onedir` for a folder (smaller files, but multiple files)

### .exe doesn't run
- Check Windows Defender/Antivirus (may block unsigned .exe)
- Test on a clean Windows machine
- Check if all dependencies are included

### Data not sending
- Check API URL is correct
- Check internet connection
- Check firewall settings
- Verify API endpoint is accessible

### GUI doesn't appear
- Check if tkinter is installed
- Try running from command line to see errors
- Check if Windows has required libraries

## Security Considerations

1. **Code Signing**: Consider signing the .exe to avoid Windows warnings
2. **Antivirus**: May flag unsigned executables
3. **HTTPS**: Always use HTTPS for .exe downloads
4. **Verification**: Consider adding checksum verification

## Alternative: Portable Version

If users can't download .exe, you can:
1. Create a portable Python script
2. Users run it with Python installed
3. Same functionality, but requires Python

## Next Steps

1. ✅ Build the .exe file
2. ✅ Host it on your server
3. ✅ Update form with .exe URL
4. ✅ Test the complete flow
5. ✅ Deploy to production

