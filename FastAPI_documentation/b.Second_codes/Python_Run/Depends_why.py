
def test_f1 () : return 1

def test_f2 ( x = test_f1 ) : print ( x )

test_f2 ()

# <function test_f1 at 0x7f8948f6a160> != 1

# Depends can help us to have return value for parameters by a function name

test_f2 ( 7 ) # 7 works

def test_f2 ( x = test_f1 () ) : print ( x ) # overwrite

test_f2 () # 1 works , i find solution without Depends

test_f2 ( 6 ) # 6 works

def test_f1 ( x ) : return x

try:
     def test_f2 ( x , y = test_f1 ( x ) ) : print ( y )
     
     test_f2 ( 6 ) # name 'x' is not defined , there are no solution for this
     
except: None

print ( 'Test yield' )

def test_f1 () : yield 1

def test_f2 ( x = test_f1 () ) :

    for i in x : print ( i )

test_f2 ()
