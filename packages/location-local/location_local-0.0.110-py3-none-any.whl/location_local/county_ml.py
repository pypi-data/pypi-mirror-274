from database_mysql_local.generic_crud_ml import GenericCRUDML
from language_remote.lang_code import LangCode
from logger_local.LoggerLocal import Logger
from user_context_remote.user_context import UserContext

from .location_local_constants import LocationLocalConstants

logger = Logger.create_logger(object=LocationLocalConstants.OBJECT_FOR_LOGGER_CODE)
user_context = UserContext()


class CountyMl(GenericCRUDML):
    def __init__(self, is_test_data: bool = False):
        logger.start("start init CountyMl")
        super().__init__(
            default_schema_name=LocationLocalConstants.LOCATION_SCHEMA_NAME,
            default_table_name=LocationLocalConstants.COUNTY_ML_TABLE_NAME,
            default_column_name=LocationLocalConstants.COUNTY_ML_ID_COLUMN_NAME,
            default_view_table_name=LocationLocalConstants.COUNTY_ML_VIEW_NAME,
            default_ml_view_table_name=LocationLocalConstants.COUNTY_ML_VIEW_NAME,
            is_test_data=is_test_data)
        logger.end("end init CountyMl")

    def insert(  # noqa
            self, *, county_id: int, county: str, title_approved: bool = False,
            lang_code: LangCode = LocationLocalConstants.DEFAULT_LANG_CODE) -> int:
        logger.start("start insert county_ml",
                     object={'county_id': county_id, 'county': county,
                             'lang_code': lang_code,
                             'title_approved': title_approved})
        LangCode.validate(lang_code)
        lang_code = lang_code or LangCode.detect_lang_code(county)
        county_ml_dict = {
            key: value for key, value in {
                'county_id': county_id,
                'lang_code': lang_code.value,
                'title': county,
                'title_approved': title_approved
            }.items() if value is not None
        }
        county_ml_id = super().insert(
            table_name=LocationLocalConstants.COUNTY_ML_TABLE_NAME,
            data_dict=county_ml_dict)
        logger.end("end insert county_ml",
                   object={'county_ml_id': county_ml_id})

        return county_ml_id
