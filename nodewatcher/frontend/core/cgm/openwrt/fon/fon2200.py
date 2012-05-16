from frontend.registry.cgm import base as cgm_base
from frontend.registry.cgm import routers as cgm_routers
from frontend.registry.cgm import protocols as cgm_protocols

from frontend.core.cgm.openwrt.fon import fon2100

class FoneraPlus(fon2100.Fonera):
  """
  Fonera FON-2200 device descriptor.
  """
  identifier = "fon-2200"
  name = "Fonera+"
  ports = [
    cgm_routers.EthernetPort("wan0", "Wan0"),
    cgm_routers.EthernetPort("lan0", "Lan0")
  ]
  
  @cgm_routers.register_module()
  def network(node, cfg):
    """
    Network configuration CGM for FON-2200.
    """
    pass

# Register the FON-2200 router
cgm_base.register_router("openwrt", FoneraPlus)

