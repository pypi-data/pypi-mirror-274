def establish_redshift_connection():
     import redshift_connector
     from zeemee_py.helper_functions import get_config
     from warnings import filterwarnings
     
     filterwarnings("ignore", category=UserWarning, message=".*pandas only supports SQLAlchemy connectable.*")
     
     dbname, user, pwd, host, port = get_config.get_creds("database", "uid", "pwd", "server", "port")
     
     con =redshift_connector.connect(
               host = host,
               database = dbname,
               port = port,
               user = user,
               password = pwd
               )
     
     return con
