# Melakukan import library random dan library math untuk operasi sin dan cos pada fungsi
import random
from math import sin, cos

# Membuat array untuk data batas x dan y
batas_x = [-5, 5]
batas_y = [-5, 5]

# Fungsi pembuatan populasi beserta kromosom-kromosomnya
def generate_populasi(n_populasi, n_kromosom):
    return [[(random.randint(0,9)) for _ in range(n_kromosom)] for _ in range(n_populasi)]

# Fungsi membagi kromosom menjadi 2 bagian yaitu bagian kiri adalah x dan bagian kanan adalah y
def bagi_kromosom(kromosom):
    bagi = len(kromosom) // 2
    return kromosom[:bagi], kromosom[bagi:]

# Fungsi rumus yang akan dicari nilai minimumnya
def function(x,y):
    return (1/(((cos(x)+sin(y))**2/(x**2 + y**2))+ 0.01)) #sesuai soal dengan menggunakan rumus 1/h+a

# Fungsi decode untuk setiap kromosom pada suatu populasi
def decode(kromosom, batas) :
    kali = 0
    pembagi = 0
    for i in range(len(kromosom)) :
        num = kromosom[i]
        kali += num * (10**-(i+1))
        pembagi += 9 * (10**-(i+1))

    return batas[0] + (((batas[1] - batas[0]) / pembagi) * kali) #representasi integer angka 0-9

# Fungsi untuk menentukan kromosom terbaik
def seleksi_kromosom_terbaik(populasi):
    max_fitness = -999
    
    for kromosom in populasi:
        kromosom_a, kromosom_b = bagi_kromosom(kromosom)
        x1 = decode(kromosom_a, batas_x)
        x2 = decode(kromosom_b, batas_y)
        fitness = function(x1, x2)
        
        if  max_fitness < fitness:
            max_fitness = fitness
            max_kromosom = kromosom
      
    return max_kromosom, max_fitness, x1, x2

# Fungsi untuk melakukan proses seleksi orang tua (parent) menggunakan cara roulette whell
def seleksi_roulette_whell(populasi, fitness, fitness_total):
    r = random.random()
    i = 0
    while r > 0:
      r -= fitness[i]/fitness_total
      i += 1
      if  i == len(populasi) - 1:
          break
          
    return populasi[i]

# Fungsi untuk melakukan proses crossover anak
def crossover(ortu_1, ortu_2) :         
    anak_1, anak_2, child = [], [], []
    pc = random.random() #pc = satu titik potong

    if pc < 0.9:
      anak_1[:1], anak_1[1:] = ortu_1[:1], ortu_2[1:]   
      anak_2[:1], anak_2[1:] = ortu_2[:1], ortu_1[1:]
      child.append(anak_1)
      child.append(anak_2)
    else:   
      child.append(ortu_1)
      child.append(ortu_2)

    return child

# Fungsi untuk melakukan proses mutasi pada anak
def mutasi(anak_1, anak_2):
    for i in range(len(anak_1)):
        p = random.random()
        if p < 0.1:
           anak_1[i] = random.randint(0,9)

        q = random.random()
        if q < 0.1:
           anak_2[i] = random.randint(0,9)
           
    return anak_1, anak_2

# Fungsi seleksi_survivor untuk memasukkan kromosom terbaik pada generasi sebelumnya
def seleksi_survivor(populasi, generasi_kromosom_terbaik, kromosom_terburuk, total_fitness):
    if  generasi_kromosom_terbaik[1] > kromosom_terburuk[0] and (generasi_kromosom_terbaik[0] not in populasi):
        populasi[kromosom_terburuk[2]] = generasi_kromosom_terbaik[0]
        total_fitness = (total_fitness - kromosom_terburuk[0]) + generasi_kromosom_terbaik[1]
        
        print('\nProses seleksi_survivor')
        print(f'Kromosom Ke-{kromosom_terburuk[2]+1}: {kromosom_terburuk[1]}, fitness: {kromosom_terburuk[0]}')
        print(f'diganti oleh   {generasi_kromosom_terbaik[0]}, fitness: {generasi_kromosom_terbaik[1]}\n')

    return populasi, total_fitness

#ini adalah fungsi utama/main
# Inisialisasi Jumlah populasi, generasi serta pemanggilan fungsi untuk membuat populasi
generasi = 30
n_populasi = 10
n_kromosom = 10

populasi = generate_populasi(n_populasi, n_kromosom)
print("Populasi Awal:", populasi)

generasi_kromosom_terbaik = []

# Perulangan untuk melakukan proses seleksi populasi
for gen in range(generasi):

      # Inisialisasi variabel untuk proses perhitungan algoritma genetika
      data_kromosom, kromosom_terbaik, kromosom_terburuk, data_fitness, populasi_baru, child = [], [], [], [], [], []
      total_fitness, jumlah_kromosom, index = 0, 999, 0
      
      print('\n================================================================')
      print('GENERASI', gen+1)
      print('================================================================')
      # Perulangan untuk mencari nilai phenotype dan nilai fungsi / fitness pada setiap kromosom 
      for i, kromosom in enumerate(populasi):                         
          kromosom_a, kromosom_b = bagi_kromosom(kromosom)
          x1 = decode(kromosom_a, batas_x)
          x2 = decode(kromosom_b, batas_y)

          nilai_fitness = function(x1, x2)
          data_fitness.append(nilai_fitness)
          total_fitness += nilai_fitness
          
          # Pencarian Fitness Terkecil Dalam Suatu Generasi
          if gen != 0 and nilai_fitness < jumlah_kromosom:
                  jumlah_kromosom = nilai_fitness
                  kromosom_terburuk = [nilai_fitness, kromosom, i]

             
      # Pemilihan Kromosom Dengan Fitness Terbaik
      kromosom_terbaik = seleksi_kromosom_terbaik(populasi)

      print("Kromosom Terbaik :", kromosom_terbaik[0])
      print("Fitness Terbaik  :", kromosom_terbaik[1])

      # Proses seleksi_survivor untuk memasukkan kromosom terbaik pada generasi sebelumnya
      if gen != 0:
         hasil_terbaik = sorted(generasi_kromosom_terbaik, key=lambda x: x[1], reverse=True)[0]
         populasi, total_fitness = seleksi_survivor(populasi, hasil_terbaik, kromosom_terburuk, total_fitness)

      generasi_kromosom_terbaik.append(kromosom_terbaik)

      # Perulangan untuk melakukan seleksi orang tua, crossover dan mutasi anak untuk mendapatkan populasi generasi selanjutnya
      if  gen != generasi-1 :
          for i in range(n_populasi // 2):
              ortu_1 = seleksi_roulette_whell(populasi, data_fitness, total_fitness)
              ortu_2 = seleksi_roulette_whell(populasi, data_fitness, total_fitness)

              child = crossover(ortu_1, ortu_2)
              anak_1, anak_2 = mutasi(child[0], child[1])

              populasi_baru.append(anak_1)
              populasi_baru.append(anak_2)

          populasi = populasi_baru

# Memanggil fungsi untuk menentukan kromosom terbaik pada keseluruhan generasi
print('===============================================================================')
print('===                     KELOMPOK 7 || IF-44-10                              ===')
print('===             Berlian Muhammad Galin Al Awienoor (1301204378)             ===')
print('===             Kiki Dwi Prasetyo                  (1301204027)             ===')
print('===============================================================================')

print('\n=====================================================')
print('           HASIL AKHIR KROMOSOM TERBAIK')
print('=====================================================')
print('Kromosom Terbaik   = ', hasil_terbaik[0])
print('x                  = ', hasil_terbaik[2])
print('y                  = ', hasil_terbaik[3])
print('Nilai Fitness      = ', hasil_terbaik[1])
print('=====================================================')