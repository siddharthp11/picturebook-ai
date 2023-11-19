from picturebook_ai_selector import textselect_component
import streamlit as st
import openai 
from openai import OpenAI

st.title('PictureBook.ai')

if 'api_key' not in st.session_state or not st.session_state['api_key']: 
    api_key = st.text_input('Please enter your OpenAI API key!', type='password', )
    
    def submit_key(key):
        if key: st.session_state['api_key'] = key
    
    
    st.button('Enter', on_click=submit_key, args = (api_key, ), type='primary')

    
else:
    if 'text' not in st.session_state or not st.session_state['text']:
        
        
        
        st.subheader('What text do you want to illustrate?')
        text = st.text_area('Enter your text!', height=300, label_visibility='collapsed', placeholder="You'll be able to generate pictures for different parts of your input." )
        
        def text_recieved():   
            if text: 
                st.session_state['images'] = {} 
                st.session_state.text = text 

        def reset_key():
            st.session_state['api_key'] = ''
        
        st.button(label='Submit', on_click= text_recieved, type='primary')
        st.button(label="Back", on_click= reset_key)
        

    elif st.session_state['text']: 
        
        st.subheader('Select portions of your text.')
        annotations = textselect_component(st.session_state.text)
        
        st.subheader('Generate Images Here!')
        imgcol, modelcol = st.columns(2)
        image_display_setting = imgcol.selectbox(label='How would you like the images displayed?',options=('rows', 'columns'))
        model = modelcol.selectbox(label='Which model do you want to use?',options=('dall-e-2', 'dall-e-3'))
        st.session_state['annotations'] = annotations[0] if annotations else []

        def display_annotations():

            def generate(prompt, widget_id):
                try: 
                    client = OpenAI(api_key=st.session_state['api_key'])
                    if model =='dall-e-2':

                        response = client.images.generate(
                            prompt=f"{prompt}",
                            model="dall-e-2",
                            n=1,
                            size="1024x1024"
                        )
                        
                    elif model == 'dall-e-3':
                        response = client.images.generate(
                            prompt=f"Generate an image inspired by the following excerpt: {prompt}",
                            model="dall-e-3",
                            quality= "standard",
                            n=1,
                            size="1024x1024"
                        )
                    image_url = response.data[0].url
                    st.session_state['images'][widget_id] = image_url
                except Exception as e:
                    #Handle API error here, e.g. retry or log
                    st.error(f"API error - check your API key!")
            
                
            annotations = st.session_state['annotations']
            
            for idx, annot in enumerate(annotations): 
                text = st.session_state['text']
                label = annot['label']

                if image_display_setting == "columns":
                    textcol, imgcol = st.columns([6,3])
                    textcol.text_area('x', label, height=220, label_visibility="collapsed")
                    

                    if idx in st.session_state['images'].keys():
                        img = st.session_state['images'][idx]
                        imgcol.image(img)
                    else: 
                        container = imgcol.container()
                        container.button('Generate!', idx, on_click=generate, args=(label,idx),type='primary')
                else: 

                    st.text_area('x', label, label_visibility="collapsed")
                    if idx in st.session_state['images'].keys():
                        img = st.session_state['images'][idx]
                        st.image(img)
                    else: 
                        container = st.container()
                        container.button('Generate!', idx, on_click=generate, args=(label,idx),type='primary')
                
                
                
        if st.session_state['annotations']: 
            display_annotations()
            

        def restart(): 
            st.session_state['text'] = None
            st.session_state['annotations'] = None 
            st.session_state['images'] = {}

        back_button = st.button(label='Restart', on_click= restart, use_container_width=True)

