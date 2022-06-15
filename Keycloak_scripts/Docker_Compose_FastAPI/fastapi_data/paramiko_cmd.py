from SQLdb.database import engine
from SQLdb.tables   import Base
from sqlalchemy     import text

import os , sys

# --------------------------------------------------------
# --------------------------------------------------------

def init_all_machines ( machines_pass ) :

    gone_well = [ None ] * len ( [ key for key in machines_pass.keys () ] [ : -1 ] )

    os.system ( 'chmod 700 /root/.ssh/id_rsa' )

    with engine.connect () as connection :

         results = connection.execute ( text ( " SELECT action_name , action_cmd FROM actions WHERE action_name ~ '^Machine.+$' " ) )
         for i , result in enumerate ( results ) :

             machine_name    = result [ 0 ]
             machine_user_ip = result [ 1 ]
             
             if not ( machine_name in machines_pass ) : continue
             
             machine_pass = machines_pass [ machine_name ]
             machine_host = machine_user_ip

             if machine_name and machine_user_ip and machine_pass : gone_well [ i ] = True

             index_host = machine_host.index ( "@" ) if machine_host.count ( "@" ) else ( -1 )
             if index_host >= 0 : machine_host = machine_host [ index_host + 1 : ]

             # -----------------------------------------------------------------------------------

             with open ( '/root/.ssh/ssh_keyscan.sh' , 'r' ) as fr :

                  ssh_keyscan_host_text = fr.read ().replace ( 'REPLACE' , machine_host )

                  with open ( '/root/.ssh/ssh_keyscan_{}.sh'.format ( machine_name ) , 'w' ) as fw : fw.write ( ssh_keyscan_host_text )
             os.system ( 'bash /root/.ssh/ssh_keyscan_{}.sh'.format ( machine_name ) )

             # -----------------------------------------------------------------------------------

             with open ( '/root/.ssh/ssh_copy.sh' , 'r' ) as fr :

                  ssh_copy_host_text = fr.read ()

                  while True :
                      if ( ssh_copy_host_text.count ( 'REPLACE1' ) == 0 ) and ( ssh_copy_host_text.count ( 'REPLACE2' ) == 0 ) : break
                      else:
                           ssh_copy_host_text = ssh_copy_host_text.replace ( 'REPLACE1' , machine_pass ).replace ( 'REPLACE2' , machine_user_ip )

                  with open ( '/root/.ssh/ssh_copy_{}.sh'.format ( machine_name ) , 'w' ) as fw : fw.write ( ssh_copy_host_text )
             os.system ( 'bash /root/.ssh/ssh_copy_{}.sh'.format ( machine_name ) )

             # -----------------------------------------------------------------------------------

             with open ( '/root/.ssh/undo_ssh_copy.sh' , 'r' ) as fr :

                  undo_ssh_copy_host_text = fr.read ()

                  while True :
                      if ( undo_ssh_copy_host_text.count ( 'REPLACE1' ) == 0 ) and ( undo_ssh_copy_host_text.count ( 'REPLACE2' ) == 0 ) : break
                      else:
                           undo_ssh_copy_host_text = undo_ssh_copy_host_text.replace ( 'REPLACE1' , machine_pass ).replace ( 'REPLACE2' , machine_user_ip )

                  with open ( '/root/.ssh/undo_ssh_copy_{}.sh'.format ( machine_name ) , 'w' ) as fw : fw.write ( undo_ssh_copy_host_text )
             #os.system ('bash /root/.ssh/undo_ssh_copy_{}.sh'.format ( machine_name ) )

         results.close ()

    return all ( single_step for single_step in gone_well )

import subprocess

def undo_ssh_copy ( machine_names_and_access_token ) :

    data_copy = machine_names_and_access_token.copy ()
    del data_copy [ 'access_token' ]
    
    results , i = [ False ] * len ( [ key for key in data_copy ] ) , 0

    for key in data_copy :
        if data_copy [ key ] == True :

               os.system ( 'bash /root/.ssh/undo_ssh_copy_{}.sh'.format ( key ) )

               results [ i ] = True
        else : results [ i ] = False
        i += 1

    return all ( results )

# --------------------------------------------------------
# --------------------------------------------------------

def run_commands ( data ) :

    os.system ( 'chmod 700 /root/.ssh/id_rsa' )
    da_ritorno , machines_user_host , action_commands = [] , {} , {}

    with engine.connect () as connection :

         results = connection.execute ( text ( " SELECT action_name , action_cmd FROM actions WHERE action_name  ~ '^Machine.+$' " ) )
         for result in results : machines_user_host [ result [ 0 ] ] = result [ 1 ]
         results.close ()

         results = connection.execute ( text ( " SELECT action_name , action_cmd FROM actions WHERE action_name !~ '^Machine.+$' " ) )
         for result in results : action_commands    [ result [ 0 ] ] = result [ 1 ]
         results.close ()

    data_copy = data.copy ()
    del data_copy [ 'access_token' ]
    machine_user_host , commands = '' , []

    for key in data_copy.keys () :

        selected_name = data_copy [ key ]
        if selected_name and ( selected_name != 'None' ) and ( selected_name != '' ) :

           if ( not ( selected_name in action_commands    ) ) and \
              ( not ( selected_name in machines_user_host ) ) : continue

           if   key == 'Name' : machine_user_host  =   machines_user_host [ selected_name ]
           else               : commands          += [ action_commands    [ selected_name ] ]

    if machine_user_host and len ( commands ) :
       machine_user , machine_host = '' , ''

       index_div = machine_user_host.index ( "@" ) if machine_user_host.count ( "@" ) else ( -1 )
       if index_div >= 0 : machine_user = machine_user_host [ : index_div    ]
       if index_div >= 0 : machine_host = machine_user_host [ index_div +1 : ]

       if machine_user and machine_host :
          for command in commands :
              if command : da_ritorno += [ connect ( machine_user , machine_host , command ) ]

    return da_ritorno

from paramiko import SSHClient , AutoAddPolicy

def connect ( user , host , cmd , port = 22 ) :
    da_ritorno , client = '' , SSHClient ()
    
    client.load_host_keys ( os.path.expanduser('~') + '/.ssh/known_hosts' )
    client.load_system_host_keys                       ()
    client.set_missing_host_key_policy ( AutoAddPolicy () )

    client.connect ( host , username = user , port = port )
    stdin, stdout, stderr = client.exec_command ( cmd )

    da_ritorno += str ( ':: STDOUT: ' +       stdout.read ().decode ( "utf8" ) [ :-1 ] )
    da_ritorno += str (  '; STDERR: ' +       stderr.read ().decode ( "utf8" ) [ :-1 ] )
    da_ritorno += str (  '; RETURN: ' + str ( stdout.channel.recv_exit_status     () ) )

    stdin.close  ()
    stdout.close ()
    stderr.close ()
    client.close ()

    return da_ritorno
