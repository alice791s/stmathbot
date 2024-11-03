import os
import streamlit as st
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv
import io

load_dotenv()
# Configure your API key
genai.configure(api_key=os.environ['GEMINI_API_KEY'])

# Function to upload and process the image
def process_image(image_file, question):
    if image_file is not None:
        # Read the uploaded file and determine its MIME type
        image_bytes = image_file.read()
        mime_type = image_file.type

        # Create a BytesIO object to pass to the upload function
        image_io = io.BytesIO(image_bytes)

        # Upload the file with the specified MIME type
        myfile = genai.upload_file(image_io, mime_type=mime_type)

        # Prepare the prompt based on user input
        if question:
            prompt = (
                f"Analyze the mathematical content in this image. "
                f"Answer the following question: {question}. "
                "Provide a detailed explanation of the problem, the solution steps, "
                "and the final answer. Make sure to format any mathematical expressions correctly."
            )
        else:
            prompt = (
                "Analyze the mathematical content in this image. "
                "Provide a detailed explanation of the problem, the solution steps, "
                "and the final answer. Make sure to format any mathematical expressions correctly."
            )

        # Initialize the model and generate content
        model = genai.GenerativeModel("gemini-1.5-flash")
        result = model.generate_content([myfile, "\n\n", prompt])
        return result.text  # Return the generated description

# Streamlit interface
st.title("🎓Ваш персональный репетитор")  # Title for the app
st.write("Загрузите изображение с математической задачей и введите свой вопрос ниже.")  # Instructions in Russian

# File uploader
uploaded_file = st.file_uploader("Выберите изображение", type=["jpg", "jpeg", "png"])

# Text input for additional question
user_question = st.text_input("Введите ваш вопрос:", "")  # Prompt in Russian

# Button to submit the question
if st.button("Отправить"):  # Button label in Russian
    if uploaded_file and user_question:
        # Process the image and get the answer
        answer = process_image(uploaded_file, user_question)
        if answer:
            # Show only the final answer
            st.subheader("Ответ:")
            st.write(answer)
        else:
            st.write("Не удалось получить ответ. Попробуйте снова.")
    elif uploaded_file:  # Handle case where only the image is uploaded
        answer = process_image(uploaded_file, "")
        if answer:
            st.subheader("Ответ:")
            st.write(answer)
    else:
        st.write("Пожалуйста, загрузите изображение и введите ваш вопрос.")  # Validation message in Russian

