def empty_validator(str) :
    return u'0,00' if not str else str

def os_validator(str) :
	return True if str else False

def whitespace_remover(str):
	return ''.join(str.split())