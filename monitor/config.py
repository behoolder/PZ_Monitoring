#-*- coding: utf-8 -*-

class Config:
    """
    Klasa ta służy do skonfigurowania parametrów połaczenia z bazą danych MySQL.\n

    Użycie:\n
    mysql.connector.Connect(**Config.dbinfo())\n
    """
    
    HOST = 'prgzsp'
    DATABASE = 'prgzspdb'
    USER = 'root'
    PASSWORD = 'root'
    PORT = 3306
    
    CHARSET = 'utf8'
    UNICODE = True
    WARNINGS = True
    
    @classmethod
    def dbinfo(cls):
        """
        Zwraca parametry połączenia w formie słownika.
        """

        return {
            'host': cls.HOST,
            'port': cls.PORT,
            'database': cls.DATABASE,
            'user': cls.USER,
            'password': cls.PASSWORD,
            'charset': cls.CHARSET,
            'use_unicode': cls.UNICODE,
            'get_warnings': cls.WARNINGS,
            }
