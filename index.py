from http.server import BaseHTTPRequestHandler
import os
import google.generativeai as genai
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(b'This is the AMA endpoint. Please submit a question via a POST request.')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            question = parse_qs(post_data.decode('utf-8'))['question'][0]
        except (KeyError, IndexError):
            self.send_response(400)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(b'Bad Request: "question" parameter is missing.')
            return

        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        model = genai.GenerativeModel('gemini-pro')

        prompt = f"""
        You are an AI assistant for Nahid, a passionate front-end developer from Bangladesh.
        Your goal is to answer questions from visitors to Nahid's GitHub profile.
        Be friendly, helpful, and slightly informal.
        Keep your answers concise and to the point.
        
        Here is some information about Nahid:
        - A passionate developer from Bangladesh, interested in creating beautiful and engaging user experiences.
        - Always learning and exploring new technologies.
        - Self-taught developer with a passion for front-end development.
        - Currently diving deeper into the React ecosystem and exploring the world of full-stack development.
        - Skills: JavaScript, HTML, CSS, React, Node.js, Vite, Git, GitHub, VS Code.
        - Currently learning: Next.js, Tailwind CSS, Firebase.
        
        The user's question is: "{question}"
        
        Your answer:
        """
        
        response = model.generate_content(prompt)
        answer = response.text

        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        
        html_response = f"""
        <html>
        <head>
            <title>AMA with Nahid's AI</title>
            <style>
                body {{ font-family: sans-serif; background-color: #f0f0f0; color: #333; }}
                .container {{ max-width: 600px; margin: 50px auto; padding: 20px; background-color: #fff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                h1 {{ color: #F70000; }}
                p {{ line-height: 1.6; }}
                .question {{ font-style: italic; color: #666; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Ask Me Anything (with Nahid's AI)</h1>
                <p class="question">You asked: {question}</p>
                <p>{answer}</p>
                <a href="https://github.com/NotNahid">Back to Nahid's Profile</a>
            </div>
        </body>
        </html>
        """
        self.wfile.write(html_response.encode('utf-8'))