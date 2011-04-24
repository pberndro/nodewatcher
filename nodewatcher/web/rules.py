from registry.rules.scope import *

# Alias definitions
project          = "core.general#project.name"
supported_radios = "core.general#equipment.supported_radios"
radios           = "core.radio"
vpn              = "core.vpn.server"

# Defaults
rule(changed(supported_radios),
  clear_config(radios)
)

rule(value(supported_radios) >= 1,
  append(radios,
    role = "endusers",
    essid = "open.wlan-si.net",
    bssid = "02:CA:FF:EE:BA:BE"
  )
)

rule(value(supported_radios) >= 2,
  append(radios,
    role = "mesh",
    essid = "backbone.wlan-si.net",
    bssid = "03:CA:FF:EE:BA:BE"
  )
)

# Per-project rules
rule(value(project) == "Ljubljana",
  # Override defaults, we want wlan-lj.net
  rule(value(supported_radios) >= 1,
    assign(radios, 0, essid = "open.wlan-lj.net")
  ),
  rule(value(supported_radios) >= 2,
    assign(radios, 1, essid = "backbone.wlan-lj.net")
  ),
  clear_config(vpn),
  append(vpn,
    protocol = "openvpn",
    hostname = "127.0.0.1",
    port = 9999
  ),
  append(vpn,
    protocol = "openvpn",
    hostname = "127.0.0.2",
    port = 9999
  )
)

