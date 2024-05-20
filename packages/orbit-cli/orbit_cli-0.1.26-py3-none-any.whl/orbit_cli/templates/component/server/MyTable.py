from orbit_component_base.src.orbit_orm import BaseTable, BaseCollection
from orbit_database import SerialiserType, Doc
from loguru import logger as log


class MyTable (BaseTable):
    norm_table_name = 'mytable'
    norm_auditing = True
    norm_codec = SerialiserType.UJSON
    #   Add your indecies here
    norm_ensure = []
    #   Insert custom object methods here


class MyTableCollection (BaseCollection):
    table_class = MyTable
    #   Add the 'stock' get_ids method
    table_methods = ['get_ids']

    #   Add your custom collection methods here
    async def my_method (self, my_params):
        return {'ok': True, 'params': my_params}
