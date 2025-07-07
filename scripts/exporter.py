import pandas as pd

class Exporter():
    def __init__(self):
        pass

    @staticmethod
    def lineage_to_df(base_model: str, lineage_dict: dict) -> pd.DataFrame:
        """
        Convert the lineage dictionary into a DataFrame, including all items from the lineage_dict.

        Args:
            base_model (str): The name of the base model to search for in the dictionary.
            lineage_dict (dict): The lineage dictionary containing model dependencies.

        Returns:
            pd.DataFrame: A DataFrame containing the lineage information with columns:
                        ['base_model', 'up_down_model', 'antecesor', 'depth', 'mode'].
        """

        # Initialize the result list
        result = []

        # Recursive function to traverse the lineage dictionary
        def traverse(model, antecesor, depth, mode):
            if model not in lineage_dict:
                return

            # Extract the path, sources, and mode from the dictionary
            model_path, sources, current_mode = lineage_dict[model]

            # Avoid adding rows where the model is its own antecesor
            if antecesor is not None and model != antecesor:
                result.append({
                    'base_model': base_model,
                    'up_down_model': model,
                    'antecesor': antecesor,
                    'depth': depth,
                    'mode': mode
                })

            # Recursively traverse the sources for upstream lineage
            if mode == "upstream":
                for source in sources:
                    traverse(source, model, depth + 1, mode)

            # Recursively traverse the dependents for downstream lineage
            elif mode == "downstream":
                for dependent in lineage_dict.keys():
                    _, dependent_sources, _ = lineage_dict[dependent]
                    if model in dependent_sources:
                        traverse(dependent, model, depth + 1, mode)

        # Start the traversal for upstream lineage
        base_model = base_model.replace('.sql', '')
        traverse(base_model, None, 0, "upstream")  # Start depth at 0 for the base model

        # Start the traversal for downstream lineage
        traverse(base_model, None, 0, "downstream")  # Start depth at 0 for the base model

        # Convert the result list to a DataFrame
        return pd.DataFrame(result, columns=['base_model', 'up_down_model', 'antecesor', 'depth', 'mode'])