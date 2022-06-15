from fastapi.testclient import TestClient

import sys , urllib3 , logging
sys.path.append ( '/fastapi_data' )

import paramiko_cmd
from main import app

client = TestClient ( app )

urllib3.disable_warnings ()
#https://fastapi.tiangolo.com/tutorial/testing/

# -----------------------------------------------

good_reloadJSON       =   'Token:True; reloadJSON:True; Group:False; Paramiko:False'
good_reload_with_init = [ 'Token:True; reloadJSON:True; Group:False; Paramiko:False' , True ]

fail_paramiko_tests1  =   'Token:False; reloadJSON:False; Group:False; Paramiko:False'
fail_paramiko_tests2  =   'Token:True; reloadJSON:False; Group:False; Paramiko:False'

good_paramiko_tests1  =   'Token:True; reloadJSON:False; Group:True; Paramiko:'
good_paramiko_tests2  =   'Token:True; reloadJSON:False; Group:True; Paramiko:'
good_paramiko_tests3  =   'Token:True; reloadJSON:False; Group:True; Paramiko:'

good_paramiko_group   =   'Token:True; reloadJSON:False; Group:'

good_paramiko_tests1 += "[':: STDOUT: /root; STDERR: ; RETURN: 0']"
good_paramiko_tests2 += "[':: STDOUT: ; STDERR: bash: line 1: cmd19: command not found; RETURN: 127', ':: STDOUT: /root; STDERR: ; RETURN: 0']"
good_paramiko_tests3 += "[]"

last_saved_token , undo = '' , False

# -----------------------------------------------

def test_1_home_page () :
    response = client.get ( "/" )
    assert response.status_code == 200

def test_2_see_your_access_token (
    user = 'pippo' , passw = 'pluto' , result = None ) :
    global last_saved_token
    print ( '' )

    response = client.post (
        'see_your_access_token' ,
         json = { 'user'     : user  ,
                  'password' : passw } )

    print ( 'Result code:' , response         )
    print ( 'Result json:' , response.json () )

    assert response.status_code == 200
    if not result : assert response.json () == None
    elif   result :
           assert len ( response.json () )
           last_saved_token = response.json ()

def test_3_see_your_access_token () :
    test_2_see_your_access_token ( 'bluebook' , '123' , True )

def test_4_see_your_access_token () :
    test_2_see_your_access_token ( 'admin' , '123' , True )

# -----------------------------------------------

def test_5_reloadJSON ( access_token = '' ) :
    second_access_token = access_token
    if access_token == '' : second_access_token = last_saved_token

    response = client.post   ( 'reloadJSON'   ,
                      json = { 'access_token' : second_access_token } )

    print ( 'Result code:' , response         )
    print ( 'Result json:' , response.json () )
    assert response.status_code == 200

    if access_token == '' : assert response.json () == good_reloadJSON
    else                  : assert response.json () == False

def test_6_reloadJSON () :
    test_5_reloadJSON ( last_saved_token [ : -1 ] )

# -----------------------------------------------

def test_07_init_all_machines (
    access_token = '' , mac_name = '' , mac_pass = '' ) :
    second_access_token = access_token

    if access_token == '' :
       second_access_token = last_saved_token
       mac_name = 'Machine_docker'
       mac_pass = '123'

    response = client.post (
      'init_all_machines' ,  json = {
      mac_name : mac_pass , 'access_token' : second_access_token })

    print ( 'Result code:' , response         )
    print ( 'Result json:' , response.json () )
    assert response.status_code == 200

    if access_token == 'abcd' : assert response.json () == False
    else                      : assert response.json () == True

def test_08_init_all_machines () :
    test_07_init_all_machines ( 'abcd' , 'Machine_docker' , '123' )

# test_07_init_all_machines ( last_saved_token , 'Pippo' , '123' ) -> impossible case
# Remember you must absolute not insert Machine Name that makes match with your hosts file
# that is a fastapi vulnerability.

