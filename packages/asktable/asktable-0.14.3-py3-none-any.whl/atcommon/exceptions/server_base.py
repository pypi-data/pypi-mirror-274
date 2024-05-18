# Error Design

class UnknownError(Exception):
    code = -1
    message = "Unknown Internal Error"


class ServerBaseError(Exception):
    code = 0
    message = "Base error"


# 1000 - 配置类错误
class ManagementError(ServerBaseError):
    code = 1
    message = "Management Error"


# 2000 - QA对话类错误
class QAError(ServerBaseError):
    code = 2
    message = "Question Answering Error"


# 3000 - 内部错误
class InternalError(ServerBaseError):
    code = 3
    message = "Internal error"


# 5000 - DataSource 自身内部错误
class DataSourceError(ServerBaseError):
    code = 5
    message = "DataSource Error"

################################


class Unauthorized(ManagementError):
    code = 1000
    message = "Unauthorized"


class DataSourceExists(ManagementError):
    code = 1001
    message = "Datasource already exists"


class DataSourceNotFound(ManagementError):
    code = 1002
    message = "Datasource not found"


class ChatNotFound(ManagementError):
    code = 1003
    message = "Chat not found"


class ParameterError(ManagementError):
    code = 1004
    message = "Parameter error"


class DataSourceConfigError(ManagementError):
    code = 1005
    message = "Datasource config error"


class TenantNotFound(ManagementError):
    code = 1006
    message = "Tenant not found"


class DataSourceMetaProcessing(ManagementError):
    code = 1007
    message = "Datasource meta processing"


class DataSourceMetaNotReady(ManagementError):
    code = 1008
    message = "Datasource meta not ready!"


class SecureTunnelNotFound(ManagementError):
    code = 1009
    message = "SecureTunnel not found"


class SecureTunnelLinkNotFound(ManagementError):
    code = 1010
    message = "SecureTunnel link not found"


class SecureTunnelInUse(ManagementError):
    code = 1011
    message = "SecureTunnel in use"


class ATSTServerAPIError(ManagementError):
    code = 1012
    message = "ATST Server API error"

################################


class QAErrorNoMatchDataSource(QAError):
    code = 2002
    message = "No match datasource"


class QAErrorInsufficientData(QAError):
    code = 2003
    message = "Insufficient data"


class QAErrorIncompleteQuestion(QAError):
    code = 2004
    message = "Incomplete question"


class QAErrorCannotHandle(QAError):
    code = 2005
    message = "Cannot handle"


class QAErrorNoColumnFound(QAError):
    code = 2006
    message = "No column found"


####################################


class PromptTooLong(InternalError):
    code = 3001
    message = "Prompt too long"


class InvalidStrucQuery(InternalError):
    code = 3002
    message = "Invalid query syntax"


class LLMServiceError(InternalError):
    code = 3003
    message = "LLM service error"


class LLMRequestError(InternalError):
    code = 3004
    message = "LLM request error"
