import time
import pycosat
from tkinter import *
from tkinter.filedialog import askopenfilenames
import tkinter.messagebox
from satispy import CnfFromString

root = Tk()
# Mengatur ukuran window (px)
root.geometry("400x615") #WxH
root.title('Shikaku Solver')

res=[]
cell_id = []
hasilAkhir = []
hasilFinal = []
isiHint = []

# Membuat function open_multiple_files()
def open_file():
    root.file = askopenfilenames(parent=root, title='Pilih file',filetypes=[("Text files","*.txt")])
    for i in root.file:
          Label(root, text=i).pack()
    isi = open(root.file[0]).readlines()

    NxN = len(isi)*(len(isi[0])-1)
    N = len(isi)
    print(N,NxN) 
    sumHint = 0 
    
    for i in range(0,N):
        for j in range(0,N):
            if (int(isi[i][j]) != 0):
                sumHint += int(isi[i][j])
    if(sumHint == NxN):
        show_shikaku(isi)
    else:
        print("Salah")
        Label(root, text="Papan Shikaku tidak sesuai aturan!", font='40').pack()

def baseN(r, c, v):
    return 1000 * (r - 1) + 100 * (c - 1) + v

def konversiCell(hint,N):
	for r in range(1, N+1):
		for c in range(1, N+1):		
			for d in range(1, hint+1):
				cell_id.append([r,c,baseN(r,c,d)])
	return cell_id

##===================================Aturan==================================================##

def aturan1(hint,N):
	for r in range(1, N+1):
		for c in range(1, N+1):
			l = []		
			for d in range(1, hint+1):
				l.append(baseN(r,c,d))
			res.append(l)
	for r in range(1, N+1):
		for c in range(1, N+1):
			l =[]		
			for d in range(1, hint+1):
				l.append(-baseN(r,c,d))
			res.append(l)
	for r in range(1, N+1):
		for c in range(1, N+1):	
			for d in range(1, hint+1):
				for e in range(1, hint+1):
					#print "[",d,e,"]"
					if e != d:
						l =[]
						l.append(-baseN(r,c,d))
						l.append(-baseN(r,c,e))
						res.append(l)
	return res

def aturan2(hint,N):
	#phi = []
	phi1=[]
	for r in range(1, N):
		for c in range(1, N):
			#print r,c
			for d in range(1, hint+1):
				l =[]		
				l.append(baseN(r,c,d))
				l.append(-baseN(r+1,c,d))
				l.append(-baseN(r,c+1,d))
				l.append(-baseN(r+1,c+1,d))
				phi1.append(l)
	
	phi2=[]
	for r in range(1, N):
		for c in range(1, N):
		
			for d in range(1, hint+1):		
				l =[]
				l.append(-baseN(r,c,d))
				l.append(baseN(r+1,c,d))
				l.append(-baseN(r,c+1,d))
				l.append(-baseN(r+1,c+1,d))
				phi2.append(l)

	phi3=[]
	for r in range(1, N):
		for c in range(1, N):
			for d in range(1, hint+1):
				l =[]
				l.append(-baseN(r,c,d))
				l.append(-baseN(r+1,c,d))
				l.append(baseN(r,c+1,d))
				l.append(-baseN(r+1,c+1,d))
				phi3.append(l)

	phi4=[]
	for r in range(1, N):
		for c in range(1, N):
			for d in range(1, hint+1):
				l =[]
				l.append(-baseN(r,c,d))
				l.append(-baseN(r+1,c,d))
				l.append(-baseN(r,c+1,d))
				l.append(baseN(r+1,c+1,d))
				phi4.append(l)
                
	for i in range(0,len(phi1)):
		res.append(phi1[i])
		res.append(phi2[i])
		res.append(phi3[i])
		res.append(phi4[i])
	return res


def cLuas(indexHasil,hint,isiHint):
	cekArea = TRUE
	for i in range(1,hint+1):
		temp = []
		for j in range(0,len(indexHasil)):
			if(indexHasil[j][2]==i):
				temp.append(indexHasil[j])
		# print("Temp:",temp)
		rBig = temp[0][0]
		rSmall = temp[0][0]
		cBig = temp[0][1]
		cSmall = temp[0][1]
		for k in range(0, len(temp)):
			if(temp[k][0] >= rBig):
				rBig = temp[k][0]
			if(temp[k][0] <= rSmall):
				rSmall = temp[k][0]
			if(temp[k][1] >= cBig):
				cBig = temp[k][1]
			if(temp[k][1] <= cSmall):
				cSmall = temp[k][1]
		luas = ((rBig-rSmall)+1)*((cBig-cSmall)+1)
		if(isiHint[i-1] != luas):
			cekArea = FALSE
	return cekArea

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def createDnf(N,h,isiHint):
    all = []
    for a in range(1,N+1):
        for b in range(1,N+1):
            if (a*b == isiHint[h-1]):
                # all = []
                ell = []
                # print(a,"x",b,"id:",h,"=================================================")
                for r in range(0,N-a+1):
                    for c in range(0,N-b+1):
                        # iterasi = []
                        dimacss = []
                        for k in range(0,a):
                            for l in range(0,b):
                                # iterasi.append([r+k+1,c+l+1])
                                dimacss.append(baseN(r+k+1,c+l+1,h))
                        ell.append(dimacss)
                # print("ELL:",len(ell),"=",ell)
                for i in range(0,len(ell)):
                    all.append(ell[i])
    return all

