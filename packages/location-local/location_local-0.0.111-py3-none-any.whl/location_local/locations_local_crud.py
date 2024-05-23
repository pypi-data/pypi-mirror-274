from typing import Dict

from database_mysql_local.generic_crud import GenericCRUD
from database_mysql_local.point import Point
from language_remote.lang_code import LangCode
from logger_local.LoggerComponentEnum import LoggerComponentEnum
from logger_local.LoggerLocal import Logger
from user_context_remote.user_context import UserContext

from .city import City
from .country import CountriesLocal
from .county import County
from .location_local_constants import LocationLocalConstants
from .neighborhood import Neighborhood
from .region import Region
from .state import State
from .util import LocationsUtil

DUMMY_POINT = Point(0, 0)
LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_ID = LocationLocalConstants.LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_ID
LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME = LocationLocalConstants.LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME

object_to_insert = {
    'component_id': LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_ID,
    'component_name': LOCATION_LOCAL_PYTHON_PACKAGE_COMPONENT_NAME,
    'component_category': LoggerComponentEnum.ComponentCategory.Code.value,
    'developer_email': 'tal.g@circ.zone'
}

logger = Logger.create_logger(object=object_to_insert)

user_context = UserContext()


# TODO Create LocationsLocal.get_country_id_by_location_id() and call it
# from importer-local-python-package

