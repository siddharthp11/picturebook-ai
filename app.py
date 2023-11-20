from picturebook_ai_selector import textselect_component
import streamlit as st
import openai
from openai import OpenAI

st.title(':city_sunset: :bridge_at_night: PictureBook.ai :night_with_stars: :sunrise_over_mountains: ', )

if 'api_key' not in st.session_state or not st.session_state['api_key']:
    st.subheader('Introduction', divider='red')
    inputcol, buttoncol = st.columns([4,1])
    api_key = inputcol.text_input('x', type='password', placeholder='Enter your OpenAI API key.', label_visibility='collapsed')

    def submit_key(key):
        if key:
            st.session_state['api_key'] = key

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
    if 'text' not in st.session_state or not st.session_state['text']:

        st.subheader('What text do you want to illustrate?', divider="blue")
        text = st.text_area('Enter your text!', height=300, label_visibility='collapsed',
                            placeholder="You'll be able to generate pictures for different parts of your input.")
        # pdf = st.file_uploader('Upload a pdf file!')

        def text_recieved():
            if text:
                st.session_state['images'] = {}
                st.session_state.text = text

                def style(text):
                    client = OpenAI(api_key=st.session_state['api_key'])
                    response = client.completions.create(
                        model="gpt-3.5-turbo-instruct",
                        prompt=f"For the following excerpt of text, generate a style description for an image to be generated from this text. Your response will be provided to a text to DALL-E, along with a selection from the text. Your response should ensure that all images from DALL-E have a common theme and style. Your style description could include a) description of the scene, b) colors, c) story theme's, d) any other information that DALL-E could use.  \n\n{text}\n\nProvide only the style, no more:",
                        temperature=1.00,
                        max_tokens=200,
                        top_p=1,
                        frequency_penalty=0,
                        presence_penalty=0
                    )

                    return response.choices[0].text
                st.session_state['style_config'] = style(text)

        def reset_key():
            st.session_state['api_key'] = ''

        st.button(label='Submit', on_click=text_recieved, type='primary')
        st.button(label="Back", on_click=reset_key)

    elif st.session_state['text']:

        st.subheader('Select portions of your text.', divider="blue")
        annotations = textselect_component(st.session_state.text)

        st.subheader(
            'Configure settings for your image generations.', divider="blue")
        gptcol, settingscol = st.columns(2)
        image_display_setting = settingscol.selectbox(
            label='How would you like the images displayed?', options=('rows', 'columns'))
        model = settingscol.selectbox(
            label='Which model do you want to use?', options=('dall-e-2', 'dall-e-3'))

        expanded = gptcol.expander(
            "GPT-3 has provided the following style, which will influence the style of the images.", True)
        st.session_state['style_config'] = expanded.text_area('x', value=str.strip(
            st.session_state['style_config']), label_visibility='collapsed')

        st.session_state['annotations'] = annotations[0] if annotations else []

        st.subheader('Generate your images.', divider="blue")

        def display_annotations():
            style_config = st.session_state['style_config']

            def generate(prompt, widget_id):
                try:
                    client = OpenAI(api_key=st.session_state['api_key'])
                    if model == 'dall-e-2':

                        response = client.images.generate(
                            prompt=f"style instructions: {style_config}, scene:{prompt}",
                            model="dall-e-2",
                            n=1,
                            size="1024x1024"
                        )

                    elif model == 'dall-e-3':
                        response = client.images.generate(
                            prompt=f"Using this style config, {style_config}, Generate an image inspired by the following scene: {prompt}",
                            model="dall-e-3",
                            quality="standard",
                            n=1,
                            size="1024x1024"
                        )
                    image_url = response.data[0].url
                    st.session_state['images'][widget_id] = image_url
                except Exception as e:
                    # Handle API error here, e.g. retry or log
                    st.error(f"API error - check your API key!")

            annotations = st.session_state['annotations']

            for idx, annot in enumerate(annotations):
                text = st.session_state['text']
                label = annot['label']

                if image_display_setting == "columns":
                    textcol, imgcol = st.columns([6, 3])
                    textcol.text_area('x', label, height=220,
                                      label_visibility="collapsed")

                    if idx in st.session_state['images'] and st.session_state['images'][idx]:
                        img = st.session_state['images'][idx]
                        imgcol.image(img)
                        imgcol.button(
                            'Re-Generate!', idx, on_click=generate, args=(label, idx), type='primary')

                    else:
                        container = imgcol.container()
                        container.button('Generate!', idx, on_click=generate, args=(
                            label, idx), type='primary')
                else:

                    st.text_area('x', label, label_visibility="collapsed")
                    if idx in st.session_state['images'] and st.session_state['images'][idx]:
                        img = st.session_state['images'][idx]
                        st.image(img)
                        st.button('Re-generate!', idx, on_click=generate,
                                  args=(label, idx), type='primary')

                    else:
                        container = st.container()
                        container.button('Generate!', idx, on_click=generate, args=(
                            label, idx), type='primary')

        if st.session_state['annotations']:
            display_annotations()

        def restart():
            st.session_state['text'] = None
            st.session_state['annotations'] = None
            st.session_state['images'] = {}

        back_button = st.button(label='Re-enter text',
                                on_click=restart, use_container_width=True)
