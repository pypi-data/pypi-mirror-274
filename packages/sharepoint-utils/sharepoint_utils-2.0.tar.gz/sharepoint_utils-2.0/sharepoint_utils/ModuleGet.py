#########################################################################################

def get_folder_url(ctx, document_library_relative_url: str):
    """
    Function to return a list of URLs of folders present in a given path in SharePoint.

    Parameters:
        - ctx: SharePoint context object.
        - document_library_relative_url (str): Relative URL of the document library.

    Returns:
        - List[str]: List of URLs of folders present in the given path.
    """
    # Getting the root folder of the document library
    root_folder = ctx.web.get_folder_by_server_relative_path(document_library_relative_url)
    ctx.load(root_folder, ["Folders"])
    ctx.execute_query()

    # Extracting the paths of Level 1 folders within the root folder
    folder_urls = [f'{document_library_relative_url}/{folder.name}' for folder in root_folder.folders]
    
    return folder_urls

# Example usage:
# Assuming you have ctx already defined
# ctx = get_sharepoint_context()  # Get SharePoint context

#########################################################################################

def get_file_path(ctx, subfolder_urls_files: str):
    """
    Function to return a list of paths of files present in a given subfolder in SharePoint.

    Parameters:
        - ctx: SharePoint context object.
        - subfolder_urls_files (str): Relative URL of the subfolder containing files.

    Returns:
        - List[str]: List of paths of files present in the given subfolder.
    """
    # Get the root folder of the Level 2 folder
    root_folder_level2 = ctx.web.get_folder_by_server_relative_path(subfolder_urls_files)
    ctx.load(root_folder_level2, ["Files"])
    ctx.execute_query()

    # Initialize a list to store file paths
    file_paths = []

    # Iterate over files within the Level 2 folder
    for file in root_folder_level2.files:
        # Append the path of each file to the list
        file_paths.append(f'{subfolder_urls_files}/{file.name}')

    return file_paths

# Example usage:
# Assuming you have ctx already defined
# ctx = get_sharepoint_context()  # Get SharePoint context
#########################################################################################
