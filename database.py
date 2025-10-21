from os import getenv
from supabase import create_client, Client

url = getenv("SUPABASE_URL")
key = getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key)
