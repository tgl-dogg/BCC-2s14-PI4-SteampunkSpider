# -*- coding: utf-8 -*-
def empty_validator(str):
    return "" if not str else str

def price_validator(str):
    if not str:
    	return 0.00
    else:
    	# Se tem ponto elimina, se tem vírgula muda pra ponto. #CoisasDeFloat
    	return float(str[0].replace('.', '').replace(',', '.'))

def description_validator(str):
	desc = ""
	for item in str:
		if (item.strip()):
			# Retira whitespaces de dentro da descrição
			desc += (item.replace('\n', '').replace('\r', '').replace('\t', '') + " ")

	return desc

def os_validator(str):
	return 1 if str else 0

def whitespace_remover(str):
	return ''.join(str.split())