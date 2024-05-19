class SecurityNotFound(Exception):
    pass

class SecurityAlreadyExists(Exception):
    pass

class InvalidRequest(Exception):
    pass

class MissingAPIToken(Exception):
    pass

class InvalidAPIToken(Exception):
    pass

class DatabaseInsertError(Exception):
    pass

class DatabaseUpdateError(Exception):
    pass

class DatabaseDeleteError(Exception):
    pass

class DatabaseQueryError(Exception):
    pass
