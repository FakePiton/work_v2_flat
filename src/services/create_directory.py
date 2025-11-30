import pandas as pd
import os

class CreateDirectoryService:
    def read(self, file_path: str) -> pd.DataFrame:
        return pd.read_excel(file_path)

    def create_base_dir(
        self, path_dir: str,
        name_base_dir: str,
    ) -> str:
        folder_path = os.path.join(path_dir, name_base_dir)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path

    def create_dirs(
        self,
        file_path: str,
        path_dir: str,
        name_base_dir: str,
    ) -> None:
        df = self.read(file_path)

        first_col = df.iloc[:, 0]
        path_base = self.create_base_dir(path_dir, name_base_dir)
        for name in first_col:
            if name:
                folder_path = os.path.join(path_base, name)
                os.makedirs(folder_path, exist_ok=True)
