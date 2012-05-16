from frontend.registry.cgm import base as cgm_base

@cgm_base.register_platform_module("openwrt", 1)
def general(node, cfg):
  """
  Generates general node configuration such as system hostname and
  timezone.
  """
  system = cfg.system.add('system')
  system.hostname = node.config.core.general().name
  #system.timezone = node.config.core.general().timezone

