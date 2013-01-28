#! /usr/bin/env python
# -*- coding: utf-8 -*-

import glpk

tps_vie = 96 #8ans = 96mois
tps_maturation_sexuelle = 7 #mois
tps_maturation_standard = 2 #mois
tps_maturation_label_rouge = 3 #mois

masse_standard =  1.65 #kg
masse_label_rouge = 2 #kg
masse_vieille = 1.5 #kg

capacite_ponte = 8 #oeufs/mois/pintade

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

tps_simulaton = 96 #mois

tab_pondeuse = tps_vie*[0]
tab_standard = tps_maturation_standard*[0]
tab_label_rouge = tps_maturation_label_rouge*[0]

#import glpk            # Import the GLPK module
#
#lp_capacite = glpk.LPX()        # Create empty problem instance
#lp_capacite.name = 'sample'     # Assign symbolic name to problem
#lp_capacite.obj.maximize = True # Set this as a maximization problem
#lp_capacite.rows.add(3)         # Append three rows to this instance
#for r in lp_capacite.rows:      # Iterate over all rows
#	r.name = chr(ord('p')+r.index) # Name them p, q, and r
#lp_capacite.rows[0].bounds = None, 100.0  # Set bound -inf < p <= 100
#lp_capacite.rows[1].bounds = None, 600.0  # Set bound -inf < q <= 600
#lp_capacite.rows[2].bounds = None, 300.0  # Set bound -inf < r <= 300
#lp_capacite.cols.add(3)         # Append three columns to this instance
#for c in lp_capacite.cols:      # Iterate over all columns
#	c.name = 'x%d' % c.index # Name them x0, x1, and x2
#	c.bounds = 0.0, None     # Set bound 0 <= xi < inf
#lp_capacite.obj[:] = [ 10.0, 6.0, 4.0 ]   # Set objective coefficients
#lp_capacite.matrix = [ 1.0, 1.0, 1.0,     # Set nonzero entries of the
#             10.0, 4.0, 5.0,     #   constraint matrix.  (In this
#              2.0, 2.0, 6.0 ]    #   case, all are non-zero.)
#lp_capacite.simplex()           # Solve this LP with the simplex method
#print 'Z = %g;' % lp_capacite.obj.value,  # Retrieve and print obj func value
#print '; '.join('%s = %g' % (c.name, c.primal) for c in lp_capacite.cols)
#                       # Print struct variable names and primal values

def cequilsepasseparmois():
	#gérér les oeufs
	
	evo_label_rouge()
	evo_standard()
	evo_pondeuse()
	consommation_de_grain()
	acheter_du_grain()
	

def gestion_des_oeufs():
	nb_disparu = tab_standard[len(tab_standard)-1] + tab_label_rouge[len(tab_label_rouge)-1] + tab_pondeuse[len(tab_pondeuse)-1]
	nb_oeuf_restant = nb_pondeuse*capacite_ponte - nb_disparu
	if nb_oeuf_restant > 0: #maintenir au minimum le même nombre de pintades dans l'élevage
		if nb_standard_restant + nb_label_rouge_restant + nb_oeuf_restant < capacite_pintade()[2]: #s'il reste de la place dans l'élevage
			#elevage grandi #TODO
			nb_oeuf_restant -= (nb_standard_ajout + nb_label_rouge_ajout)
	
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
	
	lp_capacite.matrix = [ 1.0, 1.0,
	          			   10.0, 4.0]
	lp_capacite.simplex()
	
	print 'Z = %g;' % lp_capacite.obj.value,  # Retrieve and print obj func value
	print '; '.join('%s = %g' % (c.name, c.primal) for c in lp_capacite.cols)	# Print struct variable names and primal values
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


	
def vendre_label_rouge():
	stock_argent += tab_label_rouge[tps_maturation_label_rouge]*masse_label_rouge*prix_label_rouge
	tab_label_rouge[tps_maturation_label_rouge] = 0 

def vendre_standard():
	stock_argent += tab_standard[tps_maturation_standard]*masse_standard*prix_standard
	tab_standard[tps_maturation_standard] = 0
	
def vendre_vieille():
	stock_argent += tab_pondeuse[tps_vie]*masse_vieille*prix_vieille
	tab_pondeuse[tps_vie] = 0
	
def vendre_oeuf(nb_oeuf_vendu):
	stock_argent += nb_oeuf_vendu*prix_oeuf



def consommation_de_grain():
	stock_grain -= compte_pintade()*quantite_grain_conso

def acheter_du_grain():
	nb_de_pintade = compte_pintade()
	if stock_grain < consommation_de_grain(nb_de_pintade):
		grain_acheter = nb_de_pintade*capacite_sac_grain #on achete un sac de grain par pintade pour etre tranquille pour un moment
		stock_grain += grain_acheter
		stock_argent -= grain_acheter*prix_grain
