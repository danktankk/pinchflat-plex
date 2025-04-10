![Pinchflat Logo](images/logo.png)

# Pinchflat Plex Integration

> ⚠️ **Important!**  
> This integration was made possible thanks to the original work by [TubeArchivist Plex](https://github.com/tubearchivist/tubearchivist-plex).
> This README is pulled directly from that GitHub page and changed to reflect how to use with Pinchflat.  
>  
> 🔗 https://github.com/tubearchivist/tubearchivist-plex

This is a custom set of **Scanner** and **Agent** modules to integrate **Pinchflat** with Plex.  

> ⚠️ **Important!**  
> Use this at your own risk. It is an alpha release and should be treated as such.
> I made this integration for myself only. I will likely not be providing much support for it.

---

## 🚫 Limitations

- This integration requires both the custom **Scanner** and **Agent** to be installed and active in Plex.
- It is built for integration with a **single Pinchflat instance**. TRhere is no Multi-instance support.
- **Pinchflat must be online and accessible** during Plex filesystem scans and metadata refreshes.
- If Plex cannot reach Pinchflat, metadata updates may **fail or be skipped**.
- This is an **early build**. Some features may be missing or buggy.
- **Playlist integration is planned** but not implemented yet.
- Not all Plex-supported metadata is currently provided — **future releases will expand** support.

---

## 🛠️ Installation Steps

### Locate Plex Media Server Directory

The Plex Media Server root directory varies by platform. Examples:

```
$PLEX_HOME/Library/Application Support/Plex Media Server/                # Linux  
/mnt/user/appdata/plex/Library/Application Support/Plex Media Server    # Unraid  
%LOCALAPPDATA%\Plex Media Server\                                       # Windows Vista/7/8  
/volume1/Plex/Library/Application Support/Plex Media Server/            # Synology  
/usr/local/plexdata/Plex Media Server/                                  # FreeBSD  
$HOME/Library/Application Support/Plex Media Server/                    # macOS  
```

Use the appropriate directory path for your setup.

---

### First-Time Setup

1. Ensure **Plex can access the Pinchflat media directory**.
2. Make sure the system running Plex can communicate with Pinchflat.
3. If using a **non-standard port** (e.g., `8000`), include it in all `pf_url` configurations.

---

### Download and Prepare Files

1. [Download the ZIP file](https://github.com/tubearchivist/tubearchivist-plex/archive/refs/heads/main.zip)
2. Extract the archive.
3. Rename the unpacked directory to: `Pinchflat-Agent.bundle`

---

### Scanner Installation

> 📁 Note: If `Scanners` and `Series` directories do not exist, create them.

1. Move the `Scanners` directory from `Pinchflat-Agent.bundle` into your **Plex Media Server directory**.
2. Navigate to `Scanners/Series` and copy:
   - `sample-pf_config.json` → `pf_config.json`
3. Edit `pf_config.json`:
   - Set your **Pinchflat URL** (including port if needed)
4. Ensure the **Python script and config file** are owned and readable by the **Plex user**.
5. **Restart Plex**.

---

### Agent Installation

1. If `Scanners` directory is still inside `Pinchflat-Agent.bundle`, remove it.
2. Move `Pinchflat-Agent.bundle` into the `Plug-ins` directory in the **Plex Media Server** path.
3. Fix **ownership and permissions** so that the **Plex user** can access it.
4. **Restart Plex**.

---

## 📚 Library Integration

1. In Plex, create or edit a library.
2. On the **General tab**, choose `TV Shows`.
3. On the **Add Folders tab**, point to the **Pinchflat media parent directory**.
4. On the **Advanced tab**, configure:
   - **Scanner**: `Pinchflat Scanner`
   - **Agent**: `Pinchflat Agent`
   - **Pinchflat URL** (including port if needed)

After setup:

- The scanner should **auto-detect media**.
- You can manually run **Scan Library Files**.
- Metadata should update automatically, or you can manually run **Refresh Metadata**.

---

## 🧩 Troubleshooting

- **Can't see scanner/agent?** Check file paths and permissions.
- **Media not showing?** Check the Scanner logs.
- **Metadata issues?** Check the Agent logs.

---

## 📄 Log Locations

- **Scanner Logs**:  
  `Plex Media Server/Logs/Pinchflat Scanner/_root_.scanner.log`

- **Agent Logs**:  
  `Plex Media Server/Logs/PMS Plugin Logs/com.plexapp.agents.pinchflat_agent.log`

---

## 💬 Need Help?

Dont we all............
