from picturebook_ai_selector import textselect_component
import streamlit as st
from openai_service import AI

st.title(':city_sunset: :bridge_at_night: PictureBook.ai :night_with_stars: :sunrise_over_mountains: ', )

if 'app_data' not in st.session_state or not st.session_state['app_data']:
    st.subheader('Introduction', divider='red')
    inputcol, buttoncol = st.columns([4,1])
    api_key = inputcol.text_input('x', type='password', placeholder='Enter your OpenAI API key.', label_visibility='collapsed')

    def submit_key(key):
        if key:
            app_data = {
                'openai' : {
                    'key': key,
                    'client': AI(key)
                }
            }
            st.session_state['app_data'] = app_data

    buttoncol.button('Enter', on_click=submit_key, args=(api_key, ), type='primary')
    
    custom_css = """<style>.big-font {font-size: 18px !important; margin-top:-5px;}</style>"""
    st.markdown(custom_css, unsafe_allow_html=True)
    info_str = """<p class="big-font">You know the feeling of reading a book and really wanting to visualize its landscapes, characters, and atmosphere? 
    <span style='color: turquoise;'>PictureBook.ai</span> is inspired by that feeling, and allows users to generate images from their curations of a text.</p>
    <p class="big-font">Just like an illustrated book, PictureBook.ai ensures that generated images are consistent in style, 
    enabling a user to transform any unillustrated text into a PictureBook!</p>
    <p class="big-font">To start, enter your <span style='color: orange;'>OpenAI API key</span>. If you don't have one, you can create one on their website.</p>

"""
    st.markdown(f'<p class="big-font">{info_str}</p>', unsafe_allow_html=True)

    
else:
    app_data = st.session_state['app_data']
    openai_client = app_data['openai']['client']

    if 'text_data' not in app_data:
        st.subheader('What text do you want to illustrate?', divider="blue")
        text = st.text_area('Enter your text!', height=300, label_visibility='collapsed',
                            placeholder="You'll be able to generate pictures for different parts of your input.")

        def text_recieved():
            if text:
                text_data = {
                    'text': text,
                    'style_config': openai_client.style_text(text),
                    'images': {},
                    'selections': []
                } 
                app_data['text_data'] = text_data

        def reset_key():
            st.session_state['app_data'] = {}

        st.button(label='Submit', on_click=text_recieved, type='primary')
        st.button(label="Back", on_click=reset_key)

    elif 'text_data' in app_data:
        text_data = app_data['text_data']
        text, style_config, images = text_data['text'], text_data['style_config'], text_data['images']

        st.subheader('Select portions of your text.', divider="blue")
        text_data['selections'] = textselect_component(text) # bona-fide event listener
        
        st.subheader('Configure settings for your image generations.', divider="blue")
        gptcol, settingscol = st.columns([5,4])

        with gptcol:
            expanded = st.expander("GPT-3 has provided the following style, which will influence the style of the images.", True)
            style_config = expanded.text_area('x', value=str.strip(style_config), label_visibility='collapsed')

        with settingscol: 
            image_display = st.selectbox(label='How would you like the images displayed?', options=('columns', 'rows'))
            image_model = st.selectbox(label='Which model do you want to use?', options=('dall-e-2', 'dall-e-3'))

        st.subheader('Generate your images.', divider="blue")

        def generate_onclick(prompt): 
            images[prompt] = openai_client.generate(prompt, style_config, image_model) 
        
        selections = text_data['selections'][0] if text_data['selections'] else []
        for idx, selection in enumerate(selections):
            prompt = selection['label']

            text_component, img_component = st.container(), st.container()
            if image_display == "columns":
                text_component, img_component = st.columns([6, 3])

            # TEXT
            text_component.text_area('x', prompt, height=220, label_visibility="collapsed")

            # IMAGE AND BUTTONS 
            regenerate_flag = prompt in images and images[prompt]
            button_text = 'Generate!'
            if regenerate_flag:
                img_component.image(images[prompt])
                button_text = 'Re-Generate!'
            img_component.button(button_text, idx, on_click=generate_onclick, args=(prompt, ), type='primary')
        
        def restart():
            del app_data['text_data']

        back_button = st.button(label='Re-enter text',on_click=restart, use_container_width=True)
