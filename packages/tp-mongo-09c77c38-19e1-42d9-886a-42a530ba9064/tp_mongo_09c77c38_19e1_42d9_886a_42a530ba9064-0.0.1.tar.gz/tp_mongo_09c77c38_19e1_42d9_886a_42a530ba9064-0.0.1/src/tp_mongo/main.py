from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

class Mongo():
    CONFIG_PASSWORD = 'password'
    CONFIG_USER = 'user'
    CONFIG_HOST = 'host'
    CONFIG_PORT = 'port'
    CONFIG_DBNAME = 'db_name'
    CONFIG_PARAMS = 'params'
    
    def __init__(self, application_name, logger) -> None:
        self.application_name = application_name
        self.logger = logger

    def init_mongo(self, config):      
        self.logger.info(f"Mongo: Init for: {self.application_name}. with the following config: {self.sanitized_config(config)}")
        uri = self.build_uri_from_config(config)
        connection = self.build_connection(uri, self.application_name)
        return connection

    def sanitized_config(self, config):
        dup_config = dict(config)
        dup_config[Mongo.CONFIG_PASSWORD] = "Sanitized"
        sanitized_config = dup_config
        return sanitized_config

    def build_uri_from_config(self, config):
        if self.validate_config(config):
            connection_uri = f"mongodb+srv://{config[Mongo.CONFIG_USER]}:{config[Mongo.CONFIG_PASSWORD]}@{config[Mongo.CONFIG_HOST]}/"
            if Mongo.CONFIG_PARAMS in config:
                connection_uri += f"?{config[Mongo.CONFIG_PARAMS]}"
            return connection_uri
        self.logger.error(f"Mongo: build_uri_from_config for {self.application_name} failed. Config failed validation {self.sanitized_config(config)}")
        return None
        
    def validate_config(self, config):
        required_keys = {Mongo.CONFIG_PASSWORD,
                         Mongo.CONFIG_USER, 
                         Mongo.CONFIG_HOST}
        return required_keys <= set(config.keys())
    
    def build_connection(self, uri, application_name):
        self.logger.info(f"Mongo: Creating connection for: {application_name}")
        client = MongoClient(uri, minPoolSize=2)
        try:
            # The ping command is cheap and does not require auth.
            client.admin.command('ping')
        except ConnectionFailure:
            self.logger.error("Mongo: Creating connection for: {application_name} failed: Server not available")
        return client
    

if __name__ == "__main__":
    # Local connection test
    import logging
    tmp_logger = logging.getLogger()
    tp_mongo =  Mongo("Test app Name", tmp_logger)
    mongo_config = {
                Mongo.CONFIG_HOST: 'hellbender.1m4ffvz.mongodb.net',
                Mongo.CONFIG_PASSWORD: 'kGjLCiLpwHZlME5W',
                Mongo.CONFIG_USER: 'default',
                Mongo.CONFIG_PARAMS: 'retryWrites=true&w=majority&appName=hellbender'
                }
    client = tp_mongo.init_mongo(mongo_config)
    print(client)