"""DBF file format constants shared across parsers."""

# DBF header structure offsets
DBF_HEADER_SIZE = 32
NUM_RECORDS_OFFSET = 4
HEADER_LENGTH_OFFSET = 8
RECORD_LENGTH_OFFSET = 10

# Delete marker
DELETED_RECORD_MARKER = ord("*")
