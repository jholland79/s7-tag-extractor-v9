# s7-tag-extractor

## Overview

Python CLI tool to extract tags from Siemens Step 7 projects and export them in formats suitable for OSI Pi (PI Builder Excel) and optionally Kepware.

## Success Criteria

- [ ] Parse .s7p project files and navigate the DBF structure
- [ ] Extract symbol table (names, addresses, comments, types)
- [ ] Extract data block tags including array expansion
- [ ] Export to PI Builder Excel format with correct columns
- [ ] Handle BOOL → Int16 with Location2=2 mapping
- [ ] Include InstrumentTag with S7 absolute address

## Architecture

### Step 7 Project Structure (Key Files)

```
project/
├── *.s7p                    # Project file (entry point)
├── S7RESOFF.DBF            # Program folders index
├── YLNKLIST.DBF            # Links between objects
├── YDBs/
│   └── xxxx/
│       └── SYMLIST.DBF     # Symbol table (_SKZ, _OPHIST, _COMMENT)
└── ombstx/offline/xxxx/
    ├── SUBBLK.DBF          # Sub-block data
    └── BAUSTEIN.DBF        # Block data (FBs, FCs, DBs)
```

### Parsing Strategy

1. Use `dbfread` Python library to parse dBase (DBF) files
2. Navigate the project structure via S7RESOFF.DBF → YLNKLIST.DBF → SYMLIST.DBF
3. Extract symbol table: name (_SKZ), address (_OPHIST), comment (_COMMENT)
4. Parse data blocks to get array dimensions and expand to individual elements

### PI Builder Export Format

Excel spreadsheet with columns:

| Tag | PointType | PointSource | Descriptor | EngUnits | InstrumentTag | Location2 |
|-----|-----------|-------------|------------|----------|---------------|-----------|
| Tank1_Level | Float32 | S7 | Tank 1 Level | m | DB100.DBD0 | |
| Motor1_Run | Int16 | S7 | Motor 1 Running | | DB100.DBX4.0 | 2 |

### Type Mapping (S7 → PI)

- BOOL → Int16 (with Location2=2)
- INT → Int16
- DINT → Int32
- REAL → Float32
- WORD → Int16
- DWORD → Int32

**InstrumentTag:** Contains the S7 absolute address (e.g., DB100.DBD0, M0.0, I0.0)

## Implementation Tasks

### Phase 1: Project Foundation & Test Data

- [ ] Task 1.1: Download sample Step 7 project
  - Files: tests/fixtures/sample_project/
  - Tests: tests/test_fixtures.py
  - Acceptance: Sample S7 project from snap7 repo is available with SYMLIST.DBF
  - Source: <https://github.com/SCADACS/snap7/tree/master/examples/Step%207/Snap7>

- [ ] Task 1.2: Implement data models
  - Files: src/s7_tag_extractor/models.py
  - Tests: tests/test_models.py
  - Acceptance: Tag, Symbol, DataBlock dataclasses with validation

### Phase 2: DBF Parsing

- [ ] Task 2.1: Project structure navigation
  - Files: src/s7_tag_extractor/parser/project.py
  - Tests: tests/test_project_parser.py
  - Acceptance: Given .s7p path, find all SYMLIST.DBF, BAUSTEIN.DBF files

- [ ] Task 2.2: Symbol table parsing (SYMLIST.DBF)
  - Files: src/s7_tag_extractor/parser/symbols.py
  - Tests: tests/test_symbols_parser.py
  - Acceptance: Extract _SKZ (name),_OPHIST (address), _COMMENT from SYMLIST.DBF

- [ ] Task 2.3: Data block parsing (BAUSTEIN.DBF)
  - Files: src/s7_tag_extractor/parser/blocks.py
  - Tests: tests/test_blocks_parser.py
  - Acceptance: Parse DB definitions, detect arrays, extract element types

### Phase 3: Array Expansion

- [ ] Task 3.1: Array detection and expansion
  - Files: src/s7_tag_extractor/parser/arrays.py
  - Tests: tests/test_array_expansion.py
  - Acceptance: Array[0..9] of INT → 10 individual tags with correct addresses

### Phase 4: PI Builder Export

- [ ] Task 4.1: S7 to PI type mapping
  - Files: src/s7_tag_extractor/exporters/type_mapping.py
  - Tests: tests/test_type_mapping.py
  - Acceptance: BOOL→Int16+Location2=2, INT→Int16, REAL→Float32, etc.

- [ ] Task 4.2: Excel export with PI Builder columns
  - Files: src/s7_tag_extractor/exporters/pi_builder.py
  - Tests: tests/test_pi_builder_export.py
  - Acceptance: Excel with Tag, PointType, PointSource, Descriptor, InstrumentTag, Location2

### Phase 5: CLI Interface

- [ ] Task 5.1: CLI with Click
  - Files: src/s7_tag_extractor/cli.py
  - Tests: tests/test_cli.py
  - Acceptance: `s7-tag-extractor export <project.s7p> --format pi-builder -o out.xlsx`

### Phase 6: Kepware Export (Optional)

- [ ] Task 6.1: Kepware CSV export
  - Files: src/s7_tag_extractor/exporters/kepware.py
  - Tests: tests/test_kepware_export.py
  - Acceptance: CSV with Kepware Siemens driver compatible columns

## API/Interface Design

```bash
# List tags from project
s7-tag-extractor list <project.s7p>
s7-tag-extractor list <project.s7p> --filter "Motor*"

# Export to PI Builder format
s7-tag-extractor export <project.s7p> --format pi-builder -o tags.xlsx

# Export to Kepware format
s7-tag-extractor export <project.s7p> --format kepware -o tags.csv

# Show project structure info
s7-tag-extractor info <project.s7p>
```

## Error Handling Strategy

1. **File not found**: Clear error message with path that was tried
2. **Invalid S7 project**: Check for .s7p file and required DBF files exist
3. **DBF parse errors**: Log problematic record, continue with others, report count at end
4. **Unknown data types**: Log warning, skip tag, include in summary
5. **Character encoding**: Try Windows-1252, fall back to latin-1, log if issues

All errors should be logged with context (file, record number) for debugging.

## Notes for Agent

### Dependencies

```
dbfread>=2.0.7    # Parse dBase DBF files
click>=8.0        # CLI framework
openpyxl>=3.0     # Excel export
```

### DBF Column Names

- SYMLIST.DBF: `_SKZ` (name), `_OPHIST` (address), `_COMMENT` (comment)
- The columns have underscore prefix in Step 7 DBF files

### PI Builder Excel Columns

Must include: Tag, PointType, PointSource, Descriptor, EngUnits, InstrumentTag, Location2

- Location2=2 is required for BOOL tags (mapped to Int16)

### Testing Strategy

1. Use real DBF files from snap7 sample for integration tests
2. Create minimal mock DBF data for unit tests
3. Verify Excel output can be opened and has correct structure

### Project Structure

```
s7-tag-extractor/
├── pyproject.toml
├── src/
│   └── s7_tag_extractor/
│       ├── __init__.py
│       ├── cli.py
│       ├── models.py
│       ├── parser/
│       │   ├── __init__.py
│       │   ├── project.py
│       │   ├── symbols.py
│       │   ├── blocks.py
│       │   └── arrays.py
│       └── exporters/
│           ├── __init__.py
│           ├── type_mapping.py
│           ├── pi_builder.py
│           └── kepware.py
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_project_parser.py
    ├── test_symbols_parser.py
    ├── test_blocks_parser.py
    ├── test_array_expansion.py
    ├── test_type_mapping.py
    ├── test_pi_builder_export.py
    ├── test_cli.py
    └── fixtures/
        └── sample_project/
```
