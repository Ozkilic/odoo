# -*- coding: utf-8 -*-

import os
from openai import OpenAI
import requests
from odoo import models, fields, api


class chatgpt_api(models.Model):
    _name = 'chatgpt_api.chatgpt_api'

    prompt = fields.Text(string="Prompt")
    response = fields.Text(string="Response", readonly=True)


    @api.depends('prompt')
    def send_prompt(self):
        self.response = self._get_chatgpt_response(self.prompt)

    def _get_chatgpt_response(self, prompt):
        try:
            client = OpenAI(api_key = os.getenv('OPENAI_API_KEY'))
            completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}],
            max_tokens=50)

            print(completion.choices[0].message.content)
            
            return completion.choices[0].message.content
        except Exception as e:
            return f"Error: {str(e)}"