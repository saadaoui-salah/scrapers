keywords="Jean,Marie,Paul,Emma,Louise,Lucas,Hugo,Jade,Gabriel,Alice,Nathan,Chloé,Arthur,Léa,Manon,Raphaël,Camille,Juliette,Jules,Mila,Tom,Théo,Zoé,Sarah,Ethan,Mia,Noah,Sofia,Maxime,Clara,Léo,Léna,Eva,Adam,Enzo,Laura,Elena,Nora,Louis,Charles,Hélène,François,Sophie,Catherine,Anne,Claire,Michel,Henri,André,Jacqueline,Christine,Jeanne,Lucas,Matteo,Ryan,Dylan,Aaron"

for keyword in $(echo $keywords | tr ',' '\n'); do
    grep -oP "https:\/\/www\.pagesjaunes\.fr\/pagesblanches\/recherche\?quoiqui=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$keyword'))")[^\s]+" page.log | tail -1
done
