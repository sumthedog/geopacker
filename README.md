<p align="center">
  <img src="icon.png" width="128" height="128" alt="Geopacker Logo">
</p>

# Geopacker QGIS Plugin

**Geopacker** is a QGIS plugin designed to solve the headache of broken paths when sharing QGIS projects. It bundles your entire current project (`.qgz`), vector layers, and raster layers into a single, clean `.zip` file ready to be shared. 

Unlike the native "Package Layers" tool, Geopacker actually modifies the bundled `.qgz` project to use relative paths, ensuring that whoever opens your packaged zip file will see exactly what you see, without a single broken link warning.

## Why Geopacker? (The Problem Solved)

Sharing QGIS projects often results in broken file paths because standard tools simply export data without updating the project file's references. Geopacker bridges this gap.

| Feature | QGIS "Package Layers" | Geopacker |
| --- | --- | --- |
| **Project Path Linking** | ❌ Leaves `.qgz` untouched (links break upon sharing). | ✅ Safely rewrites `.qgz` XML to use perfect **relative paths**. |
| **Raster Data Support** | ❌ Ignores raster files entirely. | ✅ Automatically copies and links local **rasters** safely. |
| **Duplicate Checking** | ❌ Blindly processes duplicates, inflating file size. | ✅ Actively detects and **strips duplicate** layer sources. |
| **Empty Layers** | ❌ Packages empty workspace/scratch layers. | ✅ Automatically **trims out empty** memory layers. |
| **Final Output** | ❌ Yields a loose, unmanaged GeoPackage file. | ✅ Generates a **single, email-ready `.zip`** archive. |

## Features
- **Consolidates Vectors**: Exports all valid shapefiles, GeoJSONs, etc. into a single `packaged_data.gpkg`.
- **Collects Rasters**: Copies local rasters (like GeoTIFFs) into a unified `rasters/` directory.
- **Path Remapping**: Behind the scenes, the plugin unzips a copy of your `.qgz` project, parses the underlying XML, and safely updates the layer data sources to point to the new relatively-pathed GeoPackage and rasters.
- **Smart Trimming**: Optional checkboxes to strip out empty memory layers and duplicate layer sources to keep your packaged file size down.

## Installation
1. Download a Geopacker ZIP release from this repository.
2. In QGIS, navigate to **Plugins** > **Manage and Install Plugins...**
3. Select **Install from ZIP**, choose the downloaded file, and click Install.
4. The Geopacker icon will appear in your Plugins toolbar.

## Usage
1. Open your target mapping project in QGIS.
2. Click the Geopacker icon or find it under the **Plugins** > **Geopacker** menu.
3. Choose the destination path for your packaged `.zip` file.
4. Check the options to remove duplicates or empty temporary layers if desired.
5. Click **Run**.
6. Share the resulting `.zip` file with your colleagues or clients!

## Requirements
- QGIS 3.0 or higher.
- Python 3 environment (native to QGIS installations).

## Contributing and Bug Reports
Please report any bugs or feature requests on the [GitHub Issues tracker](https://github.com/rick2x/geopacker/issues).
