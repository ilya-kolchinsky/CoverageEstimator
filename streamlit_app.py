import os
import subprocess

import streamlit as st


# Streamlit app
def main():
    st.set_page_config(layout="wide")

    st.title("Test Selection Demo")

    st.write("""
        This application analyzes the provided source file and picks the tests cases out of a given folder that it 
        estimates to be the best in testing the file.\n
        Enter the URLs in the text boxes below and click 'Recommend Test Cases' to see the output.
        """)

    # Input text boxes for URLs
    src_file_url = st.text_input("Enter the Github URL of the source file:")
    test_dir_url = st.text_input("Enter the Github URL of the tests directory:")

    # Optional advanced settings
    default_settings = "Let the system decide the best settings"
    define_max_tests_num = "Select at most X test cases"
    define_max_tests_percentage = "Select at most X% of all test cases"
    additional_options = ""
    col1, col2 = st.columns([2, 3])
    with col1:
        option = st.radio(
            "Test Selection Settings",
            (default_settings, define_max_tests_num, define_max_tests_percentage)
        )
    with col2:
        if option == define_max_tests_num:
            max_tests_num_text_input = st.text_input("Enter max number of test cases:")
            if max_tests_num_text_input:
                additional_options = "--output-tests-num " + max_tests_num_text_input
        if option == define_max_tests_percentage:
            max_percentage_num_text_input = st.text_input("Enter max percentage of test cases:")
            if max_percentage_num_text_input:
                additional_options = "--output-tests-perc " + max_percentage_num_text_input

    # Button to invoke the model
    if st.button("Recommend Test Cases"):
        if src_file_url and test_dir_url:
            try:

                command = f"python main.py -s -r --tests-path {test_dir_url} --change-path {src_file_url} {additional_options}"
                processing_output_text = ""
                results_text = ""
                displaying_results = False

                num_of_process_steps = 6
                progress_bar = st.progress(0)
                progress = 0
                progress_step_size = 1.0 / num_of_process_steps

                try:
                    # Initialize an empty placeholder for output
                    output_placeholder = st.empty()
                    # Run the command and capture the output in real time
                    with subprocess.Popen(command, shell=True, cwd=os.getcwd(), stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          text=True) as process:
                        for line in process.stdout:
                            if displaying_results:
                                results_text += "\n" + line
                                output_placeholder.text(results_text)
                            elif line.startswith("RESULTS"):
                                displaying_results = True
                                progress_bar.progress(1.0)
                            else:
                                if not line.startswith("Processing test file"):
                                    progress = min(progress + progress_step_size, 1.0)
                                else:
                                    progress = min(progress + progress_step_size * 0.1, 1.0 - progress_step_size)
                                progress_bar.progress(progress)
                                processing_output_text += "\n" + line
                                output_placeholder.text(processing_output_text)
                except Exception as e:
                    st.error(str(e))
            except Exception as e:
                # Handle exceptions and display an error message
                st.error(f"An error occurred: {e}")
        else:
            st.error("Please enter both URLs.")


if __name__ == "__main__":
    main()
