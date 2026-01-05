"""Constants for the CAP Alerts integration."""

DOMAIN = "cap_alerts"

# Configuration
CONF_FEED_URL = "feed_url"
CONF_AREA_FILTER = "area_filter"
CONF_SCAN_INTERVAL = "scan_interval"

# Defaults
DEFAULT_SCAN_INTERVAL = 300  # 5 minutes
DEFAULT_CHMI_URL = "https://vystrahy-cr.chmi.cz/data/XOCZ50_OKPR.xml"

# Attributes
ATTR_HEADLINE = "headline"
ATTR_DESCRIPTION = "description"
ATTR_SEVERITY = "severity"
ATTR_URGENCY = "urgency"
ATTR_CERTAINTY = "certainty"
ATTR_AREA = "area"
ATTR_EFFECTIVE = "effective"
ATTR_EXPIRES = "expires"
ATTR_EVENT = "event"
ATTR_SENDER = "sender"
ATTR_INSTRUCTION = "instruction"
ATTR_CATEGORY = "category"
ATTR_RESPONSE_TYPE = "response_type"
ATTR_AWARENESS_LEVEL = "awareness_level"
ATTR_AWARENESS_TYPE = "awareness_type"

# Awareness levels (compatible with meteoalarm)
AWARENESS_LEVEL_GREEN = "green"
AWARENESS_LEVEL_YELLOW = "yellow"
AWARENESS_LEVEL_ORANGE = "orange"
AWARENESS_LEVEL_RED = "red"

# CAP Severity to awareness level mapping
# Maps CAP severity levels to meteoalarm-compatible awareness levels:
# - Minor: Yellow (Be aware)
# - Moderate/Severe: Orange (Be prepared) 
# - Extreme: Red (Take action)
SEVERITY_TO_AWARENESS = {
    "Minor": AWARENESS_LEVEL_YELLOW,
    "Moderate": AWARENESS_LEVEL_ORANGE,
    "Severe": AWARENESS_LEVEL_ORANGE,
    "Extreme": AWARENESS_LEVEL_RED,
}

# Icons for awareness levels
AWARENESS_ICONS = {
    AWARENESS_LEVEL_GREEN: "mdi:check-circle",
    AWARENESS_LEVEL_YELLOW: "mdi:alert",
    AWARENESS_LEVEL_ORANGE: "mdi:alert-circle",
    AWARENESS_LEVEL_RED: "mdi:alert-octagon",
}
