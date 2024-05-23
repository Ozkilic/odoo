import os
from odoo import models, fields, api
from openai import OpenAI
from facebook import GraphAPI, GraphAPIError
import base64
import requests
from io import BytesIO

class facebook_post(models.Model):
    _name = 'facebook.post'
    _description = 'Facebook Post'

    name = fields.Char('Name', required=True)
    prompt = fields.Text('Prompt')
    message = fields.Text('Message', required=True)
    image = fields.Image(string='Image')
    image_filename = fields.Char(string='Image Filename')


    def generate_message_and_image(self):
        # Mesaj oluşturma
        try:
            client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))


            # Mesaj oluşturma
            completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": self.prompt}],
            max_tokens=50)

            print(completion.choices[0].message.content)
            
            self.message = completion.choices[0].message.content


            # Görüntü oluşturma
            image_response = client.images.generate(
                model="dall-e-3",
                prompt=self.prompt,
                size="512x512",
                quality="standart",
                n=1
            )

            
            image_url = image_response.data[0].url
            image_data = requests.get(image_url).content
            self.image = base64.b64encode(image_data)



            # Görüntü için bir isim oluşturma
            name_prompt = f"Generate a suitable name for an image with the following prompt: {self.prompt}"
            name_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": name_prompt}],
            max_tokens=10
            )

            image_name = name_completion.choices[0].message.content.strip().replace(" ", "_")
            self.image_filename = f"{image_name}.png"

            return True

        except Exception as e:
            return f"Error: {str(e)}"
       
       
    def create_facebook_post(self):
        # Facebook erişim token'ınızı buraya ekleyin
        access_token = os.getenv('FACEBOOK_ACCESS_TOKEN')
        graph = GraphAPI(access_token)

        message = self.message
        image = self.image
        image_filename = self.image_filename

        try:
            if image:
                image_data = base64.b64decode(image)

                # Dosyayı geçici bir dosyaya yaz
                with open(image_filename, 'wb') as f:
                    f.write(image_data)

                # Facebook'a post request gönder
                with open(image_filename, 'rb') as f:
                    graph.put_photo(image=f, message=message)
                    print("Post shared successfully on Facebook!")
            else:
                graph.put_object(parent_object='me', connection_name='feed', message=message)
                print("Post shared successfully on Facebook!")
        except GraphAPIError as e:
            print("Failed to share post on Facebook:", str(e))
        return True
