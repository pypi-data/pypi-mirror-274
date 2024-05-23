import os
from dataclasses import dataclass

# pyscript 환경 감지
try:
    from pyscript import document  # noqa: F401
    ENV = 'pyscript'
except ImportError:
    ENV = os.getenv('ENV', 'local')  # 기본값은 'local'입니다.


# # server 환경에서 실행
# export ENV=server
# python script.py
if ENV == 'server':
    from base.midasutil_server import midas_util, Product
elif ENV == 'pyscript':
    from base.midasutil_web import midas_util, Product
else:
    from base.midasutil import midas_util, Product
    
from enum import Enum

global g_base_url, g_headers
g_base_url = midas_util.get_base_url(Product.CIVIL, "KR")   
g_headers = {
    'MAPI-Key': midas_util.get_MAPI_Key(Product.CIVIL, "KR"),
    'Content-Type': 'application/json'
}


class MidasAPI:
    base_url = g_base_url
    headers = g_headers

    class AnalysisType(Enum):
        ANALYSIS = "Analysis"
        PUSHOVER = "Pushover"
    
    @dataclass
    class tableFormat:
        """
        Standard table format for the MIDAS API
        {
            "HEAD": ["Strain", "Stress"],
            "DATA": [[0.1, 2, 4, 4, 35], [0, 234235, 235, 235, 0]],
        }
        """
        HEAD: list[str , 2]
        DATA: list[list[float , 2]]

    @classmethod
    def create_instance(cls, product, country="KR"):
        cls.base_url = midas_util.get_base_url(product, country)
        cls.headers = {
            'MAPI-Key': midas_util.get_MAPI_Key(product, country),
            'Content-Type': 'application/json'
        }
        return cls()

    @classmethod
    def doc_open(cls, file_path):
        url = f'{cls.base_url}/doc/open'
        return midas_util.post(url, headers=cls.headers, json={'Argument': file_path})

    @classmethod
    def doc_anal(cls, AnalysisType: AnalysisType = AnalysisType.ANALYSIS):
        """
        Request the analysis of the current document

        Args:
            AnalysisType (AnalysisType): The type of the analysis (Analysis or Pushover)

        Returns:
            dict: The result of the analysis of the current document
            e.g. doc_anal() -> {'message': 'MIDAS CIVIL NX command complete'}
        """
        url = f'{cls.base_url}/doc/anal'
        json_body = {}
        if AnalysisType == cls.AnalysisType.PUSHOVER:
            json_body = {'Argument': {'TYPE': AnalysisType.value}}

        return midas_util.post(url, headers=cls.headers, json=json_body)

    # db #############################################################################################################
    @classmethod
    def db_create(cls, item_name: str, items: dict) -> dict:
        """
        Create the items to the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
            items: The items of the current document's collection with the name

        Returns:
            dict: created result of the current document's collection with the name
            e.g. db_create("NODE", {1: {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }}) -> {'NODE': {1: {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }}}
            e.g. db_create("ELEM", {1: {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}}) -> {'ELEM': {1: {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}}
        """
        url = f'{cls.base_url}/db/{item_name}'
        return midas_util.post(url, headers=cls.headers, json={'Assign': items})

    @classmethod
    def db_create_item(cls, item_name: str, item_id: int, item: dict) -> dict:
        """
        Create the item to the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
            item_id: The item id of the collection
            item: The item of the current document's collection with the name and id

        Returns:
            dict: created result of the current document's collection with the name and id
            e.g. db_create_item("NODE", 1, {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }) -> {'NODE': {'1': {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }}}
            e.g. db_create_item("ELEM", 1, {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}) -> {'ELEM': {'1': {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}}
        """

        url = f'{cls.base_url}/db/{item_name}/{item_id}'
        return midas_util.post(url, headers=cls.headers, json={'Assign': item})

    @classmethod
    def db_read(cls, item_name: str) -> dict:
        """
        Requst(using api) All items from the specified name collection
        !!! don't use this function in the loop, it's too slow !!!

        Args:
            item_name: The collection name of the current document (NODE, ELEM, MATL, SECT, etc.)

        Returns:
            dict: The items of the current document's collection with the name
            e.g. db_read("NODE") -> {1: {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }}
            e.g. db_read("ELEM") -> {1: {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}}
        """
        url = f'{cls.base_url}/db/{item_name}'
        responseJson = midas_util.get(url, headers=cls.headers)
        # check response.json()[item_name] is Exist
        if item_name not in responseJson:
            print(f"Error: Unable to find the registry key or value for {item_name}")
            return None
            # return midas_util.ERROR_DICT(message=f"Unable to find the registry key or value for {item_name}")
        keyVals = responseJson[item_name]
        return {int(k): v for k, v in keyVals.items()}

    @classmethod
    def db_read_item(cls, item_name: str, item_id: int) -> dict:
        """
        Requst(using api) the item from the current document
        !!! don't use this function in the loop, it's too slow !!!

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
            item_id: The item id of the collection

        Returns:
            dict: The item of the current document's collection with the name and id
            e.g. db_read_item("NODE", 1) -> {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }
            e.g. db_read_item("ELEM", 1) -> {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}
            e.g. db_read_item("MATL", 1) -> {'MATL': {'1': {'TYPE': 'CONC', 'NAME': 'C24', 'HE_SPEC': 0, 'HE_COND': 0, 'PLMT': 0, 'P_NAME': '', 'bMASS_DENS': False, 'DAMP_RAT': 0.05, 'PARAM': [{'P_TYPE': 1, 'STANDARD': 'KS01-Civil(RC)', 'CODE': 'KCI-2007', 'DB': 'C24', 'bELAST': False, 'ELAST': 26964000}]}}}
            
        """
        item_id_str = str(item_id)
        url = f'{cls.base_url}/db/{item_name}/{item_id_str}'
        responseJson = midas_util.get(url, headers=cls.headers)
        # check response.json()[item_name] is Exist
        if item_name not in responseJson:
            print(f"Error: Unable to find the registry key or value for {item_name}")
            return None
            # return midas_util.ERROR_DICT(message=f"Unable to find the registry key or value for {item_name}")
        if item_id_str not in responseJson[item_name]:
            print(
                f"Error: Unable to find the registry key or value for {item_id}")
            return None
            # return midas_util.ERROR_DICT(message=f"Unable to find the registry key or value for {item_id}")
        return responseJson[item_name][item_id_str]

    @classmethod
    def db_update(cls, item_name: str, items: dict) -> dict:
        """
        Update the items to the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
            items: The items of the current document's collection with the name

        Returns:
            dict: updated result of the current document's collection with the name
            e.g. db_update("NODE", {1: {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }}) -> {'NODE': {1: {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }}}
            e.g. db_update("ELEM", {1: {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}}) -> {'ELEM': {1: {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}}
        """

        url = f'{cls.base_url}/db/{item_name}'
        return midas_util.put(url, headers=cls.headers, json={'Assign': items})

    @classmethod
    def db_update_item(cls, item_name: str, item_id: int, item: dict) -> dict:
        """
        Update the item to the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
            item_id: The item id of the collection
            item: The item of the current document's collection with the name and id

        Returns:
            dict: updated result of the current document's collection with the name and id
            e.g. db_update_item("NODE", 1, {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }) -> {'NODE': {'1': {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }}}
            e.g. db_update_item("ELEM", 1, {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}) -> {'ELEM': {'1': {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}}
        """

        url = f'{cls.base_url}/db/{item_name}/{item_id}'
        return midas_util.put(url, headers=cls.headers, json={'Assign': item})

    @classmethod
    def db_delete(cls, item_name: str, item_id: int) -> dict:
        """
        Delete the item from the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
            item_id: The item id of the collection

        Returns:
            dict: deleted result of the current document's collection with the name and id
            e.g. db_delete("NODE", 1) -> {'NODE': {'1': {'X': 0.0, 'Y': 0.0, 'Z': 0.0 }}}
            e.g. db_delete("ELEM", 1) -> {'ELEM': {'1': {'TYPE': 'BEAM', 'MATL': 1, 'SECT': 1, 'NODE': [1, 2, 0, 0, 0, 0, 0, 0], 'ANGLE': 0, 'STYPE': 0}}
        """
        url = f'{cls.base_url}/db/{item_name}/{item_id}'
        return midas_util.delete(url, headers=cls.headers)

    @classmethod
    def db_get_next_id(cls, item_name: str) -> int:
        """
        Get the next ID of the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)

        Returns:
            int: The next ID
        """

        res_all = cls.db_read(item_name)
        if not res_all:
            return 1
        next_id = max(map(int, res_all.keys()))
        return next_id + 1

    @classmethod
    def db_get_max_id(cls, item_name: str) -> int:
        """
        Get the max ID of the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
        """

        res_all = cls.db_read(item_name)
        if not res_all:
            return 0
        return max(map(int, res_all.keys()))

    @classmethod
    def db_get_min_id(cls, item_name: str) -> int:
        """
        Get the min ID of the current document

        Args:
            item_name: The collection name (NODE, ELEM, MATL, SECT, etc.)
        """

        res_all = cls.db_read(item_name)
        if not res_all:
            return 1
        return min(map(int, res_all.keys()))

    # view ############################################################################################################
    @classmethod
    def view_select_get(cls) -> dict:
        """
        Get the selected NODE/ELEM of the current document view

        Returns:
            dict: The selected NODE/ELEM of the current view
            e.g. view_select_get() -> {'NODE_LIST': [1, 2], 'ELEM_LIST': [1]}        
        """
        url = f'{cls.base_url}/view/select'
        responseJson = midas_util.get(url, headers=cls.headers)
        if 'error' in responseJson:
            return responseJson
        else:
            return responseJson['SELECT']

    # Steel Code Check (Gen Only) ########################################################################################################
    @classmethod
    def post_steelcodecheck(cls):
        """
        Request the steel code check

        Returns:
            dict: The result of the steel code check
            e.g. post_steelcodecheck() -> {'message': 'MIDAS CIVIL NX command complete'}, TODO: check the result
        """
        url = f'{cls.base_url}/post/steelcodecheck'
        return midas_util.post(url, headers=cls.headers, json={})

    # static function ##########################################################################################################
    @staticmethod
    def select_by_subkey(value, dict, *subkey):
        ret = []
        if (len(subkey) == 1):
            ret = [key for key in dict.keys() if dict[key][subkey[0]] == value]
        if (len(subkey) == 2):
            ret = [key for key in dict.keys() if dict[key][subkey[0]][subkey[1]] == value]
        if (len(subkey) == 3):
            ret = [key for key in dict.keys() if dict[key][subkey[0]][subkey[1]][subkey[2]] == value]
        if (len(subkey) == 4):
            ret = [key for key in dict.keys() if dict[key][subkey[0]][subkey[1]][subkey[2]][subkey[3]] == value]
        if (len(subkey) == 5):
            ret = [key for key in dict.keys() if dict[key][subkey[0]][subkey[1]][subkey[2]][subkey[3]][subkey[4]] == value]

        if (len(subkey) > 5):
            print("Error: Please check the subkey length")
            # return None
            return midas_util.ERROR_DICT(message="Please check the subkey length")
        if (len(ret) == 0):
            print("Error: Please check the subkey value")
            # return None
            return midas_util.ERROR_DICT(message="Please check the subkey value")
        return ret[0]

    @staticmethod
    def get_subitem_next_id(subitem_list: dict) -> int:
        """
        Get the next ID of the subitem list

        Args:
            subitem_list (dict): The subitem list

        Returns:
            int: The next ID
        """

        if 'ITEMS' not in subitem_list:
            return 1
        return max(map(lambda x: x['ID'], subitem_list['ITEMS'])) + 1
