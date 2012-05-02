class Config:
    """
    Klasa ta sluzy do skonfigurowania parametrow polaczenia z baza danych MySQL.

    Uzycie:
       mysql.connector.Connect(**Config.dbinfo())
    """
    
    HOST = 'db4free.net'
    DATABASE = 'prgzspdb'
    USER = 'prgzsp'
    PASSWORD = '123321'
    PORT = 3306
    
    CHARSET = 'utf8'
    UNICODE = True
    WARNINGS = True
    
    @classmethod
    def dbinfo(cls):
        """
        Zwraca parametry polaczenia w formie slownika.
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
    
