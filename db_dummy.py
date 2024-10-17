# デプロイの際にはdb.pyを作成し、urlとkeyを設定する
from supabase import create_client,Client

url="supabaseのURL"
key="supabaseのkey"
supabase:Client=create_client(url,key)