def convertToCnF(reg):
    char = ""
    for i in range(0,len(reg)):
        char = char+"("
        for j in range(0,len(reg[i])):
            char = char+str(reg[i][j])
            if(j < len(reg[i])-1):
                char = char+" & "
        char = char+")"
        if(i < len(reg)-1):
            char = char+" | "

    exp, symbol = CnfFromString.create(char)
    r = str(exp)
    r = r.replace('(','')
    r = r.replace(')','')
    arr = r.split('&')
    aw = []
    for i in range(0,len(arr)):
            aw.append(arr[i].split('|'))
    for i in range(0,len(aw)):
            for j in range(0,len(aw[i])):
                    aw[i][j] = int(aw[i][j])
    # print(aw)
    # print(type(aw[0][0]))
    return aw

def aturan3(N,hint,isiHint):
	# print("ini hint:",hint)
	# print("ini isi hint:",isiHint)
	for h in range(1,hint+1):
		reg = createDnf(N,h,isiHint)
		cnf_ = convertToCnF(reg)
		print("cnf :",len(cnf_))
		for i in range(0,len(cnf_)):
			res.append(cnf_[i])
	return res

##===================================Aturan==================================================##

def satSolver(res,cell_id,hint,N):
	cnf = res
	sol = pycosat.solve(cnf)
	solusi = [] #id konversi variabel cnf
	hasil = [] #konversi kedalam bentuk normal hasil(r,c,id)
	for i in range(0,len(cell_id)):
		for j in range(0,len(sol)):
			if cell_id[i][2] == sol[j] and sol[j]>0:
				if (sol[j]-((cell_id[i][0]*1000)+(cell_id[i][1]*100))<hint+1):
					solusi.append(sol[j])
	for i in range(0,len(cell_id)):
		for j in range(0,len(solusi)):
			if(cell_id[i][2] == solusi[j]):
				hasil.append([cell_id[i][0]-1,cell_id[i][1]-1,cell_id[i][2]-(((cell_id[i][0]-1)*1000)+((cell_id[i][1]-1)*100))])
	if sol!='UNSAT':
		ss = []
		for i in range(len(sol)):
			if(sol[i]>0):
				x = sol[i]*-1
				ss.append(x)		
	else:
		ss = []
	return hasil,ss

def cekHasilAkhir(hasilAkhir,hint,isiHint):
	if(len(hasilAkhir)>0):
		for i in range(0,len(hasilAkhir)):
			cekArea = cLuas(hasilAkhir[i],hint,isiHint)
			if(cekArea == TRUE):
				hasilFinal.append(hasilAkhir[i])
		print("Hasil Final ini loh",hasilFinal)		
	else:
		print("tidak memiliki solusi")

def show_shikaku(isi):
	N = len(isi)
	hint = 0
	cell = [[0 for x in range(N)] for x in range(N)]
	petunjuk = []
	Label(root, text="Papan Shikaku:").pack()
	Label(root, text="====================================").pack()
	for i in range(0,N):
		for j in range(0,N):
			if(int(isi[i][j]) > 0):
				hint += 1
				cell[i][j] = [int(isi[i][j]),hint]
				petunjuk.append([baseN(i+1,j+1,hint)])
			else:
				cell[i][j] = [int(isi[i][j]),0]
		print(cell[i])
		Label(root, text=cell[i], font='32').pack()
	for i in range(0,len(cell)):
		for j in range(0,len(cell[i])):
			if(cell[i][j][0]!=0):
				isiHint.append(cell[i][j][0])
	for i in range(0, len(petunjuk)):
		res.append(petunjuk[i])
	Label(root, text="====================================").pack()
	button2 = Button(root, text="Cari Solusi", command= lambda: runAturan(N,hint,isiHint,petunjuk,cell,cell_id)).pack()

def runAturan(N,hint,isiHint,petunjuk,cell,cell_id):
	start = time.time()
	aturan1(hint,N)
	# aturan2(hint,N)
	aturan3(N,hint,isiHint)

	cell_id = konversiCell(hint,N) #Konversi tiap id pada tiap cell
	for i in range(0,5): #^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^GANTI^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
		cariHasil(cell,cell_id,petunjuk,hint,N)
	cekHasilAkhir(hasilAkhir,hint,isiHint)
	end = time.time()
	print("\nrunning",(end-start),"detik")
	print("")
	final(hasilFinal,cell,N)

def cariHasil(cell,cell_id,petunjuk,hint,N):
	h = satSolver(res, cell_id,hint,N)
	hasil = h[0]
	ss = h[1]
	
	if(len(hasil)>0):
		hasilAkhir.append(hasil)
	if(len(ss)>0):
		res.append(ss)

def final(hasilAkhir,cell,N):
	cell_b = cell
	if(len(hasilAkhir)>0):
		for i in range(0,len(hasilAkhir)):
			for j in range (0,len(hasilAkhir[i])):
				cell_b[hasilAkhir[i][j][0]][hasilAkhir[i][j][1]][1] = hasilAkhir[i][j][2]	
			print("#Output:")
			Label(root, text="====================================").pack()
			for i in range(0,N):
				print(cell_b[i])
				Label(root, text=cell[i], font='32').pack()
			Label(root, text="====================================").pack()
	else:
		Label(root, text="Tidak memiliki jawaban!").pack()

# scroll = Scrollbar()
# scroll.pack(side=RIGHT, fill=Y)
label1 = Label(root, text="Silahkan memilih file Shikaku dengan format .txt")
button1 = Button(root, text="Pilih file", command=open_file)
label1.pack(pady=10)
button1.pack(pady=10)

root.mainloop()