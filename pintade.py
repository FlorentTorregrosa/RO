#! /usr/bin/env python
# -*- coding: utf-8 -*-

import glpk
import math
from math import *
from matplotlib import *
import matplotlib.pyplot as plt
from pylab import *

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

surface_ajoutee = 50 #m²

tps_simulaton = 20 #ans

stock_argent = 5000 #euros
stock_grain = 500 #kg
surface_int = 200 #m²
surface_ext = 200 #m²

figure = plt.figure()
tab_stock_argent = [stock_argent]
tab_stock_grain = [stock_grain]
tab_surface_int = [surface_int]
tab_surface_ext = [surface_ext]
tab_nb_pintade = []
tab_nb_pondeuse = []
tab_nb_standard = [0]
tab_nb_label_rouge = [0]

tab_pondeuse = tps_vie*[0]
tab_standard = tps_maturation_standard*[0]
tab_label_rouge = tps_maturation_label_rouge*[0]

def pondeuse_initale():
	capacite_pondeuse = capacite_pintade()[3]
	for index in range(len(tab_pondeuse)):
		if capacite_pondeuse >= 0:
			capacite_pondeuse -= 10
			tab_pondeuse[index] = 10
	tab_nb_pintade.append(compte_pintade())
	tab_nb_pondeuse.append(compte_pondeuse())



def gestion_des_oeufs():
	nb_disparu = tab_standard[len(tab_standard)-1] + tab_label_rouge[len(tab_label_rouge)-1] + tab_pondeuse[len(tab_pondeuse)-1]
	nb_oeuf_restant = compte_pondeuse_mature()*capacite_ponte - nb_disparu
	evo_label_rouge()
	evo_standard()
	evo_pondeuse()
	nb_oeuf_restant = naitre_pondeuse(nb_oeuf_restant)
	nb_oeuf_restant = naitre_label_rouge(nb_oeuf_restant)
	nb_oeuf_restant = naitre_standard(nb_oeuf_restant)
	vendre_oeuf(nb_oeuf_restant)

def naitre_label_rouge(nb_oeuf):
	if nb_oeuf > 0 and compte_label_rouge() < capacite_pintade()[1]:
		capacite_reguliere = capacite_pintade()[1]/len(tab_label_rouge)
		nb_nouvelle_label_rouge = math.ceil(min(nb_oeuf, capacite_reguliere))
		tab_label_rouge[0] = nb_nouvelle_label_rouge
		nb_oeuf -= nb_nouvelle_label_rouge
	return nb_oeuf

def naitre_standard(nb_oeuf):
	if nb_oeuf > 0 and compte_standard() < capacite_pintade()[2]:
		capacite_reguliere = capacite_pintade()[2]/len(tab_standard)
		nb_nouvelle_standard = math.ceil(min(nb_oeuf, capacite_reguliere))
		tab_standard[0] = nb_nouvelle_standard
		nb_oeuf -= nb_nouvelle_standard
	return nb_oeuf

def naitre_pondeuse(nb_oeuf):
	if nb_oeuf > 0 and compte_pondeuse() < capacite_pintade()[3]:
		capacite_reguliere = capacite_pintade()[3]/len(tab_pondeuse)
		nb_nouvelle_pondeuse = math.ceil(min(nb_oeuf, capacite_reguliere))
		tab_pondeuse[0] = nb_nouvelle_pondeuse
		nb_oeuf -= nb_nouvelle_pondeuse
	return nb_oeuf



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

	simulation_annee_augmenter_terrain()
	argent_augm_int = stock_argent

	stock_argent = stock_argent_temp
	stock_grain = stock_grain_temp
	surface_int = surface_int_temp
	surface_ext = surface_ext_temp
	tab_pondeuse = tab_pondeuse_temp
	tab_standard = tab_standard_temp
	tab_label_rouge = tab_label_rouge_temp

	simulation_annee_augmenter_terrain()
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
	tab_surface_int.append(surface_int)
	tab_surface_ext.append(surface_ext)


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
	if stock_grain < nb_de_pintade*quantite_grain_conso*3: # 3 pour avoir de la marge
		grain_acheter = nb_de_pintade*capacite_sac_grain #on achete un sac de grain par pintade pour etre tranquille pour un moment
		stock_grain += grain_acheter
		stock_argent -= grain_acheter*prix_grain



def simulation_annee_augmenter_terrain():
	for iteration_mois in range(12):
		gestion_des_oeufs()
		acheter_du_grain()
		consommation_de_grain()

def simulation_annee_principale():
	for iteration_mois in range(12):
		gestion_des_oeufs()
		acheter_du_grain()
		consommation_de_grain()
		tab_stock_argent.append(stock_argent)
		tab_stock_grain.append(stock_grain)
		tab_nb_pintade.append(compte_pintade())
		tab_nb_pondeuse.append(compte_pondeuse())
		tab_nb_standard.append(compte_standard())
		tab_nb_label_rouge.append(compte_label_rouge())

def simulation():
	for iteration_annee in range(tps_simulaton):
		simulation_annee_principale()
		choix_augmenter_terrain()
	print "capacite totale = " + str(capacite_pintade()[0]) + ", capacite label rouge = " + str(capacite_pintade()[1]) + ", capacite standard = " + str(capacite_pintade()[2]) + ", capacite pondeuse = " + str(capacite_pintade()[3])
	trace(tab_stock_argent, 421, "argent")
	trace(tab_stock_grain, 422, "grain")
	trace(tab_surface_int, 423, "surface int")
	trace(tab_surface_ext, 424, "surface ext")
	trace(tab_nb_pintade, 425, "nb pintade")
	trace(tab_nb_pondeuse, 426, "nb pondeuse")
	trace(tab_nb_standard, 427, "nb standard")
	trace(tab_nb_label_rouge, 428, "nb label rouge")
	plt.show()

def trace(liste, numero_figure, titre):
		ax = figure.add_subplot(numero_figure)
		abscisse = []
		for iteration in range(len(liste)):
			abscisse.append(iteration)
		abscisses = abscisse
		ordonnees = liste
		title(titre)
		return ax.plot(abscisses, ordonnees, '-')


if __name__ == "__main__":
	pondeuse_initale()
	simulation()