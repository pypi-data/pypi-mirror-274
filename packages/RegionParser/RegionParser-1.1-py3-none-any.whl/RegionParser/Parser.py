import torch
import xml.etree.ElementTree as ET


class Interpolator:
    def __init__(self, xml_path, region_param, control_variables=None):
        if control_variables is None:
            control_variables = {0: 'LuxIdx', 1: 'Gain', 2: 'DrcGain', 3: 'ExpTimeRatio', 4: 'ExpGainRatio',
                                 5: 'ExpSensitivityRatio', 6: 'CCT', 7: 'HDRMode', 8: 'LensPosition', 9: 'LensZoom',
                                 10: 'LEDSensitivity', 76: 'ColorFormat', 100: 'LEDIdx', 1001: 'CustomAwb'}
        self.region_param = region_param
        root = ET.parse(xml_path).getroot()
        self.ctrl_var_order = []
        for var_type in root.find('control_variables').iter('control_var_type'):
            self.ctrl_var_order.append(control_variables[int(var_type.text)])
        # print(f'trigger info: {self.ctrl_var_order}')

        trigger = root.findall('*')[-1].findall('*')

        self.intervals = {}
        for key in self.ctrl_var_order:
            endpoint, trigger, region = self.get_interval(trigger)
            if len(region):
                self.params = self.get_region_param(region)
            self.intervals[key] = endpoint

    def interpolate(self, value_dict):
        param = self.params
        for var in reversed(self.ctrl_var_order):
            param = self._interp(self.intervals[var], value_dict[var], param)
        if len(param):
            return param
        else:
            raise ValueError('Exif value error')

    def _interp(self, full_interval, value, full_param):
        param_interp = []

        for idx, (inter, para) in enumerate(zip(full_interval, full_param)):
            if inter[0] <= value <= inter[1]:
                param_interp.append(para)
            else:
                if idx + 1 < len(full_interval):
                    if inter[1] < value < full_interval[idx + 1][0]:
                        ratio_l = (full_interval[idx + 1][0] - value) / (full_interval[idx + 1][0] - inter[1])
                        ratio_r = (value - inter[1]) / (full_interval[idx + 1][0] - inter[1])
                        param_l = full_param[idx]
                        param_r = full_param[idx + 1]
                        param_interp.append(self.param_scaling(ratio_l, ratio_r, param_l, param_r))
        return param_interp

    def param_scaling(self, ratio_l, ratio_r, param_l, param_r):
        new_param_l = {}
        new_param_r = {}
        new_param = {}
        for key, value in param_l.items():
            new_param_l[key] = value * ratio_l
        for key, value in param_r.items():
            new_param_r[key] = value * ratio_r
        for left, right in zip(new_param_l, new_param_r):
            new_param[left] = new_param_l[left] + new_param_r[right]
        return new_param

    def get_interval(self, cur_tag: list):
        endpoints = []
        triggers = []
        regions = []
        for tag in cur_tag:
            endpoint = []
            for tag_ in tag:
                if tag_.tag == 'start':
                    endpoint.append(float(tag_.text))
                if tag_.tag == 'end':
                    endpoint.append(float(tag_.text))
                if tag_.tag == 'trigger':
                    triggers.append(tag_)
                if tag_.tag == 'region':
                    regions.append(tag_)
            endpoints.append(endpoint)
        return endpoints, triggers, regions

    def get_region_param(self, region_list: list):
        param_list = []
        for region in region_list:
            parameters = {}
            for key, value in self.region_param.items():
                cur_param = region.find(key).find(value).text
                cur_param = torch.tensor([float(i) for i in cur_param.split(" ")], dtype=torch.float32)
                parameters[value] = cur_param
            param_list.append(parameters)
        return param_list

    def __call__(self, arg):
        return self.interpolate(arg)
