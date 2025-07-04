from model_lineage import Lineage
from graphviz_renderer import GraphvizRenderer

modela_lineage = Lineage(model='gold_ticket_metrics.sql')

modela_location = modela_lineage.get_model_location()

lineage_dict = modela_lineage.get_recursive_refs(modela_location,5)

#generate the graphiz themplate 
renderer = GraphvizRenderer(lineage_data=lineage_dict)
print(lineage_dict)
#print(renderer.to_graphviz())


