#  LINGUISTIC INPUT  |---------------------------------------|
#  Jumlah Follower   |      SEDIKIT  |   SEDANG     |  BANYAK|
#  Engagement Rate   |      KECIL    |   SEDANG     |  BESAR |
#  LINGUISTIC OUTPUT |---------------------------------------|
#  Acceptance        |      YA       |   TERGANTUNG |  TIDAK |

#  output membership
#  fol/emgage         kecil	       sedang 	      besar

#  sedikit			  Tidak        Tidak          Tergantung

#  sedang			  Tidak	       Tergantung     Ya

#  banyak			  Tergantung    Ya 	          Ya

import csv
with open('influencers.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            print(f'\t{row[0]}. Jumlah Follower = {row[1]} dan Engagement rate = {row[2]}.')
            line_count += 1
    print(f'Processed {line_count} lines.')


#  FUZZI
def FolSedikit(x):
    if (x <= 15000):
        return 1
    elif(x <= 20000):
        return -(x - 20000)/(20000 - 15000)
    else:
        return 0

def FolSedang(x):
    if (x < 15000 or x > 50000):
        return 0
    elif (15000 < x < 20000):
        return (x - 15000)/(20000 - 15000)
    elif (20000 <= x <= 40000):
        return 1
    elif (40000 < x < 50000):
        return -(x - 50000)/(50000 - 40000)

def FolBanyak(x):
    if (x < 40000):
        return 0
    elif(x >= 50000):
        return 1
    elif(40000 < x < 50000):
        return (x - 40000) / (50000 - 40000)

def Fol_Score(x):
    Fsedikit = FolSedikit(x)
    Fsedang = FolSedang(x)
    Fbanyak = FolBanyak(x)
    return Fsedikit, Fsedang, Fbanyak

def EngageKecil(x):
    if (x <= 2):
        return 1
    elif (2 < x < 3):
        return -(x - 3) / (3 - 2)
    else:
        return 0

def EngageSedang(x):
    if(x <1 or x >5):
        return 0
    elif(2 <= x <= 4):
        return 1
    elif(1 <= x < 2):
        return (x-1)/(2 - 1)
    elif(4 < x <= 5):
        return -(x - 5) / (5 - 4)

def EngageBesar(x):
    if (x < 4):
        return 0
    elif (x >= 5):
        return 1
    elif (4 <= x < 5):
        return (x - 4)/(5 - 4)

def Eng_Score(x):
    Ekecil = EngageKecil(x)
    Esedang = EngageSedang(x)
    Ebesar = EngageBesar(x)
    return Ekecil, Esedang, Ebesar

def inferensi(Fsedikit, Fsedang, Fbanyak, Ekecil, Esedang, Ebesar):
    inf = [ [min(Fsedikit,Ekecil), 'Tidak'], [min(Fsedikit,Esedang), 'Tidak']     , [min(Fsedikit,Ebesar),'Tergantung'],
    	 	[min(Fsedang, Ekecil), 'Tidak'], [min(Fsedang, Esedang), 'Tergantung'], [min(Fsedang, Ebesar), 'Iya'],
    		[min(Fbanyak, Ekecil), 'Tergantung'], [min(Fbanyak, Esedang), 'Iya']       , [min(Fbanyak, Ebesar), 'Iya']]

    Iya = []
    Tergantung = []
    Tidak = []
    for x in range(len(inf)):
        if inf[x][1] == 'Iya':
            Iya.append(inf[x][0])
        elif inf[x][1] == 'Tergantung':
            Tergantung.append(inf[x][0])
        elif inf[x][1] == 'Tidak':
            Tidak.append(inf[x][0])
    return max(Iya), max(Tergantung), max(Tidak)


# DEFUZZI
def defuzzy(Iya, Tergantung, Tidak):
    return ((Iya * 80) + (Tergantung * 40) + (Tidak * 20)) / (Iya + Tergantung + Tidak + 0.000001)


# MAIN
output_Defuzi = []
influecer_chosen = []
followers = []
engagement = []

with open('influencers.csv', mode='r') as csv_input:
    influencers_data = csv.reader(csv_input)
    next(influencers_data)
    for row in influencers_data:
        followers.append(float(row[1]))
        engagement.append(float(row[2]))

for i in range(len(followers)):
    FSedikit, FSedang, Fbesar = Fol_Score(followers[i])
    Ekecil, Esedang, Ebesar = Eng_Score(engagement[i])
    Iya, Tergantung, Tidak = inferensi(FSedikit, FSedang, Fbesar, Ekecil, Esedang, Ebesar)
    score = defuzzy(Iya, Tergantung, Tidak)
    output_Defuzi.append([score, (i + 1)])

output_Defuzi.sort(reverse=True)

for i in range(0, 20):
    influecer_chosen.append(output_Defuzi[i][1])

with open('chosen.csv', mode="w") as csv_output:
    output = csv.writer(csv_output, lineterminator='\n')
    for data in influecer_chosen:
        output.writerow([data])
print("hasil defuzzifikasi semua data: ",output_Defuzi)


for i in range (len(output_Defuzi[0:20])):
    print(i+1, output_Defuzi[i])
# print("20 influencers terpilih: ",output_Defuzi[0:20])


