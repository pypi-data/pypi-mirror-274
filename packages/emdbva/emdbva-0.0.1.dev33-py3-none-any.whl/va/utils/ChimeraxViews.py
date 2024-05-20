import json
import os
import re
import sys
import glob
import subprocess
import itertools
from distutils.spawn import find_executable
from va.utils.misc import scale_image, out_json
from va.metrics.contour_level_predicator import *
from va.utils.MapProcessor import *

class ChimeraxViews:

    def __init__(self, chimerax_bin_dir, input_json=None, va_dir=None):
        self.input_json = input_json
        self.va_dir = os.path.dirname(self.input_json) if input_json else va_dir
        if self.input_json:
            with open(input_json, 'r') as f:
                self.json_data = json.load(f)
        else:
            self.json_data = None
            print('There is no json file data.')

        self.chimerax = chimerax_bin_dir


    def get_root_data(self, data_type):
        """
            Get the root json data based on the input json file and the data type

        :param data_type: a string of full path name of the json file
        """

        root_data = None
        if data_type in self.json_data.keys():
            root_data = self.json_data[data_type]
            try:
                del root_data['err']
            except:
                print('There is/are %s model(s).' % len(root_data))
        else:
            print(f'{data_type} json result is')

        return root_data

    def write_residue_cxc(self, colors, residues, map_name, model_name, data_type, min_median_max):
        """
            Write a ChimeraX cxc file for generating surfaces with model cases
        :param colors: list of colors
        :param residues: list of residues e.g., A:321 THR
        :param map_name: a string of input file name
        :param model_name: a string of input model name
        :param data_type: a string of surface type, e.g., residue_local_resolution
        """

        if data_type:
            cur_type = data_type.replace('_', '')
            chimerax_file_name = f'{map_name}_{model_name}_{cur_type}_chimerax.cxc'
        else:
            cur_type = ''
            chimerax_file_name = f'{map_name}_{model_name}_chimerax.cxc'

        surface_file_name = '{}/{}_{}'.format(self.va_dir, map_name, model_name)
        model = f'{self.va_dir}/{model_name}'
        list_items = list(itertools.islice(min_median_max.items(), 3))
        min_value, min_color = list_items[0]
        median_value, median_color = list_items[1]
        max_value, max_color = list_items[2]
        with open(f'{self.va_dir}/{chimerax_file_name}', 'w') as fp:
            fp.write(f'open {model} format mmcif\n')
            fp.write('show selAtoms ribbons\n')
            fp.write('hide selAtoms\n')

            for (color, residue) in zip(colors, residues):
                chain, restmp = residue.split(':')
                # Not sure if all the letters should be replaced
                # res = re.sub("\D", "", restmp)
                res = re.findall(r'-?\d+', restmp)[0]
                fp.write(
                    f'color /{chain}:{res} {color}\n'
                )
            fp.write(
                'key showTool true\n' 
                'key size 0.25000,0.02000\n'
                'key pos 0.72000,0.05000\n'
                # f'key blue-white-red :{round(min, 2)} :{round((min+max)/2, 2)} :{round(max, 2)}\n'
                f'key {min_color}:{round(min_value, 2)} {median_color}:{round(median_value, 2)} {max_color}:{round(max_value, 2)}\n'
                'set bgColor white\n'
                'lighting soft\n'
                'view cofr True\n'
                f'save {str(surface_file_name)}_z{cur_type}.jpeg supersample 3 width 1200 height 1200\n'
                'turn x -90\n'
                'turn y -90\n'
                'view cofr True\n'
                f'save {str(surface_file_name)}_y{cur_type}.jpeg supersample 3 width 1200 height 1200\n'
                'view orient\n'
                'turn x 90\n'
                'turn z 90\n'
                'view cofr True\n'
                f'save {str(surface_file_name)}_x{cur_type}.jpeg supersample 3 width 1200 height 1200\n'
                'close all\n'
                'exit'
            )

            return chimerax_file_name

    def write_maps_cxc(self, map_name, map_two, data_type):
        """
            Write a ChimeraX cxc file for generating surfaces with model cases
        :param map_name: a string of input file name
        :param map_two: a string of input model name
        :param data_type: a string of surface type, e.g., residue_local_resolution
        """

        if data_type:
            cur_type = data_type.replace('_', '')
            chimerax_file_name = f'{map_name}_{cur_type}_chimerax.cxc'
        else:
            cur_type = ''
            chimerax_file_name = f'{map_name}_chimerax.cxc'

        map_fullname = f'{self.va_dir}/{map_name[:-4]}.map'
        # mask_fullname = f'{self.va_dir}/{map_name}_relion/mask/{map_name}_mask.mrc'

        surface_file_name = '{}/{}'.format(self.va_dir, map_name)
        with open(f'{self.va_dir}/{chimerax_file_name}', 'w') as fp:
            fp.write(f'open {map_fullname} format ccp4\n')
            fp.write(f'open {map_two} format ccp4\n')
            if data_type == 'map_local_resolution':
                a = mrcfile.open(map_fullname)
                d = a.data
                raw_contour = f'{calc_level_dev(d)[0]}'
                fp.write(f'volume #1 step 1 level {raw_contour}\n')
                fp.write('color sample #1 map #2 palette bluered key true\n')
                fp.write('key size 0.25000,0.02000\n')
                fp.write('key pos 0.72000,0.05000\n')
                fp.write('hide #!2 models\n')
            if data_type == 'map_mask':
                # prepare for map and mask overlay views here
                pass

            fp.write(
                'set bgColor white\n'
                'lighting soft\n'
                'view cofr True\n'
                f'save {str(surface_file_name)}_z{cur_type}.jpeg supersample 3 width 1200 height 1200\n'
                'turn x -90\n'
                'turn y -90\n'
                'view cofr True\n'
                f'save {str(surface_file_name)}_y{cur_type}.jpeg supersample 3 width 1200 height 1200\n'
                'view orient\n'
                'turn x 90\n'
                'turn z 90\n'
                'view cofr True\n'
                f'save {str(surface_file_name)}_x{cur_type}.jpeg supersample 3 width 1200 height 1200\n'
                'close all\n'
                'exit'
                # First line: show on z axis plane 220 with step 1 at contour level 0.01 with style surface
                # 2nd line: as 1st line is one plane, 2nd line turn it back to full surface with contour level 3.5
                #           at step 1 so it can continue the same 2 lines to get other axis planes
                # 'volume #1 planes z,220 step 1 level 0.01 style surface'
                # 'volume #1 style surface region all level 3.5 step 1'
            )

            return chimerax_file_name

    def run_chimerax(self, chimerax_file_name):
        """
            Run ChimeraX to produce the surface views

        :param chimerax_file_name: a string of ChimeraX cxc file
        """
        errs = []
        chimerax = self.chimerax
        model_name = chimerax_file_name.split('_')[1]
        bin_display = os.getenv('DISPLAY')
        try:
            if not bin_display:
                subprocess.check_call(f'{chimerax} --offscreen --nogui {self.va_dir}/{chimerax_file_name}',
                                      cwd=self.va_dir, shell=True)
                print('Colored models were produced.')
            else:
                subprocess.check_call(f'{chimerax}  {self.va_dir}/{chimerax_file_name}', cwd=self.va_dir, shell=True)
                print('Colored models were produced.')

            return None
        except subprocess.CalledProcessError as e:
            err = 'Saving model {} fit surface view error: {}.'.format(model_name, e)
            errs.append(err)
            sys.stderr.write(err + '\n')

            return errs

    def rescale_view(self, map_name, model_name=None, data_type=None):
        """
            Scale views and produce corresponding dictionary

        :param map_name: a string of input map name
        :param model_name: a string of input model name
        :param data_type: a string of view type
        """

        original = {}
        scaled = {}
        result = {}
        used_data_type = data_type.replace('_', '')
        for i in 'xyz':
            if model_name is None:
                image_name = f'{map_name}_{i}{used_data_type}.jpeg'
            else:
                image_name = f'{map_name}_{model_name}_{i}{used_data_type}.jpeg'
            full_image_path = f'{self.va_dir}/{image_name}'
            if os.path.isfile(full_image_path):
                scaled_image_name = scale_image(full_image_path, (300, 300))
                original[i] = image_name
                scaled[i] = scaled_image_name
        result['original'] = original
        result['scaled'] = scaled

        return result

    # def binarized_mask(self, mapname):
    #     """
    #
    #     """
    #
    #     input_mask = f'{self.va_dir}/{mapname}_relion/mask/{mapname}_mask.mrc'
    #     masked_map = mrcfile.open(input_mask)
    #     masked_map_data = masked_map.data > 0.5
    #     new_data = masked_map_data.astype(np.uint8)
    #     outmap_name = f'{self.va_dir}/{mapname}_binarized_mask.mrc'
    #     mout = mrcfile.new(outmap_name, overwrite=True)
    #     mout.set_data(new_data)
    #     mout.voxel_size = masked_map.voxel_size
    #     mout.close()
    #
    #     return outmap_name
    #
    # def binarized_locres(self, binarized_mask, locres_map):
    #     """
    #
    #     """
    #
    #     map_name = os.path.basename(binarized_mask).replace('_binarized_mask.mrc', '')
    #     binarized_mask_obj = mrcfile.open(binarized_mask)
    #     binarized_mask_data = binarized_mask_obj.data
    #     locres_map_obj = mrcfile.open(locres_map)
    #     locres_map_data = locres_map_obj.data
    #     raw_map = f'{self.va_dir}/{map_name[:-4] + "_rawmap.map"}'
    #     raw_map_obj = mrcfile.open(raw_map)
    #     raw_map_data = raw_map_obj.data
    #     binarized_raw_data = raw_map_data * binarized_mask_data
    #     binarized_raw_file = f'{self.va_dir}/{map_name}_binarized_raw.map'
    #     out = mrcfile.new(binarized_raw_file, overwrite=True)
    #     out.set_data(binarized_raw_data)
    #     out.voxel_size = binarized_mask_obj.voxel_size
    #     out.close()
    #
    #     binarized_locres_data = locres_map_data * binarized_mask_data
    #     binarized_locres_file = f'{self.va_dir}/{map_name}_binarized_locres.mrc'
    #     mout = mrcfile.new(binarized_locres_file, overwrite=True)
    #     mout.set_data(binarized_locres_data)
    #     mout.voxel_size = binarized_mask_obj.voxel_size
    #     mout.close()

    def get_views(self, map_name, root_data=None, data_type=None):
        """
            Based on the information produce views and save to json file

        :param root_data: root data from input json file
        :param map_name: a string of input map nanme
        :param data_type: a string of view type
        """

        if root_data:
            # Model coloured based on local resolution
            num_model = len(root_data)
            for i in range(num_model):
                output_json = {}
                json_dict = {}
                cur_model = root_data[str(i)]
                keylist = list(cur_model.keys())
                colors = None
                residues = None
                values = None
                model_name = None
                for key in keylist:
                    if key != 'name':
                        colors = cur_model[key]['color']
                        residues = cur_model[key]['residue']
                        values = cur_model[key]['localResolution']
                    else:
                        model_name = cur_model[key]
                min_middle_max = {}
                min_value = min(values)
                max_value = max(values)
                real_middle = (min_value + max_value) / 2
                difference = [abs(value - real_middle) for value in values]
                middle_index = difference.index(min(difference))
                middle_value = values[middle_index]
                min_value, middle_value, max_value = (min(values), middle_value, max(values))
                min_index = values.index(min_value)
                # median_index = values.index(median_value)
                max_index = values.index(max_value)
                min_colour = colors[min_index]
                middle_colour = colors[middle_index]
                max_colour = colors[max_index]
                min_middle_max[min_value] = min_colour
                min_middle_max[middle_value] = middle_colour
                min_middle_max[max_value] = max_colour
                chimerax_file_name = self.write_residue_cxc(colors, residues, map_name, model_name, data_type, min_middle_max)
                out = self.run_chimerax(chimerax_file_name)
                surfaces_dict = self.rescale_view(map_name, model_name, data_type)
                json_dict[model_name] = surfaces_dict
                output_json[f'{data_type}_views'] = json_dict

                output_json_file = f"{map_name}_{model_name}_{data_type.replace('_', '')}.json"
                output_json_fullpath = f'{self.va_dir}/{output_json_file}'
                out_json(output_json, output_json_fullpath)
        else:
            # no model cases
            output_json = {}
            raw_map = f'{self.va_dir}/{map_name[:-4] + "_rawmap.map"}'
            mask_map = f'{self.va_dir}/{map_name}_relion/mask/{map_name}_mask.mrc'
            map_processor = MapProcessor()
            binarized_mask_map = map_processor.binarized_mask(mask_map, map_name)
            masked_raw_map = map_processor.mask_map(raw_map, binarized_mask_map)
            # masked_raw_predicted_contour = map_processor.predict_contour(masked_raw_map)
            local_resolution_map_glob = glob.glob(f'{self.va_dir}/{map_name}_relion/*_locres.mrc')
            local_resolution_map = local_resolution_map_glob[0] if len(local_resolution_map_glob) > 0 else None
            chimerax_file_name = self.write_maps_cxc(os.path.basename(masked_raw_map), local_resolution_map, data_type)
            out = self.run_chimerax(chimerax_file_name)
            surfaces_dict = self.rescale_view(os.path.basename(masked_raw_map), None, data_type)
            output_json[f'{data_type}_views'] = surfaces_dict

            output_json_file = f"{map_name}_{data_type.replace('_', '')}.json"
            output_json_fullpath = f'{self.va_dir}/{output_json_file}'
            out_json(output_json, output_json_fullpath)
            # exit()
            #
            # local_resolution_map_glob = glob.glob(f'{self.va_dir}/{map_name}_relion/*_locres.mrc')
            # local_resolution_map = local_resolution_map_glob[0] if len(local_resolution_map_glob) > 0 else None
            # bined_mask = self.binarized_mask(map_name)
            # print(bined_mask)
            # self.binarized_locres(bined_mask, local_resolution_map)
            #
            # output_json = {}
            #
            # local_resolution_map_glob = glob.glob(f'{self.va_dir}/{map_name}_relion/*_locres.mrc')
            # local_resolution_map = local_resolution_map_glob[0] if len(local_resolution_map_glob) > 0 else None
            # chimerax_file_name = self.write_maps_cxc(map_name, local_resolution_map, data_type)
            # out = self.run_chimerax(chimerax_file_name)
            # surfaces_dict = self.rescale_view(map_name,None, data_type)
            # output_json[f'{data_type}_views'] = surfaces_dict
            #
            # output_json_file = f"{map_name}_{data_type.replace('_', '')}.json"
            # output_json_fullpath = f'{self.va_dir}/{output_json_file}'
            # out_json(output_json, output_json_fullpath)
            #



