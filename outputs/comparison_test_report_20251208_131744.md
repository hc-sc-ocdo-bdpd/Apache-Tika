# Apache Tika vs OCDO File Processing - Test Results

**Test Date:** 2025-12-08T13:17:35.351197

## Summary

| Library | Wins | Percentage |
|---------|------|------------|
| Apache Tika | 8 | 100.0% |
| OCDO File Processing | 0 | 0.0% |
| Ties | 0 | 0.0% |

## Test Results

### Basic Text Extraction

**Winner:** Tika

**Details:**
```json
{
  "tika": {
    "accuracy": 100.0,
    "time": 7.513088941574097,
    "success": true
  },
  "ocdo": {
    "accuracy": 0.0,
    "time": 0.03437209129333496,
    "success": false
  }
}
```

### Metadata Extraction

**Winner:** Tika

**Details:**
```json
{
  "tika": {
    "metadata_count": 11,
    "success": true
  },
  "ocdo": {
    "metadata_count": 6,
    "success": true
  }
}
```

### Special Character Handling

**Winner:** Tika

**Details:**
```json
{
  "tika": {
    "accuracy": 100.0,
    "success": true
  },
  "ocdo": {
    "accuracy": 0.0,
    "success": false
  }
}
```

### Processing Speed

**Winner:** Tika

**Details:**
```json
{
  "tika": {
    "avg_time": 0.0465998649597168
  },
  "ocdo": {
    "avg_time": 999.0
  }
}
```

### Empty File Handling

**Winner:** Tika

**Details:**
```json
{
  "tika": {
    "handled": true
  },
  "ocdo": {
    "handled": false
  }
}
```

### Whitespace Preservation

**Winner:** Tika

**Details:**
```json
{
  "tika": {
    "line_count": 7,
    "success": true
  },
  "ocdo": {
    "line_count": 0,
    "success": false
  }
}
```

### Numeric Data Accuracy

**Winner:** Tika

**Details:**
```json
{
  "tika": {
    "accuracy": 100.0,
    "success": true
  },
  "ocdo": {
    "accuracy": 0.0,
    "success": false
  }
}
```

### Large File Handling

**Winner:** Tika

**Details:**
```json
{
  "tika": {
    "success": true,
    "time": 0.11060619354248047
  },
  "ocdo": {
    "success": false,
    "time": null
  }
}
```

