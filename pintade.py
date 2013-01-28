#! /usr/bin/env python
# -*- coding: utf-8 -*-

masse_standard =  1.65 #kg
masse_label_rouge = 2 #kg
masse_vieille = 1.5 #kg

prix_standard = 8 #euros/kg
prix_label_rouge = 12 #euros/kg
prix_vieille = 3 #euros/kg
prix_oeuf = 1 #euro
prix_surface_int = 1000 #euros/m²
prix_surface_ext = 10 #euros/m²
prix_grain = 1 #euros/kg de grain

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

tps = 96 #mois

tab_pondeuse = tps_vie*[0]
tab_standard = tps_maturation_standard*[0]
tab_label_rouge = tps_maturation_label_rouge*[0]

nb_pintade = 0
nb_pondeuse = 0
nb_pondeuse_mature = 0
nb_standard = 0
nb_label_rouge = 0
nb_disparue = 0

#import glpk            # Import the GLPK module
#
#lp = glpk.LPX()        # Create empty problem instance
#lp.name = 'sample'     # Assign symbolic name to problem
#lp.obj.maximize = True # Set this as a maximization problem
#lp.rows.add(3)         # Append three rows to this instance
#for r in lp.rows:      # Iterate over all rows
#	r.name = chr(ord('p')+r.index) # Name them p, q, and r
#lp.rows[0].bounds = None, 100.0  # Set bound -inf < p <= 100
#lp.rows[1].bounds = None, 600.0  # Set bound -inf < q <= 600
#lp.rows[2].bounds = None, 300.0  # Set bound -inf < r <= 300
#lp.cols.add(3)         # Append three columns to this instance
#for c in lp.cols:      # Iterate over all columns
#	c.name = 'x%d' % c.index # Name them x0, x1, and x2
#	c.bounds = 0.0, None     # Set bound 0 <= xi < inf
#lp.obj[:] = [ 10.0, 6.0, 4.0 ]   # Set objective coefficients
#lp.matrix = [ 1.0, 1.0, 1.0,     # Set nonzero entries of the
#             10.0, 4.0, 5.0,     #   constraint matrix.  (In this
#              2.0, 2.0, 6.0 ]    #   case, all are non-zero.)
#lp.simplex()           # Solve this LP with the simplex method
#print 'Z = %g;' % lp.obj.value,  # Retrieve and print obj func value
#print '; '.join('%s = %g' % (c.name, c.primal) for c in lp.cols)
#                       # Print struct variable names and primal values

def gestion_des_oeufs():
	nb_disparu = tab_standard[len(tab_standard)-1] + tab_label_rouge[len(tab_label_rouge)-1] + tab_pondeuse[len(tab_pondeuse)-1]
	nb_oeuf_restant = nb_pondeuse*capacite_ponte - nb_disparu
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
	return capacite_standard_pondeuse, capacite_label_rouge, capacite_totale



def evo_label_rouge():
	vendre_label_rouge()
	for index in range(tab_label_rouge)-1:
		tab_label_rouge[index+1] = tab_label_rouge[index]

def evo_standard():
	vendre_standard()
	for index in range(tab_standard)-1:
		tab_standard[index+1] = tab_standard[index]

def evo_pondeuse():
	vendre_vieille()
	for index in range(tab_pondeuse)-1:
		tab_pondeuse[index+1] = tab_pondeuse[index]



def compte_label_rouge():
	nb_label_rouge = 0
	for index in range(tab_label_rouge)-1:
		nb_label_rouge += tab_label_rouge[index]
	return nb_label_rouge
		
def compte_standard():
	nb_standard = 0
	for index in range(tab_standard)-1:
		nb_standard += tab_standard[index]
	return nb_standard

def compte_pondeuse():
	nb_pondeuse = 0
	for index in range(tab_pondeuse)-1:
		nb_pondeuse += tab_pondeuse[index]
	return nb_pondeuse
		
def compte_pondeuse_mature():
	nb_pondeuse_mature = 0
	for index in range(tab_pondeuse)-tps_maturation_sexuelle:
		nb_pondeuse_mature += tab_pondeuse[index+tps_maturation_sexuelle]
	return nb_pondeuse_mature

def compte_pintade():
	nb_pintade = 0
	nb_pintade = compte_label_rouge() + compte_standard() + compte_pondeuse()
	return nb_pintade



def augmenter_surface_int(surface_ajoutee):
	surface_int += surface_ajoutee
	stock_argent -= surface_ajoutee*prix_surface_int
	
def augmenter_surface_ext(surface_ajoutee):
	surface_ext += surface_ajoutee
	stock_argent -= surface_ajoutee*prix_surface_ext



def vendre_standard():
	stock_argent += tab_standard[tps_maturation_standard]*masse_standard*prix_standard
	tab_standard[tps_maturation_standard] = 0
	
def vendre_label_rouge():
	stock_argent += tab_label_rouge[tps_maturation_label_rouge]*masse_label_rouge*prix_label_rouge
	tab_label_rouge[tps_maturation_label_rouge] = 0 
	
def vendre_vieille():
	stock_argent += tab_pondeuse[tps_vie]*masse_vieille*prix_vieille
	tab_pondeuse[tps_vie] = 0
	
def vendre_oeuf(nb_oeuf_vendu):
	stock_argent += nb_oeuf_vendu*prix_oeuf



def consommation_de_grain(nb_de_pintade):
	stock_grain -= nb_de_pintade*quantite_grain_conso

def acheter_du_grain(grain_en_stock):
	nb_de_pintade = compte_pintade()
	if grain_en_stock < consommation_de_grain(nb_de_pintade):
		grain_acheter = nb_de_pintade*capacite_sac_grain
		stock_grain += grain_acheter
		stock_argent -= grain_acheter*prix_grain
