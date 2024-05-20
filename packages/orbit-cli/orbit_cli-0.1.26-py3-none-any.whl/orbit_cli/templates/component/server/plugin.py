from orbit_component_base.src.orbit_plugin import PluginBase, ArgsBase
from orbit_component_{{ project }}.schema.MyTable import MyTableCollection
from loguru import logger as log


class Plugin (PluginBase):

    NAMESPACE = '{{ project }}'
    COLLECTIONS = [MyTableCollection]


class Args (ArgsBase):
        
    def setup (self):
        return self
    
    def process (self):
        pass
    
class Tasks (ArgsBase):
    
    async def process (self):
        pass
