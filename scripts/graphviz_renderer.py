class GraphvizRenderer:
    def __init__(self, lineage_data: dict):
        """
        Initialize the renderer with lineage data.

        Args:
            lineage_data (dict): The recursive result from get_recursive_refs.
        """
        self.lineage_data = lineage_data

    def to_graphviz(self) -> str:
        """
            Convert the lineage data into a Graphviz DOT format with the specified template.

        Returns:
            str: A string representing the Graphviz DOT template.
        """
        graph_lines = [
            'digraph G {',
            '    // Graph attributes',
            '    rankdir=LR;',
            '    label="NYC Parking Violations - Data Lineage";',
            '    labelloc=top;',
            '    fontsize=20;',
            '    splines=true;',
            '',
            '    // Node styles',
            '    node [shape=box, style=filled, color=lightblue, fontname="Helvetica"];',
            ''
        ]

        # Define nodes
        graph_lines.append('    // Define nodes')
        for model, (path, _, __), in self.lineage_data.items():
            graph_lines.append(f'    "{model}" [label="{model}"];')

        graph_lines.append('')

        # Define edges
        graph_lines.append('    // Define edges')
        for model, (_, sources, __) in self.lineage_data.items():
            for source in sources:
                graph_lines.append(f'    "{source}" -> "{model}" [arrowhead=None];')

        graph_lines.append('}')
        return "\n".join(graph_lines)