from paramiko import SSHClient, AutoAddPolicy
import os.path

def doc ():
    return """

Features:<div><br>

<br>&nbsp;

  * static files are shared from <text style=color:blue>static folder</text>:<br>

<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

    - Example <text style=color:darkred>GET</text>&nbsp; request: 
              <text style=color:darkred>/static/</text>paperino.jpg<br>

<br>&nbsp;

  * paramiko shell responses to <text style=color:blue>/paramiko request</text>:<br>

<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;

    - Example <text style=color:darkred>POST</text>
      request <text style=color:red>form  </text>: 
          for <text style=color:darkred>action</text>='/paramiko': <br><br></div><br>

<form action='/paramiko' target='_blank' method=POST

      style="border:solid 3px gray; padding: 20px; width: 580px;
             margin-left: calc(50% - 290px);
             font-size: initial; color:darkblue;
             background-color: rgba(255,255,255,0.6)" >

  user : <input type=text name=user > &nbsp;
  ipto : <input type=text name=ipto > <br><br>
  
  pssw : <input type=password name=pssw > &nbsp;
  port : <input type=text     name=port >

  <br><br>&nbsp;cmd : <input type=text name=cmd style=width:85%;height:100px > <br><br>

  <input type=submit value=SUBMIT style=width:100%;font-weight:bold; >

</form>

<style>
  body {
      color:        green ;
      font-weight:   bold ;
      font-size: xx-large ;

      font-family: 'Courier New', monospace ;

      background-image:  url( "/static/network.jpg" ) ;

      background-repeat: no-repeat ;
      background-size:   100% auto ;
      background-position:  center ;
  }

  input { height:30px }

  div { border:solid 1px black ; background-color: rgba(255,255,255,0.6) }
</style>

"""

# --------------------------------------------------------

def connect ( ipto , user , port , pssw , cmd ):
    da_ritorno , client = '' , SSHClient()

    client.load_host_keys ( os.path.expanduser('~') + '/.ssh/known_hosts' )
    client.load_system_host_keys ()

    client.set_missing_host_key_policy ( AutoAddPolicy () )

    client.connect ( ipto , username=user , port=port , password=pssw )

    if not cmd: cmd = 'hostname'
    stdin, stdout, stderr = client.exec_command ( cmd )

    da_ritorno += '<br>' + str ( 'STDOUT: ' + stdout.read().decode ("utf8")[:-1] )
    da_ritorno += '<br>' + str ( 'STDERR: ' + stderr.read().decode ("utf8")[:-1] )

    # Get return: 0 is default for success
    da_ritorno += '<br>' + str ( 'Return code: ' + str ( stdout.channel.recv_exit_status () ) )

    stdin.close  ()
    stdout.close ()
    stderr.close ()
    client.close ()

    return da_ritorno
