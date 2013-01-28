#! /usr/bin/env python
# -*- coding: utf-8 -*-

import glpk
import math

tps_vie = 96 #8ans = 96mois
tps_maturation_sexuelle = 7 #mois
tps_maturation_standard = 2 #mois
tps_maturation_label_rouge = 3 #mois

masse_standard =  1.65 #kg
masse_label_rouge = 2 #kg
masse_vieille = 1.5 #kg

capacite_ponte = 8 #oeufs/mois/pintade

surface_int_standard_et_pondeuse = 0.0625 #m²/pintade
surface_ext_standard_et_pondeuse = 0 #m²/pintade
surface_int_label_rouge = 0.0769 #m²/pintade
surface_ext_label_rouge = 2 #m²/pintade

fraction_pondeuse_sur_pondeuse_et_standard = 0.6 #les pondeuses et les standards sont elevees dans les memes conditions, sauf que sur 10 pintades dans ces conditions, 6 sont des pondeuses

capacite_sac_grain = 25 #kg
quantite_grain_conso = 1.5 #kg de grain/mois/pintade

prix_standard = 8 #euros/kg
prix_label_rouge = 12 #euros/kg
prix_vieille = 3 #euros/kg
prix_oeuf = 1 #euro
prix_surface_int = 1000 #euros/m²
prix_surface_ext = 10 #euros/m²
prix_grain = 1 #euros/kg de grain

stock_argent = 5000 #euros
stock_grain = 500 #kg
surface_int = 200 #m²
surface_ext = 200 #m²

surface_ajoutee = 50 #m²

tps_simulaton = 12 #ans

tab_pondeuse = tps_vie*[0]
tab_standard = tps_maturation_standard*[0]
tab_label_rouge = tps_maturation_label_rouge*[0]

def pondeuse_initale():
	capacite_pondeuse = capacite_pintade()[3]
	for index in range(len(tab_pondeuse)):
		if capacite_pondeuse >= 0:
			capacite_pondeuse -= 10
			tab_pondeuse[index] = 10

def gestion_des_oeufs():
	nb_disparu = tab_standard[len(tab_standard)-1] + tab_label_rouge[len(tab_label_rouge)-1] + tab_pondeuse[len(tab_pondeuse)-1]
	nb_oeuf_restant = compte_pondeuse_mature()*capacite_ponte - nb_disparu
	evo_label_rouge()
	evo_standard()
	evo_pondeuse()
	if nb_oeuf_restant > 0 and compte_pondeuse() < capacite_pintade()[3]:
		nb_nouvelle_pondeuse = math.ceil(((capacite_pintade()[3] - compte_pondeuse())/len(tab_pondeuse)))
		tab_pondeuse[0] = nb_nouvelle_pondeuse
		nb_oeuf_restant -= nb_nouvelle_pondeuse

	if nb_oeuf_restant > 0 and compte_label_rouge() < capacite_pintade()[1]:
		nb_nouvelle_label_rouge = math.ceil(((capacite_pintade()[1] - compte_label_rouge())/len(tab_label_rouge)))
		tab_label_rouge[0] = nb_nouvelle_label_rouge
		nb_oeuf_restant -= nb_nouvelle_label_rouge

	if nb_oeuf_restant > 0 and compte_standard() < capacite_pintade()[2]:
		nb_nouvelle_standard = math.ceil(((capacite_pintade()[2] - compte_label_rouge())/len(tab_standard)))
		tab_standard[0] = nb_nouvelle_standard
		nb_oeuf_restant -= nb_nouvelle_standard
	vendre_oeuf(nb_oeuf_restant)

def capacite_pintade():
	lp_capacite = glpk.LPX()
	lp_capacite.name = 'capacite pintade'
	lp_capacite.obj.maximize = True
	
	lp_capacite.rows.add(2)
	lp_capacite.rows[0].name = "surface int"
	lp_capacite.rows[0].bounds = None, surface_int  #m²
	lp_capacite.rows[1].name = "surface ext"
	lp_capacite.rows[1].bounds = None, surface_ext  #m²
	
	lp_capacite.cols.add(2)
	lp_capacite.cols[0].name = "label rouge"
	lp_capacite.cols[0].bounds = 0.0, None
	lp_capacite.cols[1].name = "standard + pondeuse"
	lp_capacite.cols[1].bounds = 0.0, None
	
	lp_capacite.obj[:] = [ 1, 1]
	lp_capacite.matrix = [ surface_int_label_rouge, surface_int_standard_et_pondeuse,
	          			   surface_ext_label_rouge, surface_ext_standard_et_pondeuse]
	lp_capacite.simplex()
	
	capacite_totale = lp_capacite.obj.value
	capacite_label_rouge = lp_capacite.cols[0].primal
	capacite_standard = (1 - fraction_pondeuse_sur_pondeuse_et_standard) * lp_capacite.cols[1].primal
	capacite_pondeuse = fraction_pondeuse_sur_pondeuse_et_standard * lp_capacite.cols[1].primal
	return capacite_totale, capacite_label_rouge, capacite_standard, capacite_pondeuse



def evo_label_rouge():
	vendre_label_rouge()
	for index in range(len(tab_label_rouge)-1):
		tab_label_rouge[len(tab_label_rouge) - index - 1] = tab_label_rouge[len(tab_label_rouge) - index - 2]

def evo_standard():
	vendre_standard()
	for index in range(len(tab_standard)-1):
		tab_standard[len(tab_standard) - index - 1] = tab_standard[len(tab_standard) - index - 2]

