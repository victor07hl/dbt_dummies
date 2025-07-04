import os 
import re 

class Lineage():
    def __init__(self, model: str, dbt_folder: str = '../nyc_parking_violations/models'):
        self.model = model
        self.dbt_folder = dbt_folder

    def get_model_location(self) -> str:
        """
        Search for the SQL script with the name defined in self.model within the self.dbt_folder.
        The search is recursive and stops when the model is found.

        Returns:
            str: The location (path) of the model if found, otherwise raises a FileNotFoundError.
        """
        for root, _, files in os.walk(self.dbt_folder):
            for file in files:
                model_name = self.model if self.model.endswith('.sql') else self.model + '.sql'
                if file == model_name:
                    return os.path.join(root, file)
        raise FileNotFoundError(f"Model '{self.model}' not found in '{self.dbt_folder}'.")
    
    def get_ref(self, model_location: str) -> dict:
        """
        Open the SQL file at the given model_location and search for all occurrences of the keyword 'ref'.
        Extract the sources or table references and return them in a structured dictionary.

        Args:
            model_location (str): The path to the SQL file.

        Returns:
            dict: A dictionary containing the model name, its path, and a list of sources (references).
        """
        sources = []
        with open(model_location, 'r') as file:
            content = file.read()
            # Use regex to find all occurrences of ref('...') or ref("...")
            matches = re.findall(r"ref\(['\"](.*?)['\"]\)", content)
            sources.extend(matches)
        model = model_location.split('/')[-1].replace('.sql','')

        return {
                model: {
                'path': model_location,
                'sources': sources
            }
        }
    
    def get_upstream_refs(self, model_location: str, depth: int) -> dict:
        """
            Recursively retrieve sources for a model up to a specified depth.

            Args:
                model_location (str): The path of the initial model.
                depth (int): The maximum depth for recursive source retrieval.

            Returns:
                dict: A dictionary containing the model hierarchy in the format:
                    {"model_name": (model_path, [src1, src2, ...])}.
        """
        if depth <= 0:
            return {}

        # Get the references for the current model
        model_refs = self.get_ref(model_location)
        model_name = list(model_refs.keys())[0]
        model_path = model_refs[model_name]['path']
        sources = model_refs[model_name]['sources']

        # Initialize the result dictionary with the current model
        result = {model_name: (model_path, sources)}

        # If no sources are found, return the current model's references
        if not sources:
            return result

        # Recursively get sources for each source in the current model
        for source in sources:
            try:
                source_location = Lineage(source, self.dbt_folder).get_model_location()
                # Merge the recursive results into the main result dictionary
                result.update(self.get_upstream_refs(source_location, depth - 1))
            except FileNotFoundError:
                # If a source is not found, add it with a None path and empty sources
                result[source] = (None, [])

        return result
    
