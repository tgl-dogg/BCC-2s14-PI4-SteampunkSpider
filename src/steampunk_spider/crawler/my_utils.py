# -*- coding: utf-8 -*-
def empty_validator(string):
    return "" if not string else string

def price_validator(string):
    if not string:
    	return 0.00
    else:
    	# Se tem ponto elimina, se tem vírgula muda pra ponto. #CoisasDeFloat
    	return float(string[0].replace('.', '').replace(',', '.'))

def description_validator(string):
	desc = ""
	for item in string:
		if (item.strip()):
			# Retira whitespaces de dentro da descrição
			desc += (item.replace('\n', '').replace('\r', '').replace('\t', '') + " ")

	return desc

def level_validator(string):
	if string:
		return int(string[0])
	else:
		return 0

def public_validator(string):
	return 0 if string else 1

def vac_ban_validator(string):
	return 1 if string else 0

def os_validator(string):
	return 1 if string else 0

def whitespace_remover(string):
	return ''.join(string.split())