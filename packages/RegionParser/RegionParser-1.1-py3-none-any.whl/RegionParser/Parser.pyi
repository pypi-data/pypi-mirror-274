
class Interpolator:
    def __init__(self, xml_path: str, region_param: dict, control_variables=None):
        """
        :param xml_path:
        :param region_param: dict including param_tab and param  eg. {'c_tab': 'c'}
        :param control_variables:  control_variables setup in xml
        """
        ...

    def __call__(self, arg: dict) -> list:
        """
        :param arg: exif info
        :return:
        """
        ...
