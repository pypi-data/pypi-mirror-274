from __future__ import absolute_import
from itertools import cycle
from .base_shape import BaseShape, EmptyShape
from frame_stamp.utils.exceptions import PresetError
from frame_stamp.utils import cached_result, rotate_point
from PIL import Image
import logging

logger = logging.getLogger(__name__)


class TileShape(BaseShape):
    shape_name = 'tile'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._shapes = self._init_shapes(**kwargs)
        # self._shape_rotate = super().rotate

    @property
    def rotate(self):
        return 0

    def _init_shapes(self, **kwargs):
        from frame_stamp.shape import get_shape_class

        # size = self.source_image.size
        shape_list = self._data.get('shapes')
        if not shape_list:
            return []
        coords = self._create_positions_grid(shape_list, self.source_image.size)
        shapes = []
        shape_generator = cycle(shape_list)
        for i, tile in enumerate(coords):
            shape_config = next(shape_generator)
            # print('Shape:', shape_config)
            if not shape_config:
                continue
            shape_type = shape_config.get('type')
            if shape_type is None:
                raise PresetError('Shape type not defined in template element: {}'.format(shape_config))
            # parent_shape_config = {**shape_config, **tile}
            # print(parent_shape_config)
            parent = EmptyShape(tile, self.context)#, local_context=tile)
            shape_config['parent'] = parent
            shape_cls = get_shape_class(shape_type)
            shape: BaseShape = shape_cls(shape_config, self.context, **kwargs)
            # w, h = shape.width, shape.height
            # x = x + w + self.horizontal_spacing
            # y = y + h
            # local_context = {}
            # shape_generator.send()
            # shape_config['parent'] = EmptyShape(cells[i], self.context, local_context=lc)
            # kwargs['local_context'] = local_context

            shapes.append(shape)
            if shape.id is not None:
                if shape.id in self.scope:
                    raise PresetError('Duplicate shape ID: {}'.format(shape.id))
            self.add_shape(shape)
        return shapes

    def _iter_shape_configs(self):
        from itertools import repeat
        shape_list = self._data.get('shapes')
        if not shape_list:
            raise StopIteration
        return repeat(shape_list)

    def _create_positions_grid(self, shape_list, canvas_size, **kwargs):
        """
        [
            {shape_config, index, row, col}
        ]

        :param shape_list:
        :param canvas_size:
        :param kwargs:
        :return:
        """
        from frame_stamp.shape import get_shape_class

        tile_overlap = 1
        center_x, center_y = self.x % canvas_size[0], self.y % canvas_size[1]
        print(f"{center_x=}, {center_y=}")
        shapes = []
        for shape_config in shape_list:
            if not shape_config:
                raise ValueError('Shape cannot be empty')
            shape_type = shape_config.get('type')
            shape_cls = get_shape_class(shape_type)
            shape: BaseShape = shape_cls(shape_config, self.context, **kwargs)
            shapes.append(shape)
        # create 
        cell_width = max([sh.width for sh in shapes])
        print(f"{cell_width=}")
        cell_height = max([sh.height for sh in shapes])
        print(f"{cell_height=}")
        max_shape_dim = max([cell_height, cell_width])
        print(f"{max_shape_dim=}")
        # max_canvas_dim = max(canvas_size)
        # print(f"{max_canvas_dim=}")
        max_x_value = canvas_size[0] + (max_shape_dim*tile_overlap)
        min_x_value = -(max_shape_dim*tile_overlap)
        max_y_value = canvas_size[1] + (max_shape_dim*tile_overlap)
        min_y_value = -(max_shape_dim*tile_overlap)
        # print(f"{max_coord_value=}")
        offset_x = cell_width+self.horizontal_spacing
        print(f"{offset_x=}")
        offset_y = cell_height+self.vertical_spacing
        print(f"{offset_y=}")
        # start_x = center_x - (offset_x * (canvas_size[0]//offset_x))
        start_x = 0 - (center_x % cell_width) - offset_x
        print(f"{start_x=}")
        # start_y = center_y - (offset_y * (max_coord_value//(offset_y)))
        start_y = 0 - (center_y % cell_height) - offset_y
        print(f"{start_y=}")
        max_rows = self.max_rows or canvas_size[0]//offset_x
        print(f"{max_rows=}")
        max_columns = self.max_columns or canvas_size[1]//offset_y
        print(f"{max_columns=}")

        x, y = start_x, start_y
        index = 0
        col = 0
        row = 0
        tiles = []
        rot = self._eval_parameter('rotate', default=0)
        rot_pivot = (center_x, center_y)
        while index < self.tile_count_limit:
            index += 1
            if rot:
                _x, _y = rotate_point((x, y), rot, origin=rot_pivot)
                print('COORDS', _x, _y)
            else:
                _x, _y = x, y
            if not any([_x > max_x_value,
                        _x < min_x_value,
                        _y > max_y_value,
                        _y < min_y_value]):
                tiles.append(dict(
                    x=_x,
                    y=_y,
                    rotate=rot,
                    # rotate_pivot=rot_pivot,
                    column=col,
                    row=row,
                    index=index,
                    width=cell_width,
                    height=cell_height
                ))
            x += offset_x
            col += 1
            if x > max_x_value or col+1 > max_columns:
                col = 0
                row += 1
                x = start_x
                y += offset_y
            if y > max_y_value or row > max_rows:
                break
        return tiles

    def get_shapes(self):
        return self._shapes

    def draw_shape(self, size, **kwargs):
        canvas = self._get_canvas(size)
        shapes = self.get_shapes()
        if shapes:
            for shape in shapes:
                # if shape._local_context['row'] == 1:
                #     print(shape._data, shape.y, shape.y_draw)
                overlay = shape.render(size)
                canvas = Image.alpha_composite(canvas, overlay)
        return canvas

    @property
    @cached_result
    def vertical_spacing(self):
        return self._eval_parameter('vertical_spacing', default=0)

    @property
    @cached_result
    def horizontal_spacing(self):
        return self._eval_parameter('horizontal_spacing', default=0)

    @property
    @cached_result
    def max_rows(self):
        return self._eval_parameter('max_rows', default=None)

    @property
    @cached_result
    def max_columns(self):
        return self._eval_parameter('max_columns', default=None)

    @property
    @cached_result
    def row_offset(self):
        return self._eval_parameter('row_offset', default=0)

    @property
    @cached_result
    def column_offset(self):
        return self._eval_parameter('column_offset', default=0)

    @property
    @cached_result
    def tile_count_limit(self):
        return self._eval_parameter('tile_count_limit', default=5000)
