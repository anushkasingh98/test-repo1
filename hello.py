import streamlit as st
import github_process
import gpt4_process
import llama2_process
import pandas as pd

st.set_page_config(
    page_title="Kathalyst Web App",
    page_icon="images/codeAID_green.png",
)

# placeholder = st.empty()

st.header("Kathalyst - Automated Software Documentation")

github_link = st.sidebar.text_input("Github Link")

model = st.sidebar.radio("Which LLM Model would you like to use?",["GPT-4","Llama 2 70b"],index=0)

if st.sidebar.button("Submit"):
    #process if submit button is pressed
    print(f'Processing {github_link}')
    
    file_contents,file_names,dir = github_process.control(github_link)

    st.write("Processing Github Repo: "+str(github_link))

    doc,vdd = st.tabs(["Documentation","Visual Dependency Diagram"])

    with doc:
        # print("\n\nInside Documentation Tab")
        with st.spinner(text="In progress..."):
            if model == "GPT-4":
                output = gpt4_process.control(file_contents,file_names,dir)
            elif model == "Llama 2 70b":
                output = llama2_process.control(file_contents,file_names)
        st.markdown(output)
    with vdd:
        # print("\n\nInside VDD Tab")
        st.write("Visual Dependency Diagram coming soon ...")
    
    pass

example_links = ["https://github.com/anushkasingh98/personal-portfolio","https://github.com/anushkasingh98/demo-repo",
                 "https://github.com/anushkasingh98/CapitalisationProject"]
df = pd.DataFrame(example_links,columns=["Example Github Links"])

st.sidebar.table(df)

st.sidebar.markdown("Made with ❤️ by Kathalyst")

# clear = st.sidebar.radio("Clear page?",["Yes","No"],index=1)
# if clear == "Yes":
#     placeholder.empty()
# elif clear == "No":
#     pass