#1
echo -e "\n#1"
#number of lines
wc -l friends_aula.txt
#number of words
wc -w friends_aula.txt

#2
echo -e "\n#2"
grep Monica friends_aula.txt > 2.txt

#3
echo -e "\n#3"
grep Monica friends_aula.txt | wc -l

#4 use regex - use quotations because it is a regular expression \s means a space ^ means starts with
echo -e "\n#4"
#com aspas
grep "^Monica\s" friends_aula.txt > 4.txt
#sem aspas
grep ^Monica\\s friends_aula.txt > 4.txt

#5 -o significa que só a parte que corresponde à expressão regular é que é apanhada, no outro caso faz output da linha toda
echo -e "\n#5"
#sem aspas
grep -o "(.*)" friends_aula.txt > 5.txt
#com aspas
grep -o \(.*\) friends_aula.txt > 5.txt

#6 contar o número de vezes que aparece a palavra sarcastic para cada personagem
echo -e "\n#6"
#maneira 1
grep sarcastic friends_aula.txt | grep ^Monica | wc -l
grep sarcastic friends_aula.txt | grep ^Phoebe | wc -l
grep sarcastic friends_aula.txt | grep ^Ross | wc -l
grep sarcastic friends_aula.txt | grep ^Chandler | wc -l
grep sarcastic friends_aula.txt | grep ^Joey | wc -l
grep sarcastic friends_aula.txt | grep ^Rachel | wc -l

#maneira mais complexa cut -f 1 podia ser a alternativa a "^[A-Za-z]+\s" para apanhar a primeira coluna
#sort -f para ignorar se começa ou não com coluna
#grep precisa do -E maiúsculo para interpretar expressões mais complexas
grep sarcastic friends_aula.txt | grep -o -E "^[A-Za-z]+\s" | sort -f | uniq -ci | sort -n | tail -n1

grep [Ss]inging friends_aula.txt | grep -o -E "^[A-Za-z]+\s" | sort -f | uniq -ci | sort -n | tail -n1

#7
echo -e "\n#7"
#não é garantido que tenhamos só personagens porque estamos a tirar a primeira coluna, mas n faz mal
cut -f1 friends_aula.txt | sort -f | uniq -ci | sort > 7.txt

#8
echo -e "\n#8"
#acrescentar o sort -n para ordenar pelo número de linhas e usar o tail para retirar o que tem mais
cut -f1 friends_aula.txt | sort -f | uniq -ci | sort -n | tail -n1

#9 tr para dar translate dos
echo -e "\n#9"
#manter as palavras com a flag -c e remover o "\n" com a flag -s do translate
tr -sc "AZa-z" "\n" < friends_aula.txt | sort -f | uniq -ci | sort -n > 9.txt

#10
echo -e "\n#10"
#selecionar o que está na 2a coluna para selecionar os diálogos
#é feito sort duas vezes só para ter a certeza que o uniq funciona bem
cut -f2 friends_aula.txt | tr -sc "A-Za-z" "\n" | sort -f | uniq -c | sort -n | tail -n20

#11
echo -e "\n#11"
#neste exercício fazemos o grep de cada personagem relativamente ao exercício anterior
#fazer o grep com aquilo que elas dizem no cut -f2
grep "^Monica" friends_aula.txt | cut -f2 | tr -sc "A-Za-z" "\n" | sort -f | uniq -c | sort -n | tail -n10
echo -e "\n"
grep "^Phoebe" friends_aula.txt | cut -f2 | tr -sc "A-Za-z" "\n" | sort -f | uniq -c | sort -n | tail -n10
echo -e "\n"
grep "^Joey" friends_aula.txt | cut -f2 | tr -sc "A-Za-z" "\n" | sort -f | uniq -c | sort -n | tail -n10
echo -e "\n"
grep "^Chandler" friends_aula.txt | cut -f2 | tr -sc "A-Za-z" "\n" | sort -f | uniq -c | sort -n | tail -n10
echo -e "\n"
grep "^Ross" friends_aula.txt | cut -f2 | tr -sc "A-Za-z" "\n" | sort -f | uniq -c | sort -n | tail -n10
echo -e "\n"
grep "^Rachel" friends_aula.txt | cut -f2 | tr -sc "A-Za-z" "\n" | sort -f | uniq -c | sort -n | tail -n10