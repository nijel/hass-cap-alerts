"""Sensor platform for CAP Alerts integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .cap_parser import CAPAlert
from .const import (
    ATTR_AREA,
    ATTR_AWARENESS_LEVEL,
    ATTR_AWARENESS_TYPE,
    ATTR_CATEGORY,
    ATTR_CERTAINTY,
    ATTR_DESCRIPTION,
    ATTR_EFFECTIVE,
    ATTR_EVENT,
    ATTR_EXPIRES,
    ATTR_HEADLINE,
    ATTR_INSTRUCTION,
    ATTR_RESPONSE_TYPE,
    ATTR_SENDER,
    ATTR_SEVERITY,
    ATTR_URGENCY,
    AWARENESS_ICONS,
    AWARENESS_LEVEL_GREEN,
    AWARENESS_LEVEL_ORANGE,
    AWARENESS_LEVEL_RED,
    AWARENESS_LEVEL_YELLOW,
    DOMAIN,
    SEVERITY_TO_AWARENESS,
)
from .coordinator import CAPAlertsCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up CAP Alerts sensors from a config entry."""
    coordinator: CAPAlertsCoordinator = hass.data[DOMAIN][entry.entry_id]

    # Create a summary sensor
    async_add_entities([CAPAlertsSummarySensor(coordinator, entry)])


class CAPAlertsSummarySensor(CoordinatorEntity[CAPAlertsCoordinator], SensorEntity):
    """Sensor showing CAP alerts with meteoalarm compatibility."""

    _attr_has_entity_name = True
    
    # Priority order for awareness levels: red > orange > yellow > green
    _LEVEL_PRIORITY = {
        AWARENESS_LEVEL_RED: 4,
        AWARENESS_LEVEL_ORANGE: 3,
        AWARENESS_LEVEL_YELLOW: 2,
        AWARENESS_LEVEL_GREEN: 1,
    }

    def __init__(
        self,
        coordinator: CAPAlertsCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_alert_count"
        self._attr_name = "Alert count"

    def _get_highest_awareness_level(self) -> str:
        """Get the highest awareness level from active alerts."""
        if not self.coordinator.data:
            return AWARENESS_LEVEL_GREEN
        
        highest_level = AWARENESS_LEVEL_GREEN
        highest_priority = 0
        
        for alert in self.coordinator.data:
            awareness = SEVERITY_TO_AWARENESS.get(alert.severity, AWARENESS_LEVEL_GREEN)
            priority = self._LEVEL_PRIORITY.get(awareness, 0)
            if priority > highest_priority:
                highest_priority = priority
                highest_level = awareness
        
        return highest_level

    @property
    def native_value(self) -> str:
        """Return the highest awareness level (meteoalarm compatible)."""
        return self._get_highest_awareness_level()

    @property
    def icon(self) -> str:
        """Return the icon based on awareness level."""
        awareness_level = self._get_highest_awareness_level()
        return AWARENESS_ICONS.get(awareness_level, "mdi:alert")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional state attributes."""
        if not self.coordinator.data:
            return {
                ATTR_AWARENESS_LEVEL: AWARENESS_LEVEL_GREEN,
                ATTR_AWARENESS_TYPE: None,
                "alert_count": 0,
            }

        # Get the alert with the highest severity
        highest_alert = None
        highest_priority = 0
        
        for alert in self.coordinator.data:
            awareness = SEVERITY_TO_AWARENESS.get(alert.severity, AWARENESS_LEVEL_GREEN)
            priority = self._LEVEL_PRIORITY.get(awareness, 0)
            if priority > highest_priority:
                highest_priority = priority
                highest_alert = alert

        # Include details of all active alerts
        alerts_details = []
        for alert in self.coordinator.data:
            awareness_level = SEVERITY_TO_AWARENESS.get(alert.severity, AWARENESS_LEVEL_GREEN)
            alert_info = {
                "identifier": alert.identifier,
                ATTR_HEADLINE: alert.headline,
                ATTR_DESCRIPTION: alert.description,
                ATTR_SEVERITY: alert.severity,
                ATTR_URGENCY: alert.urgency,
                ATTR_CERTAINTY: alert.certainty,
                ATTR_EVENT: alert.event,
                ATTR_EFFECTIVE: alert.effective,
                ATTR_EXPIRES: alert.expires,
                ATTR_SENDER: alert.sender,
                ATTR_INSTRUCTION: alert.instruction,
                ATTR_CATEGORY: alert.category,
                ATTR_RESPONSE_TYPE: alert.response_type,
                ATTR_AREA: ", ".join(alert.areas),
                ATTR_AWARENESS_LEVEL: awareness_level,
                ATTR_AWARENESS_TYPE: alert.event,
            }
            alerts_details.append(alert_info)

        return {
            ATTR_AWARENESS_LEVEL: self._get_highest_awareness_level(),
            ATTR_AWARENESS_TYPE: highest_alert.event if highest_alert else None,
            "alert_count": len(self.coordinator.data),
            "alerts": alerts_details,
        }
