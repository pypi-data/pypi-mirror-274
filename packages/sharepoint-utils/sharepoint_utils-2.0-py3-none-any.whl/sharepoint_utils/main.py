#########################################################################################
# Import necessary modules for authentication and working with SharePoint files
from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from io import StringIO

#########################################################################################

def connect_to_sharepoint(username, password, site_address):
    """
    This function connects to a SharePoint site using the provided username, password, and site address.
    
    :param username: The username to authenticate with SharePoint.
    :param password: The password to authenticate with SharePoint.
    :param site_address: The address of the SharePoint site.
    :return: ClientContext object if successful, None otherwise.
    """
    # Define SharePoint base URL
    sharepoint_base_url = site_address
    # Specify SharePoint user credentials
    sharepoint_user = username
    sharepoint_password = password
    # Authenticate with SharePoint
    ctx_auth = AuthenticationContext(sharepoint_base_url)
    if ctx_auth.acquire_token_for_user(sharepoint_user, sharepoint_password):
        ctx = ClientContext(sharepoint_base_url, ctx_auth)
        web = ctx.web
        ctx.load(web)
        ctx.execute_query()
        # Print a message indicating successful connection to SharePoint along with the web title
        print('Connected to SharePoint: ', web.properties['Title'])
        return ctx
    else:
        print("Failed to authenticate with SharePoint.")
        return None

#########################################################################################

def upload_dataframe_as_csv(ctx, folder_path, dataframe, file_name):
    """
    This function uploads a pandas DataFrame to a SharePoint folder as a CSV file.

    Parameters:
    ctx (ClientContext): The SharePoint ClientContext.
    folder_path (str): The server-relative URL of the SharePoint folder where the file will be uploaded.
    dataframe (DataFrame): The pandas DataFrame to be uploaded.
    file_name (str): The name of the file to be created.
    """
    try:
        # Get the SharePoint folder
        folder = ctx.web.get_folder_by_server_relative_url(folder_path).select(["Exists"]).get().execute_query()
        
        # Convert the DataFrame to a CSV string
        csv_buffer = StringIO()
        dataframe.to_csv(csv_buffer, index=False)
        file_content = csv_buffer.getvalue().encode('utf-8-sig')

        # Upload the file to the folder
        file = folder.upload_file(file_name, file_content).execute_query()
        print(f"File has been uploaded into: {file.serverRelativeUrl}")
    
    except Exception as e:
        print(f"An error occurred while uploading the file: {str(e)}")

#########################################################################################

def copy_files_within_folders(ctx, file_path, upload_to_path):
    """
    Copies files from one location to another using SharePoint client context.

    Args:
    ctx: SharePoint client context object.
    file_path: List of file paths to be copied. | Type: List
    upload_to_path: Path where files will be copied. | Type: String

    Returns:
    None
    """

    for files in file_path:
        try:
            # Get the file from the source location
            file_from = ctx.web.get_file_by_server_relative_url(files)
            
            # Get the destination folder
            folder_to = ctx.web.get_folder_by_server_relative_url(upload_to_path)
            # Alternatively, you can specify the destination folder as a string like this:
            # folder_to = "Shared Documents/archive/2002/02"
            
            # Copy the file to the destination folder
            file_from.copyto(folder_to, True).execute_query()
            
            # Print a message indicating that the file has been copied
            print("{0} copied into: '{1}'".format(file_from, upload_to_path))
        except Exception as e:
            print("Error copying file {0}: {1}".format(files, e))

#########################################################################################