def evo_pondeuse():
	vendre_vieille()
	for index in range(len(tab_pondeuse)-1):
		tab_pondeuse[len(tab_pondeuse) - index - 1] = tab_pondeuse[len(tab_pondeuse) - index - 2]



def compte_label_rouge():
	nb_label_rouge = 0
	for index in range(len(tab_label_rouge)-1):
		nb_label_rouge += tab_label_rouge[index]
	return nb_label_rouge
		
def compte_standard():
	nb_standard = 0
	for index in range(len(tab_standard)-1):
		nb_standard += tab_standard[index]
	return nb_standard

def compte_pondeuse():
	nb_pondeuse = 0
	for index in range(len(tab_pondeuse)-1):
		nb_pondeuse += tab_pondeuse[index]
	return nb_pondeuse
		
def compte_pondeuse_mature():
	nb_pondeuse_mature = 0
	for index in range(len(tab_pondeuse)-tps_maturation_sexuelle):
		nb_pondeuse_mature += tab_pondeuse[index+tps_maturation_sexuelle]
	return nb_pondeuse_mature

def compte_pintade():
	nb_pintade = 0
	nb_pintade = compte_label_rouge() + compte_standard() + compte_pondeuse()
	return nb_pintade



def augmenter_surface_int():
	global stock_argent
	global surface_int
	surface_int += surface_ajoutee
	stock_argent -= surface_ajoutee*prix_surface_int
	
def augmenter_surface_ext():
	global stock_argent
	global surface_ext
	surface_ext += surface_ajoutee
	stock_argent -= surface_ajoutee*prix_surface_ext

def choix_augmenter_terrain():
	global stock_argent
	global stock_grain
	global surface_int
	global surface_ext
	global tab_pondeuse
	global tab_standard
	global tab_label_rouge
	stock_argent_temp = stock_argent
	stock_grain_temp = stock_grain
	surface_int_temp = surface_int
	surface_ext_temp = surface_ext
	tab_pondeuse_temp = tab_pondeuse
	tab_standard_temp = tab_standard
	tab_label_rouge_temp = tab_label_rouge

	simulation_annee()
	argent_augm_int = stock_argent

	stock_argent = stock_argent_temp
	stock_grain = stock_grain_temp
	surface_int = surface_int_temp
	surface_ext = surface_ext_temp
	tab_pondeuse = tab_pondeuse_temp
	tab_standard = tab_standard_temp
	tab_label_rouge = tab_label_rouge_temp

	simulation_annee()
	argent_augm_ext = stock_argent

	stock_argent = stock_argent_temp
	stock_grain = stock_grain_temp
	surface_int = surface_int_temp
	surface_ext = surface_ext_temp
	tab_pondeuse = tab_pondeuse_temp
	tab_standard = tab_standard_temp
	tab_label_rouge = tab_label_rouge_temp

	if max(argent_augm_int, argent_augm_ext) == argent_augm_int:
		augmenter_surface_int()
	else:
		augmenter_surface_ext()


def vendre_label_rouge():
	global stock_argent
	stock_argent += tab_label_rouge[tps_maturation_label_rouge-1]*masse_label_rouge*prix_label_rouge
	tab_label_rouge[tps_maturation_label_rouge-1] = 0 

def vendre_standard():
	global stock_argent
	stock_argent += tab_standard[tps_maturation_standard-1]*masse_standard*prix_standard
	tab_standard[tps_maturation_standard-1] = 0
	
def vendre_vieille():
	global stock_argent
	stock_argent += tab_pondeuse[tps_vie-1]*masse_vieille*prix_vieille
	tab_pondeuse[tps_vie-1] = 0
	
def vendre_oeuf(nb_oeuf_vendu):
	global stock_argent
	stock_argent += nb_oeuf_vendu*prix_oeuf



def consommation_de_grain():
	global stock_grain
	stock_grain -= compte_pintade()*quantite_grain_conso

def acheter_du_grain():
	global stock_argent
	global stock_grain
	nb_de_pintade = compte_pintade()
	if stock_grain < nb_de_pintade*quantite_grain_conso:
		grain_acheter = nb_de_pintade*capacite_sac_grain #on achete un sac de grain par pintade pour etre tranquille pour un moment
		stock_grain += grain_acheter
		stock_argent -= grain_acheter*prix_grain



def simulation_annee():
	for iteration_mois in range(12):
		gestion_des_oeufs()
		acheter_du_grain()
		consommation_de_grain()
		# print "---------------------"
		# print "argent = " + str(stock_argent) + ", grain = " + str(stock_grain)
		# print "pondeuse" + str(tab_pondeuse)
		# print "standard" + str(tab_standard)
		# print "label rouge" + str(tab_label_rouge)

def simulation():
	print "simulation"
	print "pondeuse" + str(tab_pondeuse)
	print "standard" + str(tab_standard)
	print "label rouge" + str(tab_label_rouge)
	for iteration_annee in range(tps_simulaton):
		simulation_annee()
		choix_augmenter_terrain()
	print "capacite totale = " + str(capacite_pintade()[0]) + ", capacite label rouge = " + str(capacite_pintade()[1]) + ", capacite standard = " + str(capacite_pintade()[2]) + ", capacite pondeuse = " + str(capacite_pintade()[3])
	print compte_pintade()
	print compte_pondeuse()
	print compte_standard()
	print compte_label_rouge()

if __name__ == "__main__":
	pondeuse_initale()
	simulation()