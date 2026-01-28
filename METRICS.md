# Metrics & Methodology

This document defines the key metrics, classifications, and data transformations used in this analysis.

## Key Performance Indicators

| Metric | Formula | Purpose |
|--------|---------|---------|
| Total Incidents | `COUNT(*)` | Volume of recorded events |
| Total Casualties | `SUM(Number Killed + Number Wounded)` | Aggregate human impact |
| Total Killed | `SUM(Number Killed)` | Fatality count |
| Total Wounded | `SUM(Number Wounded)` | Injury count |
| Fatal Rate | `COUNT(Incidents with deaths) / COUNT(*)` | Proportion resulting in fatalities |
| Mass Casualty Rate | `COUNT(Incidents ≥4 casualties) / COUNT(*)` | High-impact event frequency |
| States Affected | `COUNT(DISTINCT State)` | Geographic spread |
| Schools Affected | `COUNT(DISTINCT School name)` | Institutional impact |

## Severity Classification

Incidents are classified into five severity levels based on casualty counts:

| Severity Level | Criteria | Rationale |
|----------------|----------|-----------|
| No Casualties | 0 killed, 0 wounded | Firearm discharged but no injuries |
| Injuries Only | >0 wounded, 0 killed | Non-fatal injuries |
| Single Fatality | 1 killed, 0 wounded | Single death, no additional injuries |
| Multiple Casualties | 2-3 total casualties | Multiple victims below mass threshold |
| Mass Casualty | ≥4 total casualties | Aligns with FBI mass shooting definition |

## Derived Fields

| Field | Calculation | Purpose |
|-------|-------------|---------|
| Academic Year | If month < 8: `{year-1}-{year}`, else `{year}-{year+1}` | Groups incidents by school calendar (Aug-Jul cycle) |
| Days Since Incident | `TODAY() - Incident Date` | Recency measure |
| Days Since Previous | Time between consecutive incidents per state | Frequency pattern analysis |
| Is Fatal | `Number Killed > 0` | Binary fatality flag |
| Mass Casualty | `Total Casualties >= 4` | Binary high-impact flag |

## Data Quality Measures

### Deduplication
Records are deduplicated using a composite key: `[Incident Date, City, State, School name]`

This prevents double-counting when the same incident appears in multiple source records.

### Completeness Score
```
Completeness = (1 - (missing_dates + missing_coords + missing_narratives) / (total_rows × 3)) × 100
```

Tracks data quality across three critical fields: date, location coordinates, and narrative description.

### Data Freshness
`Days since most recent incident` - indicates how current the dataset is.

## Assumptions & Limitations

1. **Current year data is partial** - Statistics for the current calendar year will increase throughout the year. The dashboard displays a warning when viewing current-year data.

2. **Geographic precision** - Coordinates represent school locations, not necessarily exact incident locations on campus.

3. **Deduplication limitations** - The composite key may not catch all duplicates if source data has minor variations in school names or dates.

4. **Incident scope** - Data includes incidents where a firearm was brandished, fired, or a bullet hit school property for K-12 and higher education institutions.

## Data Source

**Everytown Research** - [Gunfire on School Grounds](https://everytownresearch.org/maps/gunfire-on-school-grounds/)

Data is continuously updated as new incidents are reported and verified by Everytown's research team.
