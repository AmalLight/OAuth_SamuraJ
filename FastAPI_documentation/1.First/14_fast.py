from fastapi import FastAPI

# pip3 install fastapi[all]
# pip3 install uvicorn
# uvicorn 14_fast:app --reload

app = FastAPI ()

@app.get ( '/' )
async def first_api () :

    return { 'message' : 'Hello All' }
