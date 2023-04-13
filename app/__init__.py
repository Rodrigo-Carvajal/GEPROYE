import os
from flask import Flask
from supabase import create_client, Client

app = Flask(__name__)
app.secret_key = 'vdsajjaqwjnksdivk'

#Inicializar cliente supabase
supabase_url = 'https://eaitbimlcshobgdjzttc.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVhaXRiaW1sY3Nob2JnZGp6dHRjIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Nzk5NjExNTksImV4cCI6MTk5NTUzNzE1OX0.rk_9XJgZ1x3oaEfKJs8pmb3tnlrMxByFDfG8EGUMXOI'
supabase: Client = create_client(supabase_url, supabase_key)

from app.controllers import geproyeBp

app.register_blueprint(geproyeBp)