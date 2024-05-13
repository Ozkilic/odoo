# -*- coding: utf-8 -*-
import os
from openai import OpenAI
from odoo import http


class ChatgptApi(http.Controller):
    @http.route('/chatgpt_api/chatgpt_api', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/chatgpt_api/chatgpt_api/objects', auth='public')
    def list(self, **kw):
        return http.request.render('chatgpt_api.listing', {
            'root': '/chatgpt_api/chatgpt_api',
            'objects': http.request.env['chatgpt_api.chatgpt_api'].search([]),
        })

    @http.route('/chatgpt_api/chatgpt_api/objects/<model("chatgpt_api.chatgpt_api"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('chatgpt_api.object', {
            'object': obj
        })
