import matplotlib.pyplot as plt
from numpy import *
from csv_ical import Convert
from fpdf import FPDF
import csv

convert = Convert()
convert.CSV_FILE_LOCATION = 'ADECal.csv'
convert.SAVE_LOCATION = 'ADECal.ics'
convert.read_ical(convert.SAVE_LOCATION)
convert.make_csv()
convert.save_csv(convert.CSV_FILE_LOCATION)
edt = []
with open('ADECal.csv', newline='') as csvfile:
	reader=csv.reader(csvfile, delimiter=',')
	for row in reader:
		edt.append(row)

def indexing(temp_edt) : #Indexage de la liste au format NombresDeJoursHeuresMinutes
	annee = int(temp_edt[1][0])
	mois = int(temp_edt[1][1])
	jour = int(temp_edt[1][2])
	heure = int(temp_edt[1][3])
	index = 0
	if annee == 2022 :
		index += 12200
		if mois == 2 :
			index += 3100
	if mois == 10 :
		index += 3000
	elif mois == 11 :
		index += 6100
	elif mois == 12 :
		index += 9100
	index += (jour * 100)
	index += heure
	return index

#Création d'une liste afin de pouvoir filtré les informations
data_RH = []
clear_edt = []
for i in range(len(edt)) :
	temp_edt = []
	temp = edt[i][3].split("\n")
	temp2 = edt[i][1].replace(' ', '-').replace(':', '-').replace('+', '-').split('-')
	del temp2[-1]
	del temp2[-1]
	del temp2[-1]
	temp3 = edt[i][2].replace(' ', '-').replace(':', '-').replace('+', '-').split('-')
	del temp3[-1]
	del temp3[-1]
	del temp3[-1]
	data_RH.append(temp[-2])
	temp_edt.append(temp[-2])
	temp_edt.append(temp2)
	temp_edt.append(temp3)
	temp_edt.append(edt[i][0])
	del temp[-1]
	del temp[-1]
	temp_edt.append(temp)
	temp_edt.append(indexing(temp_edt))
	clear_edt.append(temp_edt)
clear_edt.sort(key=lambda clear_edt:clear_edt[5]) #Trie de la liste de manière croissante grace à l'indexage

def check_name(name) : #vérifier si l'enseignant figure dans l'emploie du temps
	for i in data_RH :
		if i == name :
			return True
	return False

def name_acquire() : #acquisition du nom de l'enseignant
	while True :
		name = input("Tappez votre nom de famille en majuscule, ajoutez un espace et tappez votre prénom en majuscule\n")
		if check_name(name) == True :
			return name
		else :
			print("Votre entrée ne correspond pas")

final_name = name_acquire()
print("Bienvenue %s vous avez subit notre SUPER gestionnaire de vacances !\nVous pouvez retrouver les documents associés au format png et pdf, bonne vacances !"%final_name)
#Création de la liste contenant uniquement l'emploie du temps de l'esneignant
client_edt = []
for i in clear_edt :
	if i[0] == final_name :
		client_edt.append(i)
i = 1

#Création de la liste contenant que les derniers cours et cours de reprises de l'enseignant
holidays = []
days_in_holidays = []
while i < len(client_edt) :
	if (client_edt[i][5] - client_edt[i-1][5]) > 800 : #Si l'enseignant n'a pas de cours pendant plus de 8 jours on le considère en vacances
		holidays.append(client_edt[i-1])
		holidays.append(client_edt[i])
		temp_value = (client_edt[i][5]//100) - (client_edt[i-1][5]//100) - 2
		days_in_holidays.append([temp_value, temp_value * 24, temp_value * 24* 60, temp_value * 24 * 60 * 60])
	i += 1
for i in range(len(holidays)) :
	if i%2 == 0 :
		holidays[i].insert(0, "Dernier cours")
	else :
		holidays[i].insert(0, "Cours de reprise")

#Création d'une liste contenant uniquement des chaines de caractères pour créer le tableau dans le pdf 
pdf_list = []
j = 0
for i in holidays :
	temp_list = []
	temp_list.append(i[0])
	temp_list.append(i[4])
	temp_str = "Elèves du groupe %s"%', '.join(i[5])
	temp_list.append(temp_str)
	temp_str = "Commence le : %s/%s/%s à %sh%s"%(i[2][0], i[2][1], i[2][2], i[2][3], i[2][4])
	temp_list.append(temp_str)
	temp_str = "Termine le : %s/%s/%s à %sh%s"%(i[3][0], i[3][1], i[3][2], i[3][3], i[3][4])
	temp_list.append(temp_str)
	if (j%2) != 0 :
		pdf_list.append(["Période de vacances", "%s jours complets"%days_in_holidays[j//2][0], "Soit %s heures"%days_in_holidays[j//2][1], "Soit %s minutes"%days_in_holidays[j//2][2], "Soit %s secondes"%days_in_holidays[j//2][3]])
	pdf_list.append(temp_list)
	j += 1

#print(pdf_list)
	
#Création du pdf contenant un tableau
pdf = FPDF()
pdf.add_page()
pdf.set_font("Times", size=9)
line_height = pdf.font_size * 4
col_width = pdf.epw / 5
for row in pdf_list:
	for i in row:
		pdf.multi_cell(col_width, line_height, i, border=1, align='C',new_x="RIGHT", new_y="TOP", max_line_height=pdf.font_size)
	pdf.ln(line_height)
pdf.output("Vacances_%s.pdf"%final_name)

#On compte le nombre de jours ouvrés et donc de jours non ouvrés
work_days = 0
day_check = 0
work_or_not = []
for i in client_edt :
	if i[0] != final_name :
		if day_check != int(i[6]) // 100 :
			work_days += 1
			day_check = int(i[6] // 100)
			work_or_not.append(int(i[6] // 100))
	else :
		if day_check != int(i[5]) // 100 :
			work_days += 1
			day_check = int(i[5] // 100)
			work_or_not.append(int(i[5] // 100))
day_off = (clear_edt[-1][5] // 100) - work_days
#print(day_off, work_days)

name = ['Jours non ouvrés', 'Jours ouvrés']
data = [day_off, work_days]

#On crée le diagramme circulaire des Jours ouvrés/Jours non ouvrés
plt.figure(1)
explode=(0, 0.15)
plt.pie(data, explode=explode, labels=name, autopct='%1.1f%%', startangle=90, shadow=True)
plt.suptitle("RT IUT-AUXERRE\nSemestre 1 année 2021-2022\n%s"%final_name)
plt.axis('equal')
plt.savefig('Diagramme_circulaire%s.png'%final_name)

#On crée une liste de jours non ouvrés par mois pour l'histogramme et on le sauvegarde au format png
day_off_list = []
day_off_stack = 0
i = 1
while i <= 171 :
	if i not in work_or_not :
		day_off_stack += 1
	if (i%30) == 0 :
		day_off_list.append(day_off_stack)
		day_off_stack = 0
	i += 1

#print(day_off_list)

#On crée notre histogramme du nombre de mois comprennant un certain nombre de jours non ouvrés et on le sauvegarde au format png
plt.figure(2)
plt.suptitle("Jours non ouvrés par mois\nSemestre 1 année 2021-2022\n%s"%final_name)
plt.ylabel('Mois')
plt.xlabel('Jours non ouvrés')
plt.hist(day_off_list, len(day_off_list), edgecolor = 'white')
plt.savefig('Histogramme_%s.png'%final_name)

#On crée une liste de jours non ouvrés par mois pour le diagramme de barres
day_off_list2 = []
day_off_stack = 0
i = 1
while i <= 171 :
	if i not in work_or_not :
		day_off_stack += 1
	if (i%7) == 0 :
		day_off_list2.append(day_off_stack)
		day_off_stack = 0
	i += 1
x_axis = [ i for i in arange(0, len(day_off_list2), 1)]

#Création du diagramme de barres et sauvegarde au format png
plt.figure(3)
plt.suptitle("Jours non ouvrés par semaines\nSemestre 1 année 2021-2022\n%s"%final_name)
plt.bar(x_axis, day_off_list2)
plt.ylabel('Jours non ouvrés')
plt.xlabel('Semaines')
plt.savefig('Diagramme_de_barres_%s.png'%final_name)