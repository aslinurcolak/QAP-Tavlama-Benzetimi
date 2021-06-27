import random

import numpy as np
import random as rd
#import pandas as pd
import timeit


start = timeit.default_timer()


#simetrik akış ve mesafe matrisi okutulur np.array komutu ile değişkende tutulur

akis = np.array([
   [0, 5, 2, 4, 1],
   [5, 0, 3, 0, 2],
   [2, 3, 0, 0, 0],
   [4, 0, 0, 0, 5],
   [1, 2, 0, 5, 0]
])

uzaklik = np.array([
   [0, 1, 1, 2, 3],
   [1, 0, 2, 1, 2],
   [1, 2, 0, 1, 2],
   [2, 1, 1, 0, 1],
   [3, 2, 2, 1, 0]
])

# akis maliyeti; akis*rect. distance matris çarpımıyla hesaplanır
# (1'den 2'ye akis varken 2'den 1'e ed akis var), bu sebeple flowları x2 eklemek gerekirdi ancak
#matris simetrik olduğundan hem üst üçgen hem alt üçgen dikkate alındı
#sadece üst üçgen dikkate alınsaydı return edecek değer şöyle olurdu:
# np.sum(obj_functionHesabi)[np.triu_indices(5,1)])*2
def obj_functionHesabi(akis):
    global uzaklik
    obj_functionHesabi = akis*uzaklik #matris çarpımı
    return np.sum(obj_functionHesabi)


#5 departmanın 2-opt swap operatörü ile komşuları oluşturulacak: toplam 5'in 2'li kombinasyonu kadar
#komşu yaratılıp aralarından rastgele ziyaret yapılacak
dept_sayisi = 5
N = 10 # size of neighboorhood matrix
neighbors = np.zeros((N, dept_sayisi), dtype=int) #ilk önce komşu listesi boş yaratılsın
#print(neighbors)


#mevcut çözümdeki departmanların sıralaması ikili şekilde değiştirilerek 10'a 5'lik komşu matrisi doldurulmaya başlanır.
def komsuluk(sol_n):
    global idx, neighbors
    idx=-1
    for i in range (dept_sayisi):
        j=i+1
        for j in range(dept_sayisi):
            if i<j:
                idx=idx+1
                sol_n[j], sol_n[i] = sol_n[i], sol_n[j] #swap two elements
                neighbors[idx] = sol_n
                #print("swap komşuluğuuu", neighbors)
               # neighbors[idx, -2:] = [sol_n[i], sol_n[j]]
                sol_n[i], sol_n[j] = sol_n[j], sol_n[i]
    return(neighbors) # randomly select one of the neighbors


random.seed(2)
def randomKomsuSec1 (neighbors):
    k = rd.randint(0, (N /2)-1)  # 1/N ihtimal hangi aralığa düşerse 0-1 random o komşuluğu alıyor
    return  (neighbors[k])
random.seed(1)
def randomKomsuSec2 (neighbors):
    k = rd.randint ((N/2), N - 1)  # 1/N ihtimal hangi aralığa düşerse 0-1 random o komşuluğu alıyor
    return  (neighbors[k])

random.seed(3)
#kabul kriteri fonksiyonu
def accProb(delta, T):
    return np.exp(-delta/T) >rd.random()

#Tavlama Benzetimi
def tavlamaBenzetimi(akis,uzaklik):
# INITILIZATION: başlangıç sıcaklığı, soğutma katsayısı, mü(k) iterasyon sayısı, durma kriteri için tutulan parametreler
 # başlangıç çözümü, başlangıç amaç fonksiyon değeri, incumbent initiliaze edilir.

#başlangıç çözümü için olurluluk şartı her departman permütasyon representation'a uyacak şekilde
# her departman tam olarak 1 kez dizide yer alacak şekilde gösterim yapılır:

    mevcutCozum = [3, 2, 0, 1, 4]
    mevcut_ObjValue = obj_functionHesabi(akis[np.ix_(mevcutCozum, mevcutCozum)])

