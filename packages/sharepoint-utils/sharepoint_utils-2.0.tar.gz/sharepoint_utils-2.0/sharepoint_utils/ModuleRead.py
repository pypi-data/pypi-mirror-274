#########################################################################################

# Import necessary modules for authentication and working with SharePoint files
from office365.sharepoint.files.file import File
from io import BytesIO
import pandas as pd
import io

#########################################################################################

def combine_files_into_dataframe(ctx, folder_url, sheet_name = 0):
    """
    Combine files from a SharePoint folder into a single pandas DataFrame.
    
    :param ctx: ClientContext object authenticated with SharePoint.
    :param folder_url: Server-relative URL of the SharePoint folder containing files.
    :return: Combined pandas DataFrame if successful, None otherwise.
    """
    try:
        # Get the folder object using the provided folder URL
        folder = ctx.web.get_folder_by_server_relative_url(folder_url)
        # Get the collection of files in the folder
        files = folder.files
        # Load the files collection
        ctx.load(files)
        # Execute the query to retrieve the files
        ctx.execute_query()
        # Initialize an empty list to store individual DataFrames
        all_data_frames = []
        # Iterate through each file in the folder
        for file in files:
            # Get the name of the file
            file_name = file.properties["Name"]
            # Open the file and get its content
            response = File.open_binary(ctx, file.serverRelativeUrl)
            file_content = response.content
            # Check the file extension to determine the file type
            if file_name.lower().endswith('.csv'):
                # Read CSV file content into a pandas DataFrame using BytesIO
                df = pd.read_csv(io.BytesIO(file_content))
            elif file_name.lower().endswith('.xlsx'):
                # Read XLSX file content into a pandas DataFrame
                df = pd.read_excel(io.BytesIO(file_content),sheet_name=sheet_name)
            else:
                # Skip files with unsupported extensions
                continue
            # Append the DataFrame to the list
            all_data_frames.append(df)
        # Concatenate all individual DataFrames into a single DataFrame
        combined_df = pd.concat(all_data_frames, ignore_index=True)
        # Return the combined DataFrame
        return combined_df
    # Handle any exceptions that may occur during file reading
    except Exception as e:
        print('Problem reading files: ', e)
        return None

#########################################################################################

def read_file_from_different_library(ctx, file_url):
    """
    Reads a file from custom library in SharePoint and returns its content as a Pandas DataFrame.

    Args:
        ctx: SharePoint context (e.g., client context)
        file_url: URL of the file on SharePoint

    Returns:
        pd.DataFrame: DataFrame containing the file content
    """
    # Create a MemoryStream to hold the file content
    memory_stream = BytesIO()

    try:
        # Download the file from SharePoint and write it to the MemoryStream
        ctx.web.get_file_by_server_relative_path(file_url).download(memory_stream).execute_query()
    except Exception as e:
        print(f"Error downloading the file: {e}")
        return None

    try:
        # Assuming 'file_content' contains your CSV or Excel data
        file_content = memory_stream.getvalue()
        
        if file_url.lower().endswith(".csv"):
            df = pd.read_csv(BytesIO(file_content))
        else:
            df = pd.read_excel(BytesIO(file_content))

        return df
    except pd.errors.ParserError as e:
        print(f"Error parsing the file content: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None
    finally:
        # Close the MemoryStream (optional, but recommended)
        memory_stream.close()
        
#########################################################################################

def read_file_from_default_library(ctx, file_url, sheet_name=0):
    """
    Function to read a file from SharePoint and return its content as a pandas DataFrame.

    Parameters:
        - file_url (str): URL of the file in SharePoint.
        - ctx: SharePoint context object.
        - sheet_name (str or int, optional): Name or index of the sheet to read (for Excel files). Defaults to 0.

    Returns:
        - pd.DataFrame: DataFrame containing the content of the file.
    """
    # Get the file from SharePoint
    file = File.open_binary(ctx, file_url)
    # Check the file extension to determine the file type
    if file_url.lower().endswith('.csv'):
        # Read CSV file content into a pandas DataFrame using BytesIO
        df = pd.read_csv(BytesIO(file.content))
    elif file_url.lower().endswith('.xlsx'):
        # Read XLSX file content into a pandas DataFrame
        df = pd.read_excel(BytesIO(file.content), sheet_name=sheet_name, engine='openpyxl')
    else:
        # Skip files with unsupported extensions
        print("Unsupported file extension. Please use .csv or .xlsx files.")
        return None
    return df

#########################################################################################
