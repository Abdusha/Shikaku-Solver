# Shikaku-Solver
Pencarian solusi Shikaku menggunakan pendekatan logika proposisi dalam Python

Perangkat yang digunakan:
- Python 3.7.1
- Pycosat 0.6.3
- Satispy 1.0


Program menerima masukan berupa dokumen dalam format .txt. Isi dari dokumen tersebut berupa matriks NxN yang mewakili papan Shikaku.
Contoh:

	4000
	0400
	0040
	0004

Matriks diatas adalah masukan yang mewakili bentuk Shikaku 4x4. Berikut adalah ilustrasinya:


	     0        1       2       3
	 ----------------------------------
	0|   4   |       |       |       |
	 ----------------------------------
	1|       |   4   |       |       |
	 ----------------------------------
	2|       |       |   4   |       |
	 ----------------------------------
	3|       |       |       |   4   |
	 ----------------------------------
	 
Bilangan bulat positif >= 1 mewakili petunjuk dan 0 mewakili sel kosong pada papan Shikaku. Kemudian petunjuk akan diberikan id untuk membedakan satu sama lain karena nilai petunjuk mungkin saja sama. Berikut ini adalah ilustrasi petunjuk Shikaku yang sudah diberikan id:

	     0        1       2       3
	 ---------------------------------
	0|  4,1  |       |       |       |
	 ---------------------------------
	1|       |  4,2  |       |       |
	 ---------------------------------
	2|       |       |  4,3  |       |
	 ---------------------------------
	3|       |       |       |  4,4  |
	 ---------------------------------
	 
Pada sel yang memiliki petunjuk sisi kiri mewakili nilai petunjuk dan sisi kanan mewakili id petunjuk. Contoh pada sel p(0,0) berisi bilangan (4,1), angka 4 mewakili nilai petunjuk dan angka 1 mewakili id petunjuk pada sel p(0,0).
