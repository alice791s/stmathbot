import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
# import io # Больше не нужен при прямой передаче байт

# Загрузка переменных окружения
load_dotenv()

# Конфигурация API ключа
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    st.error("API ключ GEMINI_API_KEY не найден. Пожалуйста, определите его в файле .env или переменных окружения.")
    st.stop() # Остановить приложение, если ключ отсутствует
try:
    genai.configure(api_key=api_key)
except Exception as e:
    st.error(f"Ошибка конфигурации Gemini API: {e}")
    st.stop()

# Функция для обработки изображения и генерации ответа
def process_image(image_file, question: str):
    """
    Обрабатывает загруженный файл изображения и вопрос пользователя,
    отправляет их модели Gemini и возвращает сгенерированный ответ.
    """
    if image_file is None:
        # Эта проверка больше для внутренней логики, Streamlit UI должен это предотвращать
        return None

    try:
        image_bytes = image_file.getvalue() # Получаем байты напрямую из UploadedFile
        mime_type = image_file.type

        image_part = {
            "mime_type": mime_type,
            "data": image_bytes
        }

        # Формирование промпта
        base_prompt_text = (
            "Проанализируйте математическое содержание на этом изображении. "
            "Предоставьте подробное объяснение задачи, шаги решения и окончательный ответ. "
            "Убедитесь, что все математические выражения правильно оформлены с помощью LaTeX."
            "using LaTeX within $...$ for inline math and $$...$$ for block math."
        )
        
        content_for_model = [image_part] # Начинаем с изображения
        
        if question:
            content_for_model.append(f"{base_prompt_text} Answer the following question: {question}")
        else:
            content_for_model.append(base_prompt_text)
        
        # Инициализация модели
        # ВАЖНО: "gemini-2.0-flash" может быть неактуальным.
        # Рекомендуется "gemini-1.5-flash-latest" или другая актуальная мультимодальная модель.
        # Убедитесь, что выбранная модель поддерживает обработку изображений.
        model_name = os.getenv("GEMINI_MODEL_NAME", "gemini-1.5-flash-latest")
        model = genai.GenerativeModel(model_name)
        
        # Генерация контента
        response = model.generate_content(content_for_model)
            
        return response.text

    except Exception as e:
        st.error(f"Произошла ошибка при взаимодействии с Gemini API: {e}")
        # Для отладки можно добавить:
        # import traceback
        # st.error(traceback.format_exc())
        return None

# Streamlit интерфейс
st.title("🎓 Ваш персональный репетитор по математике")
st.write("Загрузите изображение с математической задачей и, при необходимости, задайте уточняющий вопрос.")

# Загрузчик файлов
uploaded_file = st.file_uploader("Выберите файл изображения", type=["jpg", "jpeg", "png"])

# Поле для ввода вопроса
user_question = st.text_input("Ваш вопрос (необязательно):", "")

# Кнопка для отправки
if st.button("🔍 Проанализировать и решить"):
    if uploaded_file:
        with st.spinner("Анализирую изображение и генерирую ответ... Пожалуйста, подождите ✨"):
            answer = process_image(uploaded_file, user_question)
        
        if answer:
            st.subheader("📝 Решение:")
            st.markdown(answer) # Используем markdown для корректного отображения LaTeX
        # else: # Сообщение об ошибке теперь выводится внутри process_image
            # st.error("Не удалось получить ответ. Попробуйте еще раз или проверьте консоль на ошибки.")
    else:
        st.warning("⚠️ Пожалуйста, сначала загрузите изображение.")

st.caption("Работает AI")
