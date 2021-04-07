class UnknownId(Exception):
    name = ""

    def __str__(self):
        return "Unknown " + self.name + " id: " + str(self.args[0])


class TaskUnknownId(UnknownId):
    name = "task"


class CategoryUnknownId(UnknownId):
    name = "category"


class FileUnknownId(UnknownId):
    name = "file"


class UserUnknownId(UnknownId):
    name = "user"


class RoleUnknownId(UnknownId):
    name = "role"


class CategoryExistName(Exception):
    def __str__(self):
        return "Category name " + str(self.args[0]) + " already exist"


class InvalidSchema(Exception):
    def __str__(self):
        return "Invalid schema: " + str(self.args[0])


class LoginError(Exception):
    def __str__(self):
        return "Invalid login or password"


class RegistrationError(Exception):
    def __str__(self):
        return ""  # TODO - sss


class ForbiddenOperation(Exception):
    def __str__(self):
        return "Forbidden operation - ", str(self.args[0])


class ExpiredToken(Exception):
    def __str__(self):
        return "Expired JWT"


class InvalidToken(Exception):
    def __str__(self):
        return "Invalid JWT"


class TokenInBlockList(Exception):
    def __str__(self):
        return "JWT in blocklist"


class NoContentError(Exception):
    def __str__(self):
        return "Required a file"


class UnconfirmedEmailError(Exception):
    def __str__(self):
        return "Unconfirmed Email"
