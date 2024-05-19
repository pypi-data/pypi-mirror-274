from database_mysql_local.connector import Connector
from database_mysql_local.generic_crud import GenericCRUD
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.LoggerLocal import Logger

ENTITY_TYPE_COMPONENT_ID = 116
ENTITY_TYPE_COMPONENT_NAME = 'entity-type-local-python-package'

logger_code_init = {
    'component_id': ENTITY_TYPE_COMPONENT_ID,
    'component_name': ENTITY_TYPE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'idan.a@circ.zone'
}
logger_local = Logger.create_logger(object=logger_code_init)

connection = Connector.connect("entity_type")


# TODO Create new class and new method EntitiesTypeEntity.valide_entity_type_entity_id() - Please use this function both in importer-local and entity-moderation-local
# TODO: use GenericCRUD
class EntitiesType(GenericCRUD):

    def __init__(self):
        pass

    @staticmethod
    # TODO change name -> title
    def get_entity_type_id_by_name(entity_type_title):
        entity_type_id = None
        try:
            object1 = {
                'entity_type_title': entity_type_title
            }
            logger_local.start(object=object1)
            sql_query = "SELECT entity_type_id FROM entity_type.entity_type_ml_view WHERE title = '{}'".format(
                entity_type_title)
            cursor = connection.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchone()
            if result:
                entity_type_id = result[0]
        except Exception as e:
            logger_local.exception(object=e)
        object1 = {
            'entity_type_id': entity_type_id
        }
        logger_local.end(object=object1)
        return entity_type_id

    @staticmethod
    # TODO Can we get the user_id from UserContext
    # TODO name -> title
    # TODO Can we avoid sending the user_id? - Using GenericCrud?
    def insert_entity_type_id_by_name(entity_type_title, user_id, system_id: int = None):
        try:
            object1 = {
                'entity_type_title': entity_type_title
            }
            logger_local.start(object=object1)

            # TODO Can we use GenericCrudMl?
            cursor = connection.cursor()
            query_entity = "INSERT INTO entity_type.entity_type_table(`name`, `created_user_id`,`updated_user_id`, `system_id`)" \
                           " VALUES (%s, %s, %s, %s)"
            cursor.execute(query_entity, (entity_type_title, user_id, user_id, system_id))
            last_inserted_id = cursor.lastrowid()

            query_entity_ml = "INSERT INTO entity_type.entity_type_ml_table(`title`,`entity_type_id`,`lang_code`,`created_user_id`,`updated_user_id`)" \
                              " VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(query_entity_ml,
                           (entity_type_title, last_inserted_id, 'en', user_id, user_id))
            logger_local.end(object={})
            connection.commit()
        except Exception as e:
            logger_local.exception(object=e)
        # TODO Return the entity_type from all insert methods
        logger_local.end(object={})
