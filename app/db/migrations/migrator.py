import datetime
from typing import Type
import importlib
import inspect
import os
from dotenv import load_dotenv
from main import supabase

# Load environment variables from .env file
load_dotenv()

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
# Get the list of model directories from the environment variable
model_directories = os.getenv("MODEL_DIRECTORIES", "").split(",")
# Create a directory for the current datetime
datetime_of_beginning = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
# Define the path to the migrations directory
migrations_directory = os.path.join(os.path.dirname(__file__), "app/db/migrations")

current_migration_directory = os.path.join(migrations_directory, datetime_of_beginning)
def class_to_supabase_table_schema(cls: Type) -> dict:
    table_schema = {"name": cls.__name__, "columns": {}}

    for field_name, field in cls.__annotations__.items():
        if field.__name__.lower() != 'classvar':
            column_type = field.__name__.lower()
            default_value = None  # Default value

            # Set default values based on field type
            if column_type == 'str':
                default_value = ""
            elif column_type in ['int', 'float']:
                default_value = 0
            elif column_type == 'bool':
                default_value = False
            elif column_type == 'datetime':
                default_value = datetime.datetime.now()
            elif column_type == 'date':
                default_value = datetime.date.today()
            table_schema["columns"][field_name] = default_value

    return table_schema
if __name__ == "__main__":
    # Iterate through each model directory
    for models_directory in model_directories:
        models_directory = os.path.join(os.path.dirname(__file__), models_directory.strip())
        relative_path = os.path.relpath(models_directory, project_root)
        print(relative_path)
        # List all Python files in the models directory
        model_files = [f for f in os.listdir(models_directory) if f.endswith(".py")]

        # Import each module and look for classes
        for model_file in model_files:
            
            # model_module = f"{relative_path.replace(os.path.sep, '.')}.{model_file[:-3]}"
            model_module = f"{relative_path.replace(os.path.sep, '.')}.{model_file[:-3]}"
            print(model_module)
            module = importlib.import_module(model_module)
            print('Module imported successfully:', model_module)
            # Iterate through the items in the module
            for item_name, item in inspect.getmembers(module):
                print(getattr(item, "is_supabase_table", False))
                # Check if the item is a class and has the attribute is_supabase_table
                if inspect.isclass(item) and getattr(item, "is_supabase_table", False) is True:
                    print(f"Processing: {item.__name__}")
                    # Apply class_to_supabase_table_schema only to classes marked as Supabase tables
                    table_schema = class_to_supabase_table_schema(item)
                    print(f"Processed: {item.__name__}, Table Schema: {table_schema}")
                    supabase.table(table_schema["name"]).upsert(table_schema["columns"], returning='minimal').execute()
                    migration_content = f"supabase.table().upsert({[table_schema]}, returning='minimal').execute()"

                    # Write the migration content to a file
                    migration_file_path = os.path.join(current_migration_directory, f"{item.__name__}_migration.py")
                    with open(migration_file_path, "w") as migration_file:
                        migration_file.write(migration_content)


