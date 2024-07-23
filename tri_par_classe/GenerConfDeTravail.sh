# Récupère le fichier XML et supprime la racine, puis concatène plusieurs fichiers XML
# Argument 1 : nom du programme. Exemple : script.sh
# Argument 2 : nom du fichier de conf. Exemple : MDO-conf.xml
# Argument 3 : trigramme. Exemple : MDO
# Argument 4 : nom du fichier de conf tel. Exemple : MDO-tel.xml
# Argument 5 : nom du fichier de conf radio. Exemple : MDO-radio.xml
# Argument 6 : nom du fichier final xml voulu (après concaténation des 3 fichiers)
# Argument 7 : nom du fichier texte contenant les class-name des objets à inclure

if [ $# -ne 6 ]; then
    echo "Il faut mettre en premier argument nom_fichier, en deuxième le trigramme, en troisième la conf_tel, en quatrième la conf_radio, en cinquième nom du fichier_final et en sixième le fichier_texte contenant les class-name des objets à inclure"
    exit 1
fi

# Récupération des arguments et assignation à des variables. Ici, on choisit en dur le nom du nouveau fichier que python va créer. Ce nom peut être modifié
nom_fichier=$1
trigramme=$2
conf_tel=$3
conf_radio=$4
fichier_final=$5
fichier_texte=$6
nouveau_fichier="nouvelle_conf.xml"

# Suppression des lignes souhaitées dans les deux fichier de conf (tel et radio)
sed -i '/<configuration/d ; /<\/configuration/d ; /<?xml version/d ; /<\/groupe-object-model>/d ; /<groupe-object-model>/d' $conf_tel
sed -i '/<configuration/d ; /<\/configuration/d ; /<?xml version/d ; /<\/groupe-object-model>/d ; /<groupe-object-model>/d' $conf_radio

python v2-xml-Parser.py $nom_fichier $nouveau_fichier $trigramme $fichier_texte # Tri du fichier de conf

# Traitement nécessaire à la concaténation de tous les fichier. La suppression des redondances a été faite précedemment (sed...)
echo "Fin du script de python"

sed -i '/<\/configuration/d ' $nouveau_fichier
rm -rf $fichier_final
cat $nouveau_fichier >> $fichier_final
cat $conf_tel >> $fichier_final
cat $conf_radio >> $fichier_final
echo "</groupe-object-model></configuration></configurations>" >> $fichier_final

echo "Fin du script bash"
