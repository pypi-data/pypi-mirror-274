import pandas as pd
import os
import sys

from cdh_lava_core.cdc_log_service.environment_logging import LoggerSingleton

# Get the currently running file name
NAMESPACE_NAME = os.path.basename(os.path.dirname(__file__))
# Get the parent folder name of the running file
SERVICE_NAME = os.path.basename(__file__)

class ExcelSheetCombiner:
    
    # Function to check if a column is blank
    @staticmethod
    def is_blank_column(col):
        # Correctly evaluates if column header is empty or NaN
        return (isinstance(col, str) and col.strip() == '') or str(col) == ''

    @staticmethod
    def extract_list_headers( file_path, data_product_id, environment):
        
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("extract_lists"):
            try:                 
                # Load the 'lists' sheet into a DataFrame
                lists_df = pd.read_excel(file_path, sheet_name='lists')
                lists_df['data_product_id'] = data_product_id
                                
                return lists_df
            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise

    @classmethod
    def combine_sheets(cls, file_path, data_product_id, environment):
        
        tracer, logger = LoggerSingleton.instance(
            NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
        ).initialize_logging_and_tracing()

        with tracer.start_as_current_span("combine_sheets"):
            try:
                
                # Load the Excel file
                xls = pd.ExcelFile(file_path)
                
                # Retrieve all sheet names
                sheets = xls.sheet_names
                
                # Find the first sheet that contains 'lists' in its name to determine the cutoff
                list_sheets = [sheet for sheet in sheets if 'lists' in sheet.lower()]
                if not list_sheets:
                    raise ValueError("No 'lists' tabs found in the Excel file.")
                
                # Determine the index of the last 'lists' sheet
                last_list_index = max(sheets.index(sheet) for sheet in list_sheets)

                # Initialize an empty DataFrame to append data
                combined_data = pd.DataFrame()

                # Process each sheet past the last 'lists' sheet
                for sheet in sheets[last_list_index + 1:]:
                    data = pd.read_excel(file_path, sheet_name=sheet)
                    
                    # Append the data if DataFrame is not empty
                    if not combined_data.empty:
                        # Ignore the first row if it's a header row (duplicate)
                        data = data.iloc[1:]
                    
                    combined_data = pd.concat([combined_data, data], ignore_index=True)

                # Assuming the first row of the first appended sheet is the header
                combined_data.columns = combined_data.iloc[0]
                combined_data = combined_data[1:]
                
                # Remove blank rows based on all columns being NaN
                combined_data = combined_data.dropna(how='all')

                # Finding the last non-blank column
                last_valid_index = len(combined_data.columns) - 1
                for col in reversed(combined_data.columns):
                    if cls.is_blank_column(col) and combined_data[col].isna().all():
                        last_valid_index -= 1
                    else:
                        break

                # Dropping blank columns from the end
                if last_valid_index + 1 < len(combined_data.columns):
                    combined_data = combined_data.iloc[:, :last_valid_index + 1]

                # New column names
                new_columns = ['list', 'item_code', 'item_name', 'item_sort', 'item_description', 'item_visibility', 'item_color', 'data_product_id']

                # Rename the columns
                combined_data = combined_data.iloc[:, :8]
                combined_data.columns = new_columns
                combined_data['data_product_id'] = data_product_id
                
                # Remove duplicate rows
                combined_data = combined_data.drop_duplicates()

                return combined_data

            except Exception as ex:
                error_msg = "Error: %s", ex
                exc_info = sys.exc_info()
                LoggerSingleton.instance(
                    NAMESPACE_NAME, SERVICE_NAME, data_product_id, environment
                ).error_with_exception(error_msg, exc_info)
                raise
