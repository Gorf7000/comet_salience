"""Configuration for the comet visibility pipeline.

All tunable parameters live here, per spec §15. Override at runtime by
mutating these module attributes before invoking the pipeline.
"""

from pathlib import Path

# ----------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[2]
DATA_RAW = ROOT / "data" / "raw" / "comet_sources"
DATA_INPUTS = ROOT / "data" / "inputs"
DATA_INTERMEDIATE = ROOT / "data" / "intermediate"
DATA_PROCESSED = ROOT / "data" / "processed"
HORIZONS_CACHE = DATA_INTERMEDIATE / "horizons_cache"
AERITH_CACHE = DATA_RAW / "aerith"
SBDB_CACHE = DATA_RAW / "sbdb"
FIGURES = ROOT / "figures" / "comet_visibility_diagnostics"
REPORTS = ROOT / "reports"

for p in (DATA_RAW, DATA_INPUTS, DATA_INTERMEDIATE, DATA_PROCESSED, HORIZONS_CACHE,
          AERITH_CACHE, SBDB_CACHE, FIGURES, REPORTS):
    p.mkdir(parents=True, exist_ok=True)

# ----------------------------------------------------------------------
# Date and scope (spec §5)
# ----------------------------------------------------------------------
START_DATE = "1850-01-01"
END_DATE = "1940-12-31"
START_YEAR = 1850
END_YEAR = 1940

# ----------------------------------------------------------------------
# Light-curve windows (spec §5.3, §5.4)
# ----------------------------------------------------------------------
DEFAULT_WINDOW_DAYS = 180
MAX_WINDOW_DAYS = 365
WINDOW_EXTENSION_STEP_DAYS = 30
WINDOW_EXTENSION_BOUNDARY_DAYS = 14

# ----------------------------------------------------------------------
# Brightness thresholds (spec §9)
# ----------------------------------------------------------------------
NAKED_EYE_MAG_THRESHOLD = 6.0

# ----------------------------------------------------------------------
# Magnitude model (spec §8.2)
# ----------------------------------------------------------------------
DEFAULT_K1 = 10.0  # active-comet activity slope, equivalent to n=4

# Below this K1 value, SBDB's stored (M1, K1) are treated as a nuclear /
# asteroidal fit rather than total cometary photometry, and a manual
# Tier 1.5 override is permitted (and preferred). Active comae have K1 ~ 8-15;
# inert asteroidal bodies have K1 ~ 5. See validation_results.md for context.
NUCLEAR_FIT_K1_THRESHOLD = 6.0

# ----------------------------------------------------------------------
# Caching and reproducibility (spec §15)
# ----------------------------------------------------------------------
CACHE_REMOTE_QUERIES = True
IMPLEMENT_CITY_VISIBILITY = False  # next-increment guard

# ----------------------------------------------------------------------
# Scrape behavior
# ----------------------------------------------------------------------
AERITH_BASE_URL = "https://aerith.net/comet/catalog"
AERITH_VERIFY_SSL = False  # aerith.net uses a self-signed cert
HTTP_TIMEOUT_SEC = 30
HTTP_THROTTLE_SEC = 0.25  # polite pause between scrape requests

# ----------------------------------------------------------------------
# JPL endpoints
# ----------------------------------------------------------------------
SBDB_QUERY_API = "https://ssd-api.jpl.nasa.gov/sbdb_query.api"
SBDB_LOOKUP_API = "https://ssd-api.jpl.nasa.gov/sbdb.api"
HORIZONS_OBSERVER_LOC = "500"  # geocentric

# ----------------------------------------------------------------------
# Overnight stop-condition thresholds (this conversation, not in spec)
# ----------------------------------------------------------------------
TIER3_FRACTION_HALT = 0.40       # halt if >40% apparitions get no light curve
NETWORK_OUTAGE_HALT_SEC = 30 * 60  # halt if network unreachable >30 minutes

# ----------------------------------------------------------------------
# Geographic visibility (Phase 1: geometry + extinction; spec §8.5)
# ----------------------------------------------------------------------
GEO_VISIBILITY_BANDS = [
    {"name": "Gulf",  "lat": 30.0, "city": "New Orleans"},
    {"name": "South", "lat": 35.0, "city": "Memphis"},
    {"name": "Mid",   "lat": 40.0, "city": "New York"},
    {"name": "North", "lat": 45.0, "city": "Minneapolis"},
]
GEO_OBSERVER_LON_DEG = -74.0      # NYC longitude; same for all bands (Phase 1 simplification)
GEO_LIMITING_MAG = 4.5            # urban-naked-eye threshold (headline)
GEO_LIMITING_MAG_SENSITIVITY = (4.0, 4.5, 5.0)  # all three derived from one geometry pass
GEO_EXTINCTION_K = 0.3            # mag per airmass (standard)
GEO_DARK_SUN_ALT_DEG = -12.0      # nautical twilight cutoff
GEO_MIN_ALT_DEG = 5.0             # below this altitude, treat as invisible
GEO_MIN_VISIBLE_MINUTES = 30      # margin > 0 must persist this long to count
GEO_NIGHT_SAMPLE_MINUTES = 10     # within-night sampling cadence

GEO_DAILY_OUTPUT = DATA_PROCESSED / "comet_daily_visibility.csv.gz"