def test_09_init_all_machines () :
    test_07_init_all_machines ( last_saved_token , 'Machine_docker' , 'A' )
    # True because True is not for our ssh-copy, +- is good for security

# -----------------------------------------------

def test_10_reload_with_init (
    access_token = '' , mac_name = '' , mac_pass = '' ) :

    global undo
    second_access_token = access_token

    if access_token == '' :
       second_access_token = last_saved_token
       mac_name = 'Machine_docker'
       mac_pass = '123'

    response = client.post (
      'reload_with_init'  ,  json = {
      mac_name : mac_pass , 'access_token' : second_access_token })

    print ( 'Result code:' , response         )
    print ( 'Result json:' , response.json () )
    assert response.status_code == 200

    if access_token == 'abcd' : assert response.json () == False
    else:
         assert response.json () == good_reload_with_init
         undo = False

def test_11_undo_ssh_copy () :
    global undo
    print ( 'Middle Test for undo_ssh copy' )

    response = client.post ( 'undo_ssh_copy' , json =   {
              'Machine_docker' : True ,
              'access_token'   : last_saved_token })

    undo = response.json ()

    print ( 'Undo Result:' , str ( undo ) )
    assert undo == True

def test_12_reload_with_init () :
    test_10_reload_with_init ( 'abcd' , 'Machine_docker' , '123' )

def test_13_reload_with_init () :
    test_10_reload_with_init ( last_saved_token , 'Machine_docker' , 'B' )

# -----------------------------------------------

def test_14_paramiko ( access_token = '' ,
    mac_name = 'Machine_docker' , well = 'reboot' , tests = 'home' ,
    user = 'bluebook' , passw = '123' ,
    mssg = 'bluebook has Group inside json - valid token and 2 shell' ) :
    
    test_2_see_your_access_token ( user , passw , True )
    if access_token != 'abcd' : access_token = last_saved_token

    return_value , response = None , None
    try:
        response = client.post  (
            'paramiko' , json =   {
            'Name'     : mac_name ,
            'Sistema'  : 'None'   ,
            'Shell1'   : 'None'   ,
            'Shell2'   : 'None'   ,
            'Shell3'   : 'None'   ,

            'Well_Known'  :  well  ,
            'Rombo_boxes' : 'None' ,
            'Tests'       : tests  ,

            'access_token' : access_token })

    except Exception as e : return_value , response = str ( e ) , None

    print ( 'Run on:'  , mac_name )
    print ( 'Message:' , mssg     )

    if response:
       print ( 'Result code:' , response         )
       print ( 'Result json:' , response.json () )
       assert   response.status_code == 200

       if access_token == 'abcd'                         : assert response.json () == fail_paramiko_tests1 ; print ( 'ok case 1.' )
       elif ( well == 'bblbu1' ) and ( tests == ''     ) : assert response.json () == fail_paramiko_tests2 ; print ( 'ok case 2.' )
       elif ( well == 'reboot' ) and ( tests == 'myip' ) : assert response.json () == fail_paramiko_tests2 ; print ( 'ok case 3.' )
       elif ( well == 'bblbu2' ) and ( tests == 'home' ) : assert response.json () == fail_paramiko_tests2 ; print ( 'ok case 4.' )

       elif ( well == ''               ) and ( tests == ''     ) : assert response.json ().count ( good_paramiko_group ) ; print ( 'ok case 5.' )
       elif ( well == 'docker_restart' ) and ( tests == 'myip' ) : assert response.json ().count (   '192.168.56.107'  ) ; print ( 'ok case 6.' )

       elif ( mac_name == 'Mvkyvky' )                    : assert response.json () == fail_paramiko_tests2  ; print ( 'ok case  7.' )

       elif ( well == 'bblbu2' ) and ( tests == ''     ) : assert response.json () == good_paramiko_tests3 ; print ( 'ok case  8.' )
       elif ( well == ''       ) and ( tests == 'home' ) : assert response.json () == good_paramiko_tests1 ; print ( 'ok case  9.' )
       elif ( well == 'reboot' ) and ( tests == 'home' ) : assert response.json () == good_paramiko_tests2 ; print ( 'ok case 10.' )

       else: assert False == True

    elif return_value :
         print ( 'Return Value:' , return_value )
         assert return_value.count ( 'Authentication failed.' )
         print ( 'ok case 11.' )

    else : assert False == True

