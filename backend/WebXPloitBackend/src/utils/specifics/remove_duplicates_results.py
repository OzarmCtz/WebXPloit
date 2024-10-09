# cython: language_level=3


from pathlib import Path
import src.utils.generics.generic as UtilsGenerics
from config.params import ConfigConst


class RemoveDuplicatesLinesInResult:
    def __init__(self):
        self.logger = UtilsGenerics.setup_logging(
            logger_name=f"{ConfigConst.LoggingConfig.LOGGER_OUTPUT_NAME}",
            log_file=ConfigConst.LoggingConfig.OUTPUT_FILE_PATH,
        )

        self.logger.info(f"RemoveDuplicatesLinesInResult : Started .")

        [
            self.remove_duplicates_from_file(file_path)
            for file_path in ConfigConst.get_all_file_paths()
        ]
        self.logger.info(f"RemoveDuplicatesLinesInResult : Finished .")
        print(
            f"[{UtilsGenerics.ret_hour()}] RemoveDuplicatesLinesInResult Process Done ."
        )

    def remove_duplicates_from_file(self, file_path: Path):
        try:
            with file_path.open("r") as file:
                lines = file.readlines()

            unique_lines = {}
            for line in lines:
                # Découper la ligne au dernier '|'
                parts = line.rsplit("|", 1)
                line_without_date = parts[0]

                # Ignorer la ligne si 'Checked : True' est présent
                if "Checked : True" in line_without_date:
                    continue

                # Ajouter la ligne à unique_lines si elle n'est pas déjà présente
                if line_without_date not in unique_lines:
                    unique_lines[line_without_date] = line

            # Écrire les lignes uniques dans le fichier
            with file_path.open("w", encoding="utf-8") as file:
                file.writelines(unique_lines.values())

            self.logger.info(f"File alerady cleaned : {file_path}")
        except IOError as e:
            self.logger.error(
                f"An error was occured when cleaned duplicates data in : {file_path}: {e}"
            )
