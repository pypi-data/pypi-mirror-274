import sys
import pytest
from utils.tp_mongo.src.tp_mongo.main import Mongo
import logging

class TestMongo:

    @pytest.fixture
    def mongo_util(self):
        tmp_logger = logging.getLogger()
        return Mongo("Test app Name", tmp_logger)

    @pytest.fixture
    def mongo_config(self):
        config = {
            Mongo.CONFIG_HOST: "127.0.0.1",
            Mongo.CONFIG_PASSWORD: "Pa$$wor4",
            Mongo.CONFIG_USER: "UserName"
        }
        return config

    def test_str_sanitized_config(self, mongo_util):
        config = {Mongo.CONFIG_PASSWORD : "Pa$$wor4"}
        sanitized_config = mongo_util.sanitized_config(config)
        assert sanitized_config[Mongo.CONFIG_PASSWORD] == "Sanitized"
    
    def test_validate_config(self, mongo_util):
        config = {
            Mongo.CONFIG_HOST: "127.0.0.1",
            Mongo.CONFIG_PASSWORD: "Pa$$wor4",
            Mongo.CONFIG_USER: "User_Name"
        }
        assert mongo_util.validate_config(config) is True

        config = {
            Mongo.CONFIG_PASSWORD: "Pa$$wor4",
            Mongo.CONFIG_PORT: 1324,
            Mongo.CONFIG_USER: "User_Name"
        }
        assert mongo_util.validate_config(config) is False

        config = {}
        assert mongo_util.validate_config(config) is False

    
    def test_build_uri_from_config(self, mongo_util, mongo_config):
        result = mongo_util.build_uri_from_config(mongo_config)
        assert result == f"mongodb+srv://UserName:Pa$$wor4@127.0.0.1/"
