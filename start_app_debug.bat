cd "$(dirname ".\create_bat_fastapi.bat")" 
call .\env\Scripts\activate 
python -m uvicorn app.main:app --reload --host=192.168.30.103 --port=3000 
