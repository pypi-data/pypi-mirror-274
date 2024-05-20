import os
import inspect, importlib, time, re


class RInitiate:

    def __init__(self):
        try:
            from RTS_WebUIBuilder import rtswuib_cache
            ws = None
            while ws is None:
                ws = rtswuib_cache.MAIN_WEBSERVER
                if ws is None:
                    time.sleep(1)  # Wait for 1 second before checking again
                else:
                    modul_pfad = os.path.dirname(os.path.abspath(__file__))
                    ziel_pfad = os.path.normpath(os.path.join(modul_pfad, "srcFolder"))
                    ws.enableSourceRoute(ziel_pfad)
        except ImportError:
            print("⚠️  You may not remove the dependency module 'RTS_WebUIBuilder'.")
            return
    
        self.topics:list = []
        self.subtopics:list = []
        self.initiator:list = []
        caller_frame = inspect.stack()[1]
        caller_module = inspect.getmodule(caller_frame[0])
        module_file_path = caller_module.__file__
        
        # Get the root folder of the module
        module_root_folder = os.path.dirname(module_file_path)
        
        if os.path.basename(module_root_folder) != 'docs':
            docs_folder_path = os.path.join(module_root_folder, 'docs')
        else:
            docs_folder_path = module_root_folder
        if os.path.exists(docs_folder_path):
            self.create_topic_subtopic_structure(docs_folder_path)
        else:
            print("No 'docs' folder exists in the module root folder.")

    def create_topic_subtopic_structure(self, docs_folder_path):
        
        # Get the root folder of the module
        module_root_folder = os.path.dirname(os.path.abspath(__file__))
    
        # Initialize the 'subtopics' list and 'initiator' list
        self.subtopics = []
        self.initiator = []
    
        # Iterate over the topics in the 'docs' folder
        for topic in os.listdir(docs_folder_path):
            display_topic = re.sub(r'^[a-z]--', '', topic)
            topic_path = os.path.join(docs_folder_path, topic)
            if os.path.isdir(topic_path):
                # Get all .py files in the topic folder
                py_files = [file for file in os.listdir(topic_path) if file.endswith('.py')]
                # Check if there is exactly one .py file
                if len(py_files) == 1:
                    # Add the topic to the 'topics' list
                    self.topics.append((os.path.splitext(py_files[0])[0], '/' + display_topic))
                    # Store the module path and function name
                    module_path = os.path.join(topic_path, os.path.splitext(py_files[0])[0])
                    try:
                        # Versuchen Sie, den relativen Pfad zu berechnen
                        module_path = os.path.relpath(module_path, module_root_folder).replace(os.sep, '.')
                    except ValueError:
                        # Wenn sich die Pfade auf unterschiedlichen Laufwerken befinden, verwenden Sie den absoluten Pfad
                        # und ersetzen Sie die Pfadtrennzeichen durch Punkte
                        module_path = module_path.replace(os.sep, '.')
                    if module_path.startswith('...'):
                        module_path = module_path[3:]
                    function_name = os.path.splitext(py_files[0])[0]  # Get the function name from the file name
                    self.initiator.append((module_path, function_name))
                    # Initialize the 'topic_subtopics' list
                    topic_subtopics = []
                    # Iterate over the subtopics in the topic folder
                    for subtopic in os.listdir(topic_path):
                        display_stopic = re.sub(r'^[a-z]--', '', subtopic)
                        subtopic_path = os.path.join(topic_path, subtopic)
                        if os.path.isdir(subtopic_path):
                            # Get all .py files in the subtopic folder
                            subtopic_py_files = [file for file in os.listdir(subtopic_path) if file.endswith('.py')]
                            # Check if there is exactly one .py file
                            if len(subtopic_py_files) == 1:
                                # Add the subtopic to the 'topic_subtopics' list
                                topic_subtopics.append((os.path.splitext(subtopic_py_files[0])[0], '/' + display_stopic))
                                # Store the module path and function name
                                subtopic_module_path = os.path.join(subtopic_path, os.path.splitext(subtopic_py_files[0])[0])
                                subtopic_module_path = os.path.relpath(subtopic_module_path, module_root_folder).replace(os.sep, '.')
                                if subtopic_module_path.startswith('...'):
                                    subtopic_module_path = subtopic_module_path[3:]
                                subtopic_function_name = os.path.splitext(subtopic_py_files[0])[0]  # Get the function name from the file name
                                self.initiator.append((subtopic_module_path, subtopic_function_name))
                    # Add the 'topic_subtopics' list to the 'subtopics' list
                    self.subtopics.append(topic_subtopics)
            print("Topics: ", self.topics)
            print("Subtopics: ", self.subtopics)
    
    def execute_initiator(self):
        for module_path, function_name in self.initiator:
            #try:
                # Import the module
                module = importlib.import_module(module_path)
                # Get the function
                function = getattr(module, function_name)
                # Call the function
                function()
            #except ImportError as e:
            #    print(f"Failed to import module {module_path}. Error: ", e)
            #    return
            #except AttributeError as e:
            #    print(f"Failed to find function {function_name} in module {module_path}. Error: ", e)
            #    return