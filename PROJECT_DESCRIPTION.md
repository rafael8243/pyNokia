# NOKIA Parser II - Project Description

## Overview
**pyNokia** is a Python-based XML parser and data processor designed to read Nokia network configuration dumps (XML format) and export structured data to Excel spreadsheets. The application provides a GUI interface for file selection and processing, with support for both default and complete data extraction modes.

## Purpose
This tool automates the extraction of managed objects (MO) and their parameters from Nokia telecom equipment configuration files, converting complex XML hierarchies into organized CSV files that are then merged into Excel workbooks for analysis and reporting.

---

## Project Structure

```
pyNokia/
├── pynokia.py              # Main application entry point (GUI & orchestration)
├── base/
│   ├── config.py           # Configuration module (currently minimal)
│   ├── mergecsv.py         # CSV merging utilities
│   ├── nok_etreader.py     # XML parsing engine (core logic)
│   ├── comments.txt        # Documentation/notes
│   └── __pycache__/        # Compiled Python files (auto-generated)
└── PROJECT_DESCRIPTION.md  # This file
```

---

## Key Components

### 1. **pynokia.py** - Main Application
**Responsibility**: GUI interface and workflow orchestration

**Features:**
- Tkinter-based graphical user interface with file selection dialog
- Two extraction modes: Default (predefined object types) and Complete (all objects)
- Real-time progress display in scrolled text widget
- Threading for non-blocking file processing
- Performance timing measurements

**Key Classes:**
- `App(Tk)`: Main application window inheriting from Tkinter root

**Key Methods:**
- `select_file()`: File dialog and validation
- `read_file()`: Main processing orchestrator (runs in background thread)
- `check_file()`: Validates selected XML files exist
- `threading_read()`: Manages background processing thread
- `print_box()`: Thread-safe message display (note: currently NOT thread-safe)

---

### 2. **nok_etreader.py** - XML Parser
**Responsibility**: Core XML parsing using event-driven SAX-like parsing with lxml

**Architecture:**
- Event-driven XML parsing with `lxml.etree.XMLParser` and custom target class
- `NokiaXML` class implements target interface with `start()`, `end()`, `data()` methods
- Hierarchical parameter tracking for managed objects and their attributes

**Key Data Structures:**
- `all_mo`: Dictionary of all managed objects grouped by class
- `all_p`: Dictionary tracking all parameters used per managed object class
- `this_mo`: Current managed object being processed
- `this_item`: Current list item being processed

**Supported Object Types:**
Processes objects like: LNCEL, LNCEL_FDD, LNBTS, WCEL, BTS, RNC, TRX, ADCE, ADJL, and 30+ more

**Features:**
- Extracts DN (Distinguished Name) and hierarchical attributes
- Handles nested lists and items within parameters
- Supports both full export and filtered mini-exports with predefined parameters
- Generates report file listing exported vs. ignored elements

---

### 3. **mergecsv.py** - CSV Merge Utility
**Responsibility**: Convert multiple CSV files into an Excel workbook

**Function:**
- `ext_MergeCSV(origem, destino)`: Reads CSV files and writes to Excel sheets

**Process:**
1. Discovers all CSV files in source directory
2. Reads each CSV with `|` delimiter (pipe-separated)
3. Creates separate Excel sheet for each CSV
4. Writes to destination Excel file

---

### 4. **config.py** - Configuration Module
**Current Status**: Placeholder with imports only

**Intended Use**: Should contain:
- Configuration constants and parameters
- Encoding defaults
- Export filtering rules
- File paths and temporary directory settings

---

## Data Flow

```
1. User selects XML file(s) via GUI
   ↓
2. pynokia.py validates file(s) exist
   ↓
3. Processing spawned in background thread
   ↓
4. nok_etreader.py parses XML and extracts managed objects
   ↓
5. CSV files generated in temporary directory
   ↓
6. mergecsv.py combines CSVs into Excel workbook
   ↓
7. Output Excel file saved to source directory
   ↓
8. Performance metrics and status displayed to user
```

---

## Workflow Modes

### **Default Mode**
Exports only predefined object types relevant to typical Nokia network analysis:
- Cell types: LNCEL, LNCEL_FDD, WCEL, WNCELG, NRCELL
- Base Station: LNBTS, WNBTS, BTS
- RAN Controllers: RNC, BSC
- Adjacencies: ADCE, ADJL, LNADJW, ADJI, ADJS, ADJD, ADJG, ADJL, ADJW
- Supporting objects: TRX, SIB, MOPR, LAPD, MAL, etc.
- ~34 predefined object types

### **Complete Mode**
Exports all managed objects found in the XML file, regardless of type.

---

## Processing Features

### **Parameter Extraction**
- Extracts all parameters (name-value pairs) from managed objects
- Dynamically discovers parameters across all instances
- Handles special characters in parameter values using `¬` separator for list items

### **Mini-Exports**
For key object types (BSC, RNC, BTS, etc.), generates additional CSV files with only essential parameters. Example for BTS:
- name, adminState, angle, btsIsHopping, cellId, gprsEnabled, etc.