def test_15_ssh_copy () :
    test_2_see_your_access_token ( 'admin' , '123' , True )
    test_10_reload_with_init ()
    print ( 'Middle Test for ssh copy'    )
    print ( 'Undo Result:' , str ( undo ) )
    assert undo == False
    test_14_paramiko ()

def test_16_paramiko () :
    test_14_paramiko ( 'abcd' , 'Machine_docker' , 'reboot' , 'home' ,
                        mssg = 'bluebook has Group inside json - empty token and 2 shell' )

def test_17_paramiko () :
    test_14_paramiko ( last_saved_token , 'Machine_docker' , '' , 'home' ,
                       mssg = 'bluebook has Group inside json - valid token and 1 shell' )

def test_18_paramiko () :
    test_14_paramiko ( last_saved_token , 'Machine_docker' , '' , '' ,
                       mssg = 'bluebook has Group inside json - valid token and 0 shell' )

# ---- EASY ERRORS ----

def test_19_paramiko () :
    test_14_paramiko ( last_saved_token , 'Machine_docker' , '' ,  '' , user = 'test_user' , passw = '123' ,
                       mssg = 'good_paramiko_group case - test_user has group but not inside json - valid token and 0 shell' )

def test_20_paramiko () :
    test_14_paramiko ( last_saved_token , 'Machine_docker' , '' , '' , user = 'kaumi' , passw = '123' ,
                       mssg = 'good_paramiko_group case - kaumi does not have group - valid token and 0 shell' )

# -------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------- STRONG ERRORS

def test_21_paramiko () :
    test_14_paramiko ( '' , 'Machine_docker' , well = 'bblbu1' , tests = '' , user = 'kaumi'     , passw = '123' ,
                       mssg = 'good_paramiko_group case - kaumi does not have group - valid token and wrong shell' )

def test_22_paramiko () :
    test_14_paramiko ( '' , 'Machine_docker' , well = 'bblbu1' , tests = '' , user = 'test_user' , passw = '123' ,
                       mssg = 'good_paramiko_group case - test_user has group but not inside json - valid token and wrong shell' )

def test_23_paramiko () :
    test_14_paramiko ( '' , 'Machine_docker' , well = 'bblbu2' , tests = '' ,
                       mssg = 'bluebook has Group inside json - valid token and wrong shell' )

def test_24_paramiko () :
    test_14_paramiko ( '' , 'Machane_docker' , well = 'bblbu2' , tests = '' , # all mistakes will be ignored
                       mssg = 'bluebook has Group inside json - valid token + wrong machine and shell' )

def test_25_paramiko () :
    test_14_paramiko ( '' , 'Machane_docker' , well = 'bblbu2' , tests = 'home' , # searching for home
                       mssg = 'bluebook has Group inside json - valid token + wrong machine and good tests' )

def test_26_paramiko () :
    test_14_paramiko ( access_token = None , mac_name = 'Mvkyvky' , # wrong init enable for actions from machine
                       mssg = 'bluebook has Group inside json - valid token and only wrong machine name' )

def test_27_paramiko () :
    test_14_paramiko ( '' , 'Machine_docker' , well = 'reboot' , tests = 'myip' , user = 'bluebook' , passw = '123' ,
                       mssg = 'bluebook has Group inside json - valid token and 2 shell' )

# ---- FINAL TEST DONE ----

def test_28_paramiko () :
    test_14_paramiko ( '' , 'Machine_docker' , well = 'docker_restart' , tests = 'myip' , user = 'bluebook' , passw = '123' ,
                       mssg = 'bluebook has Group inside json - valid token and 2 shell' )
