import pandas as pd
import streamlit as st

def process_files(file1, email_column_file1, file2, email_column_file2):
    # Read the CSV files
    file1_data = pd.read_csv(file1)
    file2_data = pd.read_csv(file2)

    # Match email columns and merge data
    matching_emails = file1_data[email_column_file1].unique()
    matched_data = file2_data[file2_data[email_column_file2].isin(matching_emails)]

    # Select output columns
    output_columns = [email_column_file2] + [col for col in file2_data.columns if col != email_column_file2]
    result = matched_data[output_columns]

    return result

# Streamlit app
def main():
    st.title("Email Matching and Data Merge")

    # Upload first file
    st.header("Upload the First File")
    file1 = st.file_uploader("Upload the first CSV file (original file)", type="csv")
    email_column_file1 = None
    if file1 is not None:
        try:
            file1_data = pd.read_csv(file1)
            st.write("Columns in the first file:", list(file1_data.columns))
            email_column_file1 = st.selectbox("Select the email column in the first file", options=list(file1_data.columns))
        except pd.errors.EmptyDataError:
            st.error("The first file is empty or invalid. Please upload a valid CSV file.")

    # Upload second file
    st.header("Upload the Second File")
    file2 = st.file_uploader("Upload the second CSV file", type="csv")
    email_column_file2 = None
    if file2 is not None:
        try:
            file2_data = pd.read_csv(file2)
            st.write("Columns in the second file:", list(file2_data.columns))
            email_column_file2 = st.selectbox("Select the email column in the second file", options=list(file2_data.columns))
        except pd.errors.EmptyDataError:
            st.error("The second file is empty or invalid. Please upload a valid CSV file.")

    # Process and download the result
    if file1 is not None and file2 is not None and email_column_file1 and email_column_file2:
        st.header("Process and Download")
        if st.button("Generate Output File"):
            result = process_files(file1, email_column_file1, file2, email_column_file2)
            st.write("Generated Data Preview:")
            st.dataframe(result)

            # Provide download link
            output_file_name = "matched_output.csv"
            result.to_csv(output_file_name, index=False)
            with open(output_file_name, "rb") as f:
                st.download_button(
                    label="Download Output File",
                    data=f,
                    file_name=output_file_name,
                    mime="text/csv"
                )

if __name__ == "__main__":
    main()
