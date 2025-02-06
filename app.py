import replicate
import os
import streamlit as st
os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"] #"No stealing my API key!"  # put your api_token


# Define the Streamlit app layout
st.title("Cover Letter Generator with Llama 2")

with st.form('Form to generate cover letter'):
    # User input to generate the cover letter 
    st.markdown("### Enter your Cover Letter Details")
    user_name = st.text_input("Name")
    api_key = st.text_input("API Key")
    company = st.text_input("Company Name")
    manager = st.text_input("Hiring Manager")
    role = st.text_input("Job Title")
    referral = st.text_input("How did you find out about this opportunity? (Optional)")
    prompt_input = st.text_area("Job description")
    temperature = st.number_input('AI Temperature. Reflects the model creativity on a scale of 0 to 1', value=0.)

    # Generate LLM response
    generate_cover_letter = st.form_submit_button("Generate!")

if generate_cover_letter:
    if(api_key):
        os.environ["REPLICATE_API_TOKEN"] = api_key
    # Prompts
    pre_prompt = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    # Create a prompt for LLM: Include user inputs, and job description in the prompt
    prompt = f"The job description is: {prompt_input}\n"
    prompt += f"The candidate's name to include on the cover letter: {user_name}\n"
    prompt += f"The job title/role: {role}\n"
    prompt += f"The hiring manager is: {manager}\n"
    prompt += f"How I heard about the opportunity: {referral}\n."
    prompt += "Generate a cover letter"
    # Generate LLM response
    with st.spinner("Generating response"):
        
        response = replicate.run(
            'meta/llama-2-13b-chat',  # Llama 2 model
            input={
                "prompt": f"{pre_prompt} {prompt} Assistant:",
                "temperature": temperature,
            }
        )
        # Extract and display the LLM-generated cover letter
        generated_cover_letter = "".join([item for item in response])
    
    st.subheader("Generated Cover Letter:")
    st.write(generated_cover_letter)

    # Download link for the generated cover letter
    st.subheader("Download Generated Cover Letter:")
    st.download_button("Download Cover Letter as TXT", generated_cover_letter, key="cover_letter")