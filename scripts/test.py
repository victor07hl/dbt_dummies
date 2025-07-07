from model_lineage import Lineage
from graphviz_renderer import GraphvizRenderer
from exporter import Exporter

model = 'gold_ticket_metrics.sql'
modela_lineage = Lineage(model=model)

modela_location = modela_lineage.get_model_location()

upstream_dict = modela_lineage.get_upstream_refs(modela_location,5,'upstream')
downstream_dict = modela_lineage.get_downstream_refs(model,5,'downstream')
full_lineage ={}
full_lineage.update(downstream_dict)
full_lineage.update(upstream_dict)

df_ = Exporter.lineage_to_df(base_model = model,
                             lineage_dict = full_lineage,
                             )


df_['depth'] = df_['depth'].astype(int)

# Sort the DataFrame by 'base_model' and 'depth'
df_.sort_values(['base_model', 'mode', 'depth'], inplace=True)
#print(df_.head())
df_.to_csv('up_down_list.csv',index=False)

#generate the graphiz themplate 
renderer = GraphvizRenderer(lineage_data=full_lineage)
#print(downstream_dict)
renderer.generate_png(f'{model.replace('.sql','')}_lineage.png')


