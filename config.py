from dotenv import dotenv_values
config_values = dotenv_values('.env')
# sqlalchemy_database_uri = dotenv_values('.env')
algorithm = config_values['ALGORITHM']
secret_key = config_values['SECRET_KEY']
access_token_exp_minutes = config_values['ACCESS_TOKEN_EXPIRE_MINUTES']