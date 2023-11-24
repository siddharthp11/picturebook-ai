from openai import OpenAI 
import openai 

class AI:
    def __init__(self, key):
        self.client = OpenAI(api_key=key)
    
    def style_text(self, text):
        response = self.client.completions.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"For the following excerpt of text, generate a style description for an image to be generated from this text. Your response will be provided to a text to DALL-E, along with a selection from the text. Your response should ensure that all images from DALL-E have a common theme and style. Your style description could include a) description of the scene, b) colors, c) story theme's, d) any other information that DALL-E could use.  \n\n{text}\n\nProvide only the style, no more:",
            temperature=1.00,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        ## return a style agent instance to make calls to generate image
        return response.choices[0].text
    
    def generate(self, prompt, style_config, model):
        try:
            response = self.client.images.generate(
                    prompt=f"style instructions: {style_config}, scene:{prompt}",
                    model=model,
                    n=1,
                    quality="standard",
                    size="1024x1024"
                )

            image_url = response.data[0].url
            return image_url
        
        except Exception as e:
            return False 
        