### **Output Filename Generation**
- Removes Nokia dump identifiers (NOK3, NOK4, NOK5) from filename
- Auto-increments filename if file exists (avoids overwriting)
- Places output in same directory as source XML

### **Performance Metrics**
- Measures parsing time, merge time, and total time
- Displays timing breakdown in UI

---

## Dependencies

### **Required Libraries**
- `pandas`: CSV reading and Excel writing
- `lxml`: XML parsing (event-driven)
- `tkinter`: GUI (usually included with Python)
- **Standard Library**: `os`, `threading`, `tempfile`

### **Installation**
```bash
pip install pandas lxml
```

---

## Usage Instructions

### **Launch Application**
```bash
python pynokia.py
```

### **Using the GUI**
1. Click "Open XML" button
2. Select one or more Nokia XML dump files
3. Choose extraction mode: "Default" or "Complete"
4. Processing starts automatically after file selection
5. Monitor progress in the text output area
6. Look for "FINISHED" message with output file path

### **Output**
- Main Excel file: `<original_name>.xlsx` (or `<name> (1).xlsx`, `<name> (2).xlsx` if file exists)
- Location: Same directory as source XML file
- Contains one sheet per object type
- Each sheet has columns for: ID, DN, inherited attributes, and all extracted parameters

---

## Known Limitations & Issues

### **Critical**
- [ ] Thread safety: GUI updates from background thread can cause race conditions
- [ ] Cross-platform paths: Hardcoded `/` separators fail on Windows in some places
- [ ] Resource leaks: Excel writer not closed properly on exceptions

### **Important**
- Requires `iso-8859-1` encoding (not configurable, may fail with other encodings)
- No error recovery for malformed XML
- Sheet names not validated for Excel length/character limits
- High memory usage with very large XML files (entire DOM loaded)

### **Minor**
- TODO comments indicate incomplete features (line 151)
- Unused variable assignments (line 71)
- Configuration not actually used (config.py empty)
- Duplicate code between pynokia.py and mergecsv.py

---

## File Specifications

### **Input Format**
- **Type**: XML files
- **Source**: Nokia telecom equipment configuration dumps
- **Structure**: Managed objects with nested parameters and lists
- **Encoding**: ISO-8859-1 (assumed)
- **Typical Size**: 50 MB - 500 MB+

### **Output Format**
- **Type**: Excel workbook (.xlsx)
- **Sheets**: One per managed object type
- **Delimiter**: Pipe (`|`) in intermediate CSVs
- **Columns**: Dynamic, based on discovered parameters
- **Sorting**: Parameters alphabetically (after system columns)

---

## Configuration

### **Default Object Types (for Default Mode)**
Located in `nok_etreader.py` line ~115:
```python
default_list = ['LNCEL_FDD', 'LNBTS', 'LNCEL', 'IRFIM', 'SIB', 'LNMME', ...]
```

### **Mini-Export Parameters**
Located in `nok_etreader.py` line ~160 in `params_mini` dictionary:
```python
params_mini = {
    'BSC': ['name'],
    'RNC': ['name'],
    'BTS': ['nwName', 'adminState', ...],
    ...
}
```

### **GUI Constants**
Located in `pynokia.py` line ~13-15:
```python
APP_NAME = "NOKIA Parser II"
WIDTH = 550
HEIGHT = 600
```

---

## Performance Characteristics

| Operation | Typical Time | File Size |
|-----------|--------------|-----------|
| Parse & Extract | 10-30 seconds | 100 MB |
| Merge CSVs to Excel | 5-15 seconds | 100 MB |
| **Total** | **15-45 seconds** | **100 MB** |

*Actual times vary with number of object types and parameters*

---

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| No file selected | Dialog dismissed | Click "Open XML" again, select file(s) |
| File not found error | Path changed/file deleted | Verify file location, try again |
| Encoding error | File not ISO-8859-1 | Check source file encoding |
| Excel file locked | Another process using file | Close Excel, clear temp directory |
| GUI freezes | Background thread issue | Restart application |

---

## Future Enhancements

1. **Fix Critical Issues**
   - Implement thread-safe message queue for GUI updates
   - Use `os.path.join()` for all path operations
   - Add proper exception handling and cleanup

2. **Feature Improvements**
   - Configurable encoding detection
   - Support for other export formats (CSV, JSON, database)
   - Parameter filtering/selection in GUI
   - Batch processing multiple files
   - Progress bar instead of text updates

3. **Code Quality**
   - Add unit tests
   - Implement logging instead of print statements
   - Create proper configuration file system
   - Split MergeCSV into base module

4. **Performance**
   - Streaming XML parsing for memory efficiency
   - Parallel CSV processing
   - Incremental Excel generation

---

## Author Notes
- Application designed for Nokia network engineers analyzing network configurations
- Handles complex Nokia-specific XML structure with managed objects and parameters
- Temporary files stored in system temp directory (auto-cleaned on exit)
- Currently single-file output; multiple input files processed together into one workbook

---

## Version History
- **Current**: Initial release with GUI, dual-mode extraction, mini-exports
- **Planned**: Thread safety fixes, configuration system, enhanced error handling

