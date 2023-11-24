# picturebook-ai

## Overview 
* PictureBook.ai allows readers to generate images from their favourite books.
* Using model pipeling with GPT3 and DALL-E, PictureBook ensures that generated images are consistent in style, enabling a user to transform any unillustrated text into a PictureBook!
* To start, enter your OpenAI API key. If you don't have one, you can create one on their website.

## Development   
* A custom ui component was built to support text selection, which is not natively supported by streamlit. It will be installed by default if you `pip install -r requirements.txt``.
* Else, you can install using pip `pip install picturebook-ai-selector-3`.
* For development, `streamlit run app.py`
* Test deployed at https://picturebook-ai-c6ejeietkztcmrxzbcupdu.streamlit.app/