#başta en iyi çözümümüz (incumbent) elimizdeki çözüme eşittir
    bestCozum = mevcutCozum
    bestCozum_maliyet = obj_functionHesabi(akis[np.ix_(bestCozum, bestCozum)])


    print("Initial Simulated Annealing Solution: " + str(bestCozum))
    print("Initial Simulated Annealing Cost: " + str(bestCozum_maliyet))


    T= 10000 #başlangıç sıcaklığı
    T_min = 0.001 #sıcaklık bunun altına düştüğünde durmalı
    toplamIterasyon=0  # toplam algoritma iterasyonu sayısı
    alpha = 0.9
    iterasyon=2 #mü(k) o sıcaklıkta kaç iterasyon arama yapacağım

#sıcaklık 0.001'in altına düştüğünde veya toplam iterasyon belirtilen değere ulaştığında dur
    while T > T_min or toplamIterasyon<=200:
    #while bestCozum_maliyet!=50:
        sayac=0 #mü(k) iterasyon'a ulaşılıp ulaşılmadığını kontrol etmek için
        komsuListesi= komsuluk(mevcutCozum)
#mü(k) iterasyon boyunca mevcut çözümün komşuları o T(k) sıcaklığı altında araştırılır
        for sayac in range(iterasyon):

#komşular rastgele şekilde iterasyonun tek veya çift numaralı iterasyon olmasına göre
#mevcut çözümün ilk yarısındaki elemanlar arasıda veya ikinci yarısında swap yapılacak şekilde seçilir
            if (sayac)%2==0:
                hangiKomsu= randomKomsuSec1(komsuListesi)
            else:
                hangiKomsu = randomKomsuSec2(komsuListesi)
            #print("hangi aday komşu seçildi:", hangiKomsu)

#aday komşunun maliyeti hesaplanır
            komsuMaliyet = obj_functionHesabi(akis[np.ix_(hangiKomsu, hangiKomsu)])
            #print("yeni komşunun maliyeti", komsuMaliyet)

#MEVCUT ÇÖZÜM GÜNCELLENSİN Mİ?
#eğer aday komşu mevcut çözümümüzden amaç fonksiyonu olarak daha iyiyse veya,
#aday komşu çözümü mevcut çözümden daha kötüyse ancak kabul kriterimizden geçtiyse mevcut çözüm bu aday komşu
#olarak güncellenir, yeni amaç fonksiyonu da mevcut çözüme göre hesaplanır
            if komsuMaliyet < mevcut_ObjValue | accProb(komsuMaliyet - mevcut_ObjValue, T):
                mevcutCozum = hangiKomsu
                #print("mevcut çözüm güncellendi ise:", mevcutCozum)
                mevcut_ObjValue = obj_functionHesabi(akis[np.ix_(mevcutCozum, mevcutCozum)])
#INCUMBENT GÜNCELLENSİN Mİ?
#mevcut çözüm ile best çözüm karşılaştırılır daha iyi ise best çözüm güncellenir.

            if mevcut_ObjValue < bestCozum_maliyet:
                bestCozum = mevcutCozum
                print("incumbent güncellendi mi?", bestCozum)
                bestCozum_maliyet = obj_functionHesabi(akis[np.ix_(bestCozum, bestCozum)])
                # np.ix_ operatörü çözümdeki sıralamaya uygun şekilde indisleri çaprazlar:
                #[0,1], [0,2] -> [0,0], [0,2], [1,0], [1,2] şeklinde akış matrisindeki akışları çözümün indislerine göre gönderir
        toplamIterasyon=toplamIterasyon+1
#soğutma çizelgesi ile sıcaklık güncellenir
        T = T*alpha


    print("Final Simulated Annealing Solution: " + str(bestCozum))
    print("Final Simulated Annealing Cost: " + str(bestCozum_maliyet))
    return bestCozum_maliyet

tavlamaBenzetimi(akis, uzaklik)

stop = timeit.default_timer()

print('ÇALIŞMA SÜRESİ: ', stop - start)