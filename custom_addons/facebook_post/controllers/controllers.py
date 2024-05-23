from odoo import http
from odoo.http import request

class OpenAIFacebookIntegration(http.Controller):

    @http.route('/openai_facebook_integration/generate', type='json', auth='user')
    def generate_message_and_image(self, prompt):
        Post = request.env['facebook.post']
        new_post = Post.create({'name': 'Generated Post', 'prompt': prompt})
        new_post.generate_message_and_image()
        return {
            'message': new_post.message,
            'attachment': new_post.attachment.decode('utf-8') if new_post.attachment else None,
            'attachment_filename': new_post.attachment_filename
        }

    @http.route('/openai_facebook_integration/post_to_facebook', type='json', auth='user')
    def post_to_facebook(self, post_id):
        post = request.env['facebook.post'].browse(post_id)
        if post:
            post.create_facebook_post()
            return {'status': 'success'}
        return {'status': 'error', 'message': 'Post not found'}