# TODO: add location ml using crud ml
class LocationsLocal(GenericCRUD):
    def __init__(self, is_test_data: bool = False):
        logger.start("start init LocationLocal")

        GenericCRUD.__init__(
            self,
            default_schema_name=LocationLocalConstants.LOCATION_SCHEMA_NAME,
            default_table_name=LocationLocalConstants.LOCATION_TABLE_NAME,
            default_view_table_name=LocationLocalConstants.LOCATION_VIEW_NAME,
            default_column_name=LocationLocalConstants.LOCATION_ID_COLUMN_NAME,
            is_test_data=is_test_data)

        # Initiated with None for performance reasons
        self.city_instance = None
        self.country_instance = None
        self.county_instance = None
        self.neighborhood_instance = None
        self.region_instance = None
        self.state_instance = None

        logger.end("end init LocationLocal")

    def get_location_dict(self, *, neighborhood_name: str, county_name: str, region_name: str, state_name: str,
                          country_name: str, city_name: str, lang_codes_dict: dict = None) -> dict:
        # TODO Fix the algorithm as the current will not work in all cases. i.e. same neighborhood name in different places
        logger.start("start get location ids",
                     object={'neighborhood_name': neighborhood_name,
                             'county_name': county_name,
                             'region_name': region_name,
                             'state_name': state_name,
                             'country_name': country_name,
                             'city_name': city_name})
        lang_codes_dict = lang_codes_dict or {}
        self.city_instance = self.city_instance or City()
        self.country_instance = self.country_instance or CountriesLocal()
        self.county_instance = self.county_instance or County()
        self.neighborhood_instance = self.neighborhood_instance or Neighborhood()
        self.region_instance = self.region_instance or Region()
        self.state_instance = self.state_instance or State()

        neighborhood_id = self.neighborhood_instance.get_neighborhood_id_by_neighborhood_name(
            neighborhood_name=neighborhood_name,
            lang_code=LocationsUtil.get_lang_code(lang_codes_dict, "neighborhood"))
        county_id = self.county_instance.get_county_id_by_county_name_state_id(
            county_name=county_name,
            lang_code=LocationsUtil.get_lang_code(lang_codes_dict, "county"))
        region_id = self.region_instance.get_region_id_by_region_name(
            region_name=region_name,
            lang_code=LocationsUtil.get_lang_code(lang_codes_dict, "region"))
        state_id = self.state_instance.get_state_id_by_state_name(
            state_name=state_name,
            lang_code=LocationsUtil.get_lang_code(lang_codes_dict, "state"))
        country_id = self.country_instance.get_country_id_by_country_name(
            country_name=country_name,
            lang_code=LocationsUtil.get_lang_code(lang_codes_dict, "country"))
        city_id = self.city_instance.get_city_id_by_city_name(
            city_name=city_name,
            lang_code=LocationsUtil.get_lang_code(lang_codes_dict, "city"))
        location_dict = {"neighborhood_id": neighborhood_id, "county_id": county_id, "region_id": region_id,
                         "state_id": state_id, "country_id": country_id, "city_id": city_id}
        logger.end(object=location_dict)
        return location_dict

    def insert(self, *,  # noqa
               data: Dict[str, any],
               lang_code: LangCode = LocationLocalConstants.DEFAULT_LANG_CODE,
               is_approved: bool = False,
               is_test_data: bool = False,
               lang_codes_dict: dict = None,
               new_country_data: Dict[str, any] = None) -> int or None:

        logger.start("start insert location",
                     object={'data': data, 'lang_code': lang_code,
                             'is_approved': is_approved, 'is_test_data': is_test_data,
                             'new_country_data': new_country_data})
        if not data:
            logger.warning(log_message="Location was not inserted because no data was provided")
            return None
        LangCode.validate(lang_code)
        lang_code = lang_code or user_context.get_effective_profile_preferred_lang_code()
        lang_codes_dict = lang_codes_dict or {}
        lang_codes_dict["default"] = lang_code
        location_dict = self._check_details_and_insert_if_not_exist(
            data=data, lang_codes_dict=lang_codes_dict,
            is_approved=is_approved, new_country_data=new_country_data)

        location_dict = {
            key: value for key, value in {
                'coordinate': data.get("coordinate"),
                'address_local_language': data.get("address_local_language"),
                'address_english': data.get("address_english"),
                'neighborhood_id': location_dict.get("neighborhood_id"),
                'county_id': location_dict.get("county_id"),
                'region_id': location_dict.get("region_id"),
                'state_id': location_dict.get("state_id"),
                'country_id': location_dict.get("country_id"),
                'city_id': location_dict.get("city_id"),
                'postal_code': data.get("postal_code"),
                'plus_code': data.get("plus_code"),
                'is_approved': is_approved,
                'is_test_data': is_test_data
            }.items() if value is not None
        }
        # We want to allow multiple locations for the same coordinates
        # We could do that if we had the location name
        # location_id = self.select_one_value_by_id(select_clause_value="location_id",
        #                                           column_name="coordinate", column_value=data.get("coordinate"))
        if data.get("coordinate") == DUMMY_POINT:  # used for tests
            location_id = 0
        else:
            location_id = super().insert(data_dict=location_dict)

        logger.end("end_insert location", object={'location_id': location_id})
        return location_id

    def update(self, *, location_id: int, data: Dict[str, any],
               lang_code: LangCode = LocationLocalConstants.DEFAULT_LANG_CODE, is_approved: bool = False,
               lang_codes_dict: dict = None):

        logger.start("start update location",
                     object={'location_id': location_id, 'data': data,
                             'lang_code': lang_code,
                             'is_approved': is_approved})
        lang_codes_dict = lang_codes_dict or {}
        lang_codes_dict["default"] = lang_code
        location_info = self._check_details_and_insert_if_not_exist(
            data=data,
            lang_codes_dict=lang_codes_dict,
            is_approved=is_approved)

        updated_location_dict = {
            key: value for key, value in {
                'coordinate': data.get('coordinate'),
                'address_local_language': data.get(
                    "address_local_language"),
                'address_english': data.get("address_english"),
                'neighborhood_id': location_info.get("neighborhood_id"),
                'county_id': location_info.get("county_id"),
                'region_id': location_info.get("region_id"),
                'state_id': location_info.get("state_id"),
                'country_id': location_info.get("country_id"),
                'city_id': location_info.get("city_id"),
                'postal_code': data.get("postal_code"),
                'plus_code': data.get("plus_code"),
                'is_approved': is_approved
            }.items() if value is not None
        }
        super().update_by_column_and_value(
            column_value=location_id,
            data_dict=updated_location_dict
        )

        logger.end("end update location")

    def read(self, location_id: int) -> dict:
        logger.start("start read location",
                     object={'location_id': location_id})
        result = super().select_one_dict_by_column_and_value(
            column_value=location_id,
            select_clause_value=LocationLocalConstants.LOCATION_TABLE_COLUMNS)

        result = LocationsUtil.extract_coordinates_and_replace_by_point(data_dict=result)
        logger.end("end read location",
                   object={"result": result})
        return result

    def delete(self, location_id: int):
        logger.start("start delete location by id",
                     object={'location_id': location_id})
        super().delete_by_column_and_value(column_value=location_id)

        logger.end("end delete location by id")

    def _check_details_and_insert_if_not_exist(
            self, *, data: dict,
            lang_codes_dict: dict = None, is_approved: bool = False,
            new_country_data: Dict[str, any] = None) -> dict or None:
        logger.start("start _check_details_and_insert_if_not_exist",
                     object={'data': data,
                             'new_country_data': new_country_data})
        coordinate = data.get("coordinate")
        neighborhood_name = data.get("neighborhood")
        county_name = data.get("county")
        region_name = data.get("region")
        state_name = data.get("state")
        country_name = data.get("country")
        city_name = data.get("city")

        location_info = self.get_location_dict(neighborhood_name=neighborhood_name, county_name=county_name,
                                               region_name=region_name, state_name=state_name,
                                               country_name=country_name,
                                               city_name=city_name, lang_codes_dict=lang_codes_dict)
        if location_info is None:
            return None

        if location_info.get("neighborhood_id") is None and neighborhood_name is not None:
            self.neighborhood_instance = self.neighborhood_instance or Neighborhood()
            location_info["neighborhood_id"] = self.neighborhood_instance.insert(
                coordinate=coordinate,
                neighborhood=neighborhood_name,
                lang_code=LocationsUtil.get_lang_code(lang_codes_dict, "neighborhood"),
                title_approved=is_approved)

        if location_info.get("county_id") is None and country_name is not None:
            self.county_instance = self.county_instance or County()
            location_info["county_id"] = self.county_instance.insert(
                coordinate=coordinate,
                county=county_name,
                state_id=location_info["state_id"],
                lang_code=LocationsUtil.get_lang_code(lang_codes_dict, "county"),
                title_approved=is_approved)

        if location_info.get("region_id") is None and region_name is not None:
            self.region_instance = self.region_instance or Region()
            location_info["region_id"] = self.region_instance.insert(
                coordinate=coordinate,
                region=region_name,
                lang_code=LocationsUtil.get_lang_code(lang_codes_dict, "region"),
                title_approved=is_approved)

        if location_info.get("state_id") is None and state_name is not None:
            self.state_instance = self.state_instance or State()
            location_info["state_id"] = self.state_instance.insert(
                coordinate=coordinate,
                state=state_name,
                lang_code=LocationsUtil.get_lang_code(lang_codes_dict, "state"),
                state_name_approved=is_approved)

        if location_info.get("country_id") is None and country_name is not None:
            self.country_instance = self.country_instance or CountriesLocal()
            location_info["country_id"] = self.country_instance.insert(
                coordinate=coordinate,
                country=country_name,
                lang_code=LocationsUtil.get_lang_code(lang_codes_dict, "country"),
                title_approved=is_approved,
                new_country_data=new_country_data)
        if location_info.get("city_id") is None and city_name is not None:
            self.city_instance = self.city_instance or City()
            location_info["city_id"] = self.city_instance.insert(
                coordinate=coordinate,
                city=city_name,
                state_id=location_info["state_id"],
                lang_code=LocationsUtil.get_lang_code(lang_codes_dict, "city"),
                title_approved=is_approved)
        logger.end("end _check_details_and_insert_if_not_exist",
                   object=location_info)
        return location_info

    def get_test_location_id(self):
        logger.start("start get_test_location_id")
        test_point = Point(0, 0)
        test_location_id = self.get_test_entity_id(
            entity_name="location",
            insert_function=self.insert,
            insert_kwargs={"data": {"coordinate": test_point}},
            view_name=LocationLocalConstants.LOCATION_VIEW_NAME)
        logger.end("end get_test_location_id", object={'test_location_id': test_location_id})
        return test_location_id
