import os
import zipfile
from bs4 import BeautifulSoup


class DiskFileManager:
    @staticmethod
    def navigate_to_folder(root_folder, folder_name):
        folder_path = os.path.join(root_folder, folder_name)
        if os.path.isdir(folder_path):
            root_folder = folder_path
        else:
            print(f"Folder not found: {folder_name}")
        return root_folder

    @staticmethod
    def change_html_content(root_folder, new_name):
        index_file_path = os.path.join(root_folder, "index.html")
        if os.path.isfile(index_file_path):
            with open(index_file_path, "r") as file:
                content = file.read()

            soup = BeautifulSoup(content, "html.parser")
            title_tag = soup.find("title")
            heading_tag = soup.find("h1", class_="heading")

            if title_tag:
                title_tag.string = new_name
            else:
                title_tag = soup.new_tag("title")
                title_tag.string = new_name
                soup.head.append(title_tag)

            if heading_tag:
                heading_tag.string = new_name
            else:
                heading_tag = soup.new_tag("h1", class_="heading")
                heading_tag.string = new_name
                soup.body.append(heading_tag)

            with open(index_file_path, "w") as file:
                file.write(soup.prettify())

            print("HTML content updated successfully.")
        else:
            print("index.html file not found.")

    @staticmethod
    def zip_folder_contents(root_folder, zip_path):
        if not os.path.exists(root_folder):
            print(f"The provided folder path {root_folder} does not exist.")
            return

        if not os.path.exists(os.path.dirname(zip_path)):
            print(
                f"The parent folder of the provided zip path {zip_path} does not exist."
            )
            return

        if os.path.exists(zip_path):
            os.remove(zip_path)

        with zipfile.ZipFile(zip_path, "w") as zipf:
            for foldername, subfolders, filenames in os.walk(root_folder):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    zipf.write(file_path, os.path.relpath(file_path, root_folder))

        print(
            f"Successfully zipped the contents of {root_folder} and saved to {zip_path}"
        )
