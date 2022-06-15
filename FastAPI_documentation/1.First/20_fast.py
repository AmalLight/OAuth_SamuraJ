from fastapi import FastAPI

# pip3 install fastapi[all]
# pip3 install uvicorn
# uvicorn 14_fast:app --reload

app = FastAPI ()

BOOKS = {

    'book_1' : { 'title' : 'A' , 'author' : 'Pippo' } ,
    'book_2' : { 'title' : 'B' , 'author' : 'Pippo' } ,
    'book_3' : { 'title' : 'C' , 'author' : 'Pippo' } ,
    'book_4' : { 'title' : 'D' , 'author' : 'Pippo' } ,
    'book_5' : { 'title' : 'E' , 'author' : 'Pippo' }
}

#
# @app.get ( '/' )
# async def first_api () :
#
#    return { 'message' : 'Hello All' }
#

@app.get ( '/' )
async def read_all_books () :

    return BOOKS

@app.get ( '/books/{title}' )
async def read_book_title ( title ) : 

    if title in [ BOOKS [ key ] [ 'title' ] for key in BOOKS.keys () ] :

       index_book = [ title == BOOKS [ key ] [ 'title' ] for key in BOOKS.keys () ].index ( True )
       
       return BOOKS [ [ key for key in BOOKS.keys () ] [ index_book ] ]

    else:

       return 'not found'
