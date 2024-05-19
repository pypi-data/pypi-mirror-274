class ParcatsSankeyPlot:
    def __init__(self, df, columns, chart='sankey', w=1200, h=800):
        self.df = df
        self.columns = columns
        self.chart = chart
        self.w = w
        self.h = h

    import sys

    def import_libraries():
        if 'plotly.graph_objects' not in sys.modules:
            print("Importing plotly.graph_objects...")
            import plotly.graph_objects as go
        else:
            print("plotly.graph_objects is already imported.")

        if 'random' not in sys.modules:
            print("Importing random...")
            import random
        else:
            print("random is already imported.")

    import_libraries()

    def create_nodes(self):
        dict_of_nodes = {}
        for col in self.columns:
            dict_of_nodes[col] = self.df[col].unique().tolist()
        return dict_of_nodes

    def create_node_labels(self):
        dict = self.create_nodes()
        node_labels = []
        for key, val in dict.items():
            for i in val:
                node_labels.append(str(key) + ':' + str(i))
        return node_labels

    def label_to_index(self, node_labels):
        label_map = {label: i for i, label in enumerate(node_labels)}
        return label_map

    def get_label_index(self, labels_index, col, val):
        key = str(col) + ':' + str(val)
        return labels_index[key]

    def get_keys_by_value(self, dictionary, value):
        for key, val in dictionary.items():
            if val == value:
                return key

    def create_source_target(self):
        dict_of_nodes = self.create_nodes()
        node_labels = self.create_node_labels()
        labels_index = self.label_to_index(node_labels)
        source_target_dict = {}
        keys = list(dict_of_nodes.keys())

        for k in range(len(keys) - 1):
            col1 = keys[k]
            col2 = keys[k + 1]
            for val1, val2 in zip(self.df[col1], self.df[col2]):
                source = self.get_label_index(labels_index, col1, val1)
                target = self.get_label_index(labels_index, col2, val2)
                link_value = 1
                source_target_dict[(source, target)] = source_target_dict.get((source, target), 0) + link_value

        source_list = []
        target_list = []
        value_list = []
        for key, value in source_target_dict.items():
            source_list.append(key[0])
            target_list.append(key[1])
            value_list.append(value)

        return source_list, target_list, value_list

    def create_labels_colors(self, node_labels):
        node_colors = []
        for label in node_labels:
            node_colors.append(
                f'rgba({random.randint(0, 255)},{random.randint(0, 255)},{random.randint(0, 255)},{0.7})')
        return node_colors

    def create_link_colors(self, source_list, target_list, node_labels, node_colors):
        label_map = self.label_to_index(node_labels)
        link_colors_list = []
        for source, target in zip(source_list, target_list):
            source_label = self.get_keys_by_value(label_map, source)
            target_label = self.get_keys_by_value(label_map, target)

            source_index = node_labels.index(source_label)
            target_index = node_labels.index(target_label)

            source_color = node_colors[source_index]
            target_color = node_colors[target_index]

            color = self.get_intermediate_color(source_color, target_color)
            link_colors_list.append(color)
        return link_colors_list

    def get_intermediate_color(self, color1, color2):
        r1, g1, b1, a1 = map(float, color1[5:-1].split(','))
        r2, g2, b2, a2 = map(float, color2[5:-1].split(','))

        r = (r1 + r2) / 2
        g = (g1 + g2) / 2
        b = (b1 + b2) / 2
        a = (a1 + a2) / 2

        return f'rgba({int(r)},{int(g)},{int(b)},{a})'

    def create_dimension(self):
        dimensions = []

        for col in self.columns:
            dim = go.parcats.Dimension(
                values=self.df[col],
                categoryorder='array',
                label=col,
                categoryarray=self.df[col].unique().tolist()
            )
            dimensions.append(dim)

        return dimensions

    def create_plot(self):
        node_labels = self.create_node_labels()
        node_colors = self.create_labels_colors(node_labels)
        source_list, target_list, value_list = self.create_source_target()
        link_colors = self.create_link_colors(source_list, target_list, node_labels, node_colors)
        dimensions = self.create_dimension()

        if self.chart == 'Sankey':
            fig = go.Figure(data=[go.Sankey(
                node=dict(
                    pad=15,
                    thickness=20,
                    line=dict(color="black", width=0.5),
                    label=node_labels,
                    color=node_colors
                ),
                link=dict(
                    source=source_list,
                    target=target_list,
                    value=value_list,
                    color=link_colors
                ))])

            fig.update_layout(
                width=self.w,
                height=self.h
            )
            return fig

        elif self.chart == 'Parcats':
            parcats_trace = go.Parcats(
                dimensions=dimensions,
                line={
                    'color': value_list,
                    'colorscale': 'Viridis',
                    'shape': 'hspline'
                },
                arrangement='freeform'
            )

            layout = go.Layout(
                title='Parcats Plot',
                font=dict(size=16, color='black'),
                width=self.w,
                height=self.h
            )

            fig = go.Figure(data=[parcats_trace], layout=layout)
            return fig

        elif self.chart == 'raw_variables':
            return node_labels, node_colors, source_list, target_list, value_list, link_colors, dimensions

        else:
            print('Invalid chart. Please choose between "Sankey", "Parcats" or "raw_variables".')
