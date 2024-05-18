# Author: Simon Blanke
# Email: simon.blanke@yahoo.com
# License: MIT License


from typing import Union


class SearchSpacePruningLayer:
    def __init__(self):
        super().__init__()

    def run_search_space_pruining(self, margin: Union[dict, int, float] = 0.1):
        margin = self.c_layer_setup["margin"]

        if isinstance(margin, dict):
            margin_d = {}

            for key in self.s_space.c_search_space.keys():
                values = self.s_space.c_search_space[key]
                margin_1d = margin[key]

                if isinstance(margin_1d, float):
                    margin_d[key] = int(margin_1d * len(values))
                elif isinstance(margin_1d, int):
                    margin_d[key] = margin_1d
                else:
                    raise ValueError("1")
        else:
            margin_1d = margin
            if isinstance(margin, float):
                margin_d = {}
                for key in self.s_space.c_search_space.keys():
                    values = self.s_space.c_search_space[key]
                    margin_d[key] = int(margin_1d * len(values))
            elif isinstance(margin, int):
                margin_d = {}
                for key in self.search_space.keys():
                    margin_d[key] = margin_1d
            else:
                raise ValueError("2")

        pruned_search_space = {}
        pruned_search_space_positions = {}

        for key in self.s_space.c_search_space.keys():
            best_value = self.best_para[key]
            values = self.s_space.c_search_space[key]

            idx = values.index(best_value)
            dim_margin = margin_d[key]

            lower = idx - dim_margin
            upper = idx + dim_margin

            if lower < 0:
                lower = 0
            if upper > len(values) - 1:
                upper = len(values) - 1

            pruned_search_space[key] = values[lower:upper]
            pruned_search_space_positions[key] = range(lower, upper)

        self.s_space.c_search_space = pruned_search_space
        self.s_space.positions = pruned_search_space_positions
