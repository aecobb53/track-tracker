import os
import json
from datetime import datetime, timezone
from models import ContextSingleton


class BaseFileHandler:
    def __init__(self, file_name: str, file_directory: str = None, skip_load: bool = False, *args, **kwargs):
        self.context = ContextSingleton()
        self.base_file_directory = '/db'
        self.file_directory = file_directory
        self.file_name = file_name
        self._ensure_directory()

        if skip_load:
            # self.metadata = {
            #     'last_updated': None,
            # }
            self.metadata = {}
        else:
            self._saved_content = None
            self.load_file()
        """
        content is the internal data content this will have pydantic
        saved_content is exclusively JSON 
        """

        """
        To keep versioning straight, the object holds the expected last_updated time in self.metadata
        The file can be inspected to find the files last_updated time
        If there is a mismatch, saves should fail
        """

    @property
    def file_path(self):
        """
        Form the path for the file
        """
        if self.file_directory:
            return os.path.join(self.base_file_directory, self.file_directory, self.file_name)
        else:
            return os.path.join(self.base_file_directory, self.file_name)

    @property
    def file_directory_path(self):
        """
        Form the path for the file
        """
        if self.file_directory:
            return os.path.join(self.base_file_directory, self.file_directory)
        else:
            return os.path.join(self.base_file_directory)

    def inspect(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                content = json.load(f)
            return content['metadata']
        else:
            return None

    def _ensure_directory(self):
        """
        Ensure the directory exists for the file
        """
        os.makedirs(self.file_directory_path, exist_ok=True)

    def save_file(self):
        """
        Save the file to the file system
        saved_content is only allowed to be json content and is reset after save
        This allows it to be set ahead of time for a save
        """
        self._ensure_directory()
        metadata = self.inspect()
        if metadata and metadata['last_updated'] != self.metadata['last_updated']:
            self.context.logger.error(f"File {self.file_path} has been modified since last read. Please reload the file.")
            raise ValueError(f"File {self.file_path} has been modified since last read. Please reload the file.")
        with open(self.file_path, 'w') as f:
            self.metadata['last_updated'] = datetime.now(timezone.utc).isoformat()
            content = {
                'metadata': self.metadata,
                'content': self._saved_content,
            }
            f.write(json.dumps(content, indent=4))

    def load_file(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r') as f:
                content = json.load(f)
            self.metadata = content.get('metadata', {})
            self._saved_content = content.get('content', {})
        else:
            self.context.logger.error(f"File not found at {self.file_path}")
            raise FileNotFoundError(f"File not found at {self.file_path}")

# # Example usage
# print('EXAMPLE USAGE')
# file_handler = BaseFileHandler(file_name="example.json", file_directory="test_dir")
# file_handler.save_file({"key": "value2"})
# content = file_handler.load_file()
# print(content)
