# -*- coding: utf-8 -*-

def audit_streetname(tag):
	errs = []
	tag['value'] = tag['value'].replace(u'nám.',u'náměstí')
	return tag, errs