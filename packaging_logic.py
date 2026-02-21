# -*- coding: utf-8 -*-
import os
import tempfile
import shutil
import zipfile
import xml.etree.ElementTree as ET
from qgis.core import (
    QgsProject,
    QgsVectorLayer,
    QgsRasterLayer,
    QgsVectorFileWriter,
    QgsMessageLog,
    Qgis
)
from qgis.PyQt.QtCore import QCoreApplication

class GeopackerLogic:
    def __init__(self, output_file, strip_duplicates=True, strip_empty=True, skip_remote=True, progress_bar=None, status_label=None):
        self.output_file = output_file
        self.strip_duplicates = strip_duplicates
        self.strip_empty = strip_empty
        self.skip_remote = skip_remote
        self.progress_bar = progress_bar
        self.status_label = status_label
        self.project = QgsProject.instance()

    def update_status(self, message, progress=None):
        if self.status_label:
            self.status_label.setText(message)
        if self.progress_bar and progress is not None:
            self.progress_bar.setValue(progress)
        QgsMessageLog.logMessage(message, "Geopacker", Qgis.Info)
        # Keep UI responsive during long operations
        QCoreApplication.processEvents()

    def is_layer_empty_temp(self, layer):
        if not layer.isValid():
            return True
        if layer.type() == QgsVectorLayer.VectorLayer:
            if layer.dataProvider().name() == 'memory':
                if layer.featureCount() <= 0:
                    return True
        return False

    def run(self):
        self.update_status("Starting packaging...", 0)
        
        temp_dir = tempfile.mkdtemp(prefix="geopacker_")
        rasters_dir = os.path.join(temp_dir, "rasters")
        os.makedirs(rasters_dir, exist_ok=True)
        media_dir = os.path.join(temp_dir, "media")
        os.makedirs(media_dir, exist_ok=True)
        gpkg_path = os.path.join(temp_dir, "packaged_data.gpkg")
        
        try:
            layers = self.project.mapLayers().values()
            total_layers = len(layers)
            if total_layers == 0:
                self.update_status("No layers in project to package.", 100)
                return

            seen_sources = set()
            layers_to_package = []
            layers_to_remove = []
            
            self.update_status("Filtering layers...", 5)
            for layer in layers:
                if self.strip_empty and self.is_layer_empty_temp(layer):
                    self.update_status(f"Skipping empty temporary layer: {layer.name()}")
                    layers_to_remove.append(layer.id())
                    continue
                
                source = layer.publicSource()
                if self.strip_duplicates:
                    if source in seen_sources:
                        self.update_status(f"Skipping duplicate layer: {layer.name()}")
                        layers_to_remove.append(layer.id())
                        continue
                    seen_sources.add(source)
                
                layers_to_package.append(layer)

            layer_mapping = {}  
            used_layer_names = set()
            failed_layers = []
            
            for i, layer in enumerate(layers_to_package):
                progress = 5 + int(60 * (i / len(layers_to_package)))
                self.update_status(f"Processing layer: {layer.name()}", progress)
                
                if layer.type() == QgsVectorLayer.VectorLayer:
                    provider_name = layer.dataProvider().name() if layer.dataProvider() else ""
                    if self.skip_remote and provider_name not in ('ogr', 'memory', 'delimitedtext', 'gpx', 'spatialite'):
                        self.update_status(f"Skipping remote vector layer: {layer.name()} ({provider_name})")
                        failed_layers.append(f"• {layer.name()} (Skipped: remote/online provider '{provider_name}')")
                        continue

                    options = QgsVectorFileWriter.SaveVectorOptions()
                    options.driverName = "GPKG"
                    
                    base_safe_name = "".join([c if c.isalnum() else "_" for c in layer.name()])
                    safe_name = base_safe_name
                    suffix = 1
                    while safe_name in used_layer_names:
                        safe_name = f"{base_safe_name}_{suffix}"
                        suffix += 1
                    
                    used_layer_names.add(safe_name)
                    options.layerName = safe_name
                    
                    options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteFile
                    
                    if os.path.exists(gpkg_path):
                        options.actionOnExistingFile = QgsVectorFileWriter.CreateOrOverwriteLayer
                    
                    write_result = QgsVectorFileWriter.writeAsVectorFormatV3(
                        layer, gpkg_path, self.project.transformContext(), options)
                        
                    writer_err = write_result[0]
                    error_msg = write_result[1] if len(write_result) > 1 else str(writer_err)
                        
                    if writer_err == QgsVectorFileWriter.NoError:
                        new_source = f"./packaged_data.gpkg|layername={options.layerName}"
                        layer_mapping[layer.id()] = {
                            'type': 'vector',
                            'source': new_source,
                            'provider': 'ogr'
                        }
                    else:
                        QgsMessageLog.logMessage(f"Failed to export {layer.name()}: {error_msg}", "Geopacker", Qgis.Warning)
                        failed_layers.append(f"• {layer.name()} (Failed export: {error_msg})")
                
                elif layer.type() == QgsRasterLayer.RasterLayer:
                    source_path = layer.dataProvider().dataSourceUri()
                    if os.path.isfile(source_path):
                        filename = os.path.basename(source_path)
                        source_dir = os.path.dirname(source_path)
                        base_name, _ = os.path.splitext(filename)
                        
                        if os.path.isdir(source_dir):
                            for f in os.listdir(source_dir):
                                if f == filename or f.startswith(base_name + '.') or f.startswith(filename + '.'):
                                    src_f = os.path.join(source_dir, f)
                                    if os.path.isfile(src_f):
                                        dst_f = os.path.join(rasters_dir, f)
                                        shutil.copy2(src_f, dst_f)
                                        
                        new_source = f"./rasters/{filename}"
                        layer_mapping[layer.id()] = {
                            'type': 'raster',
                            'source': new_source,
                            'provider': 'gdal'
                        }
                    else:
                        QgsMessageLog.logMessage(f"Skipping raster copy for {layer.name()} (not a local file)", "Geopacker", Qgis.Info)

            self.update_status("Saving project copy...", 70)
            
            temp_qgz_path = os.path.join(temp_dir, "project.qgz")
            self.project.write(temp_qgz_path)
            
            self.update_status("Remapping project paths...", 75)
            
            qgz_extract_dir = os.path.join(temp_dir, "qgz_unpacked")
            os.makedirs(qgz_extract_dir, exist_ok=True)
            
            with zipfile.ZipFile(temp_qgz_path, 'r') as zf:
                zf.extractall(qgz_extract_dir)
                
            qgs_file = None
            for file in os.listdir(qgz_extract_dir):
                if file.endswith('.qgs'):
                    qgs_file = os.path.join(qgz_extract_dir, file)
                    break
                    
            if qgs_file:
                tree = ET.parse(qgs_file)
                root = tree.getroot()
                
                # --- Media Packaging Logic ---
                media_mapping = {}
                def process_media_path(path_str):
                    if not path_str or not isinstance(path_str, str):
                        return path_str
                    if os.path.isabs(path_str) and os.path.isfile(path_str):
                        if path_str not in media_mapping:
                            filename = os.path.basename(path_str)
                            safe_name = filename
                            suffix = 1
                            dest_path = os.path.join(media_dir, safe_name)
                            while os.path.exists(dest_path):
                                base, ext = os.path.splitext(filename)
                                safe_name = f"{base}_{suffix}{ext}"
                                dest_path = os.path.join(media_dir, safe_name)
                                suffix += 1
                            try:
                                shutil.copy2(path_str, dest_path)
                                media_mapping[path_str] = f"./media/{safe_name}"
                            except Exception as e:
                                QgsMessageLog.logMessage(f"Failed to copy media {path_str}: {str(e)}", "Geopacker", Qgis.Warning)
                                return path_str
                        return media_mapping[path_str]
                    return path_str

                def remap_assets_in_element(element):
                    changed = False
                    if element.tag == 'prop' and element.get('k') in ('name', 'svgFile', 'file'):
                        v = element.get('v')
                        if v:
                            new_path = process_media_path(v)
                            if new_path != v:
                                element.set('v', new_path)
                                changed = True
                    if element.tag == 'Option' and element.get('type') == 'QString':
                        name = element.get('name')
                        if name in ('pictureUrl', 'file', 'svgFile', 'path', 'sourceFile'):
                            v = element.get('value')
                            if v:
                                new_path = process_media_path(v)
                                if new_path != v:
                                    element.set('value', new_path)
                                    changed = True
                    for child in list(element):
                        if remap_assets_in_element(child):
                            changed = True
                    return changed
                
                remap_assets_in_element(root)
                # -----------------------------
                
                project_layers = root.find('projectlayers')
                layer_tree = root.find('layer-tree-group')
                
                if project_layers is not None:
                    for maplayer in list(project_layers):
                        layer_id_elem = maplayer.find('id')
                        if layer_id_elem is not None:
                            lid = layer_id_elem.text
                            if lid in layers_to_remove:
                                project_layers.remove(maplayer)
                                continue
                                
                            if lid in layer_mapping:
                                ds_elem = maplayer.find('datasource')
                                if ds_elem is not None:
                                    ds_elem.text = layer_mapping[lid]['source']
                                
                                provider_elem = maplayer.find('provider')
                                if provider_elem is not None:
                                    provider_elem.text = layer_mapping[lid]['provider']
                
                def remove_from_layer_tree(group):
                    for child in list(group):
                        if child.tag == 'layer-tree-layer':
                            lid = child.get('id')
                            if lid in layers_to_remove:
                                group.remove(child)
                        elif child.tag == 'layer-tree-group':
                            remove_from_layer_tree(child)
                
                if layer_tree is not None:
                    remove_from_layer_tree(layer_tree)
                    
                paths_elem = root.find('properties/Paths/Absolute')
                if paths_elem is not None:
                    paths_elem.text = 'false'
                
                tree.write(qgs_file, encoding='utf-8', xml_declaration=True)
                
                new_qgz_path = os.path.join(temp_dir, "project_remapped.qgz")
                with zipfile.ZipFile(new_qgz_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                    for root_dir, dirs, files in os.walk(qgz_extract_dir):
                        for file in files:
                            file_path = os.path.join(root_dir, file)
                            arcname = os.path.relpath(file_path, qgz_extract_dir)
                            zf.write(file_path, arcname)
                
                shutil.move(new_qgz_path, temp_qgz_path)
                shutil.rmtree(qgz_extract_dir, ignore_errors=True)

            self.update_status("Zipping final package...", 85)
            
            output_basename = os.path.basename(self.output_file)
            project_name, _ = os.path.splitext(output_basename)
            qgz_name_in_zip = f"{project_name}.qgz"
            
            with zipfile.ZipFile(self.output_file, 'w', zipfile.ZIP_DEFLATED) as final_zip:
                final_zip.write(temp_qgz_path, qgz_name_in_zip)
                
                if os.path.exists(gpkg_path):
                    final_zip.write(gpkg_path, "packaged_data.gpkg")
                
                for root_dir, dirs, files in os.walk(rasters_dir):
                    for file in files:
                        file_path = os.path.join(root_dir, file)
                        rel_path = os.path.relpath(file_path, temp_dir)
                        final_zip.write(file_path, rel_path)

                if os.path.exists(media_dir):
                    for root_dir, dirs, files in os.walk(media_dir):
                        for file in files:
                            file_path = os.path.join(root_dir, file)
                            rel_path = os.path.relpath(file_path, temp_dir)
                            final_zip.write(file_path, rel_path)

            self.update_status("Packaging complete!", 100)
            return failed_layers
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)
