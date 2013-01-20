#! /usr/bin/env python
# -*- coding: utf-8 -*-

#option solver "./minos";
#model "./pintade.mod";
#data "./pintade.dat";
#solve;

masse_standard =  1.65 #kg
masse_label_rouge = 2 #kg
masse_vieille = 1.5 #kg

prix_standard = 8 #euros/kg
prix_label_rouge = 12 #euros/kg
prix_vieille = 3 #euros/kg
prix_oeuf = 1 #euro
prix_surface_int = 1000 #euros/m²
prix_surface_ext = 10 #euros/m²

tps_vie = 96 #8ans = 96mois
tps_maturation_sexuelle = 7 #mois
tps_maturation_standard = 2 #mois
tps_maturation_label_rouge = 3 #mois

capacite_ponte = 8 #oeufs/mois/pintade

capacite_sac_grain = 25 #kg
quantite_grain_conso = 1.5 #kg de grain/mois/pintade

stock_argent = 5000 #euros
stock_grain = 500 #kg
surface_int = 200 #m²
surface_ext = 200 #m²

nb_pintade
nb_pondeuse
nb_standard
nb_label_rouge
nb_mature
nb_disparue

tps = 96 #mois

tab_pondeuse = tps_vie*[0]
tab_standard = 3*[0]
tab_label_rouge = 2*[0]

def evo_label_rouge():
	vendre_label_rouge(tab_label_rouge[len(tab_label_rouge)-1])
	for index in range(tab_label_rouge)-1:
		tab_label_rouge[index+1] = tab_label_rouge[index]

def evo_standard():
	vendre_standard(tab_standard[len(tab_standard)-1])
	for index in range(tab_standard)-1:
		tab_standard[index+1] = tab_standard[index]

def evo_pondeuse():
	vendre_vieille(tab_pondeuse[len(tab_pondeuse)-1])
	for index in range(tab_pondeuse)-tps_maturation_sexuelle:
		nb_mature += tab[index+tps_maturation_sexuelle]
	for index in range(tab_pondeuse)-1:
		tab_pondeuse[index+1] = tab_pondeuse[index]



def gestion_des_oeufs():
	nb_oeuf_restant = nb_mature*capacite_ponte - (tab_standard[len(tab_standard)-1] + tab_label_rouge[len(tab_label_rouge)-1] + tab_pondeuse[len(tab_pondeuse)-1])
	if nb_oeuf_restant > 0: #maintenir au minimum le même nombre de pintades dans l'élevage
		
		if nb_standard_restant + nb_label_rouge_restant + nb_oeuf_restant < capacite_pintade()[2]: #s'il reste de la place dans l'élevage
			#elevage grandi #TODO
			nb_oeuf_restant -= (nb_standard_ajout + nb_label_rouge_ajout)
	
	vendre_oeuf(nb_oeuf_restant)

#ancienne version
#def gestion_des_oeufs(nb_standard_vendues, nb_label_rouge_vendues, nb_vieille_vendues, nb_matures):
	#nb_oeufs_restant = nb_matures*capacite_ponte - (nb_standard_vendues + nb_label_rouge_vendues + nb_vieille_vendues)
	#if nb_oeufs_restant > 0: #maintenir au minimum le même nombre de pintades dans l'élevage
		
		#if nb_standard_restant + nb_label_rouge_restant + nb_oeufs_restant < capacite_pintade()[2]: #s'il reste de la place dans l'élevage
			##elevage grandi #TODO
			#nb_oeufs_restant -= (nb_standard_ajout + nb_label_rouge_ajout)
	
	#vendre_oeuf(nb_oeufs_restant)

def capacite_pintade(surface_int, surface_ext):
	#TODO
	#option1 solver1 "./minos";
	#model1 "./capacite.mod";
	#data1 "./capacite.dat";
	#solve;
	return capacite_standard_pondeuse, capacite_label_rouge, capacite_totale


def augmenter_surface_int(surface_ajoutee):
	surface_int += surface_ajoutee
	stock_argent -= surface_ajoutee*prix_surface_int
	
def augmenter_surface_ext(surface_ajoutee):
	surface_ext += surface_ajoutee
	stock_argent -= surface_ajoutee*prix_surface_ext

def vendre_standard(nb_standard_vendue):
	nb_standard -= nb_standard_vendue
	stock_argent += nb_standard_vendue*masse_standard*prix_standard
	
def vendre_label_rouge(nb_label_rouge_vendue):
	nb_label_rouge -= nb_label_rouge_vendue
	stock_argent += nb_label_rouge_vendue*masse_label_rouge*prix_label_rouge
	
def vendre_vieille(nb_vieille_vendue):
	nb_pondeuse -= nb_vieille_vendue
	stock_argent += nb_vieille_vendue*masse_vieille*prix_vieille
	
def vendre_oeuf(nb_oeuf_vendu):
	stock_argent += nb_oeuf_vendu*prix_oeuf

def consommation_de_grain(nb_de_pintade):
	stock_grain -= nb_de_pintade*quantite_grain_conso

def acheter_du_grain(grain_en_stock):
	if grain_en_stock < consommation_de_grain(nb_de_pintade):
		grain_acheter = nb_de_pintade*capacite_sac_grain
		stock_grain += grain_acheter
		stock_argent -= grain_acheter
