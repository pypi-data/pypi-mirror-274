from django.conf import settings
from netbox.plugins import PluginMenuItem


PLUGIN_SETTINGS = settings.PLUGINS_CONFIG.get("netbox_device_support_plugin", dict())
DEVICE_VENDORS = PLUGIN_SETTINGS.get("DEVICE_VENDORS", ["Cisco"])
CISCO_MANUFACTURER = PLUGIN_SETTINGS.get("CISCO_MANUFACTURER", "Cisco")
FORTINET_MANUFACTURER = PLUGIN_SETTINGS.get("FORTINET_MANUFACTURER", "Fortinet")
PURESTORAGE_MANUFACTURER = PLUGIN_SETTINGS.get("PURESTORAGE_MANUFACTURER", "Pure Storage")

menu_items = []

if CISCO_MANUFACTURER in DEVICE_VENDORS:
    menu_items.append(
        PluginMenuItem(
            link="plugins:netbox_device_support_plugin:ciscodevicesupport_list",
            link_text="Cisco Device Support",
        )
    )
    menu_items.append(
    PluginMenuItem(
            link="plugins:netbox_device_support_plugin:ciscodevicetypesupport_list",
            link_text="Cisco Device Type Support",
        )
    )

if FORTINET_MANUFACTURER in DEVICE_VENDORS:
    menu_items.append(
        PluginMenuItem(
            link="plugins:netbox_device_support_plugin:fortinetdevicesupport_list",
            link_text="Fortinet Device Support",
        )
    )

if PURESTORAGE_MANUFACTURER in DEVICE_VENDORS:
    menu_items.append(
        PluginMenuItem(
            link="plugins:netbox_device_support_plugin:purestoragedevicesupport_list",
            link_text="PureStorage Device Support",
        )
    )

menu_items = tuple(menu_items)
