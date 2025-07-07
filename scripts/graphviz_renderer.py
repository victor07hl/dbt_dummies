import graphviz

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
    
    def generate_png(self, output_filename: str) -> None:
        """
        Generate a PNG image from the lineage data.

        Args:
            output_filename (str): The name of the final PNG image file (without extension).
        """
        # Convert lineage data to Graphviz DOT format
        dot_content = self.to_graphviz()

        # Create a Graphviz object and render the PNG image
        graph = graphviz.Source(dot_content)
        graph.format = 'png'
        graph.render(output_filename, cleanup=True)

        print(f"PNG image generated: {output_filename}.png")