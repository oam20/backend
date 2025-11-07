# Quick Start: .exe File Solution

## What This Does

1. User submits form → .exe file downloads automatically
2. User runs .exe → Popup window appears (like System Requirements Lab)
3. System collects data → All Windows system details collected
4. Data sent to API → Complete system details saved to database

## Quick Setup (3 Steps)

### Step 1: Build the .exe File

**Windows:**
```bash
build_exe.bat
```

**Or manually:**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name=SystemCollector --add-data="get_system_details.py;." --hidden-import=requests --hidden-import=psutil --hidden-import=tkinter system_collector_gui.py
```

The .exe file will be in `dist/SystemCollector.exe`

### Step 2: Host the .exe File

Upload `dist/SystemCollector.exe` to your web server and get the URL.

**Options:**
- Your web server (e.g., `https://yoursite.com/SystemCollector.exe`)
- GitHub Releases
- Cloud storage (Google Drive, Dropbox, etc.)
- CDN

### Step 3: Update the Form

Open `form-example.html` and update line ~220:

```javascript
const exeUrl = 'https://yoursite.com/SystemCollector.exe'; // Update this!
```

## How It Works

### User Experience:

1. **User fills form** → Employee ID, Email, Department
2. **Clicks Submit** → Form validates
3. **.exe downloads** → `SystemCollector.exe` downloads automatically
4. **User runs .exe** → Popup window appears
5. **System collects** → Shows "Taking a Look..." with progress
6. **Data sent** → Automatically sends to your API
7. **Success** → Window closes with success message

### What Gets Collected:

✅ **Complete Windows System Details:**
- Username
- Hostname
- System Manufacturer (hardware)
- System Model (hardware)
- Serial Number
- IP Address
- OS Information
- Storage Details (all drives)
- RAM Details
- And more!

## Testing

1. Build the .exe:
   ```bash
   build_exe.bat
   ```

2. Test locally:
   ```bash
   dist\SystemCollector.exe
   ```

3. Test with parameters:
   ```bash
   dist\SystemCollector.exe "EMP001,user@example.com,IT,https://backend-blue-beta.vercel.app"
   ```

4. Test the form:
   - Open `form-example.html`
   - Fill in the form
   - Submit
   - .exe should download
   - Run the .exe
   - Verify data is collected and sent

## Files Created

- ✅ `system_collector_gui.py` - GUI application (System Requirements Lab style)
- ✅ `build_exe.bat` - Windows build script
- ✅ `build_exe.py` - Python build script
- ✅ `form-example.html` - Updated form with .exe download
- ✅ `EXE_DEPLOYMENT.md` - Detailed deployment guide

## Customization

### Change Window Title
Edit `system_collector_gui.py` line ~40:
```python
self.root.title("Your Custom Title")
```

### Change Version Number
Edit `system_collector_gui.py` line ~180:
```python
version_label = tk.Label(..., text="v 1.0.0", ...)
```

### Add Icon
1. Create an `.ico` file
2. Update build command:
   ```bash
   pyinstaller --icon=icon.ico ...
   ```

## Troubleshooting

### .exe doesn't download
- Check the URL in `form-example.html` is correct
- Verify the .exe file is accessible via the URL
- Check browser download settings

### .exe doesn't run
- Check Windows Defender/Antivirus (may block unsigned .exe)
- Right-click → Properties → Unblock (if blocked)
- Test on a clean Windows machine

### Data not sending
- Check API URL in `system_collector_gui.py` (line ~20)
- Verify internet connection
- Check firewall settings
- Verify API endpoint is accessible

### GUI doesn't appear
- Check if tkinter is installed
- Try running from command line to see errors
- Check Windows has required libraries

## Next Steps

1. ✅ Build the .exe file
2. ✅ Host it on your server
3. ✅ Update form with .exe URL
4. ✅ Test the complete flow
5. ✅ Deploy to production

## Support

For detailed instructions, see:
- `EXE_DEPLOYMENT.md` - Complete deployment guide
- `README.md` - General documentation

