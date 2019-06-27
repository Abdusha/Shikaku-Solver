# Shikaku-Solver
Pencarian solusi Shikaku menggunakan pendekatan logika proposisi dalam Python

Pereangkat yang digunakan:
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
	0|   4    |       |       |       |
	 ----------------------------------
	1|        |   4   |       |       |
	 ----------------------------------
	2|        |       |   4   |       |
	 ----------------------------------
	3|        |       |       |   4   |
	 ----------------------------------
