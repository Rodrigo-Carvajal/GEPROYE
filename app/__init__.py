from flask import Flask, g
from supabase import create_client, Client

#Urls y keys de las bases de datos
supabase_url = 'https://eaitbimlcshobgdjzttc.supabase.co'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVhaXRiaW1sY3Nob2JnZGp6dHRjIiwicm9sZSI6ImFub24iLCJpYXQiOjE2Nzk5NjExNTksImV4cCI6MTk5NTUzNzE1OX0.rk_9XJgZ1x3oaEfKJs8pmb3tnlrMxByFDfG8EGUMXOI'

supabase_url_2 = 'https://ugeojydllzecihhhtmza.supabase.co'
supabase_key_2 = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InVnZW9qeWRsbHplY2loaGh0bXphIiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODMyNTMwNjQsImV4cCI6MTk5ODgyOTA2NH0.PaOdZIY4BXas4pcY3nbVNAcUXOqtK-gu0_0NR76TEHQ'

#Instanciación de los clientes para cada una de las bases de datos
supabase_1: Client = create_client(supabase_url, supabase_key)
supabase_2: Client = create_client(supabase_url_2, supabase_key_2)

app = Flask(__name__)
app.secret_key = 'vdsajjaqwjnksdivk'

from app.controllers import geproyeBp

app.register_blueprint(geproyeBp)