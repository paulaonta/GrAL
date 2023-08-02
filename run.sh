language=( 'en' 'es' 'es')
quest_sign_source_path=( 'QUEST_clinical_caseMIR_english.csv' 'QUEST_clinical_caseMIR.csv' 'QUEST_clinical_caseMIR_relations.csv')
check_path=( 'clinical_cases_translated_2_english.csv' 'clinical_cases_spanish.csv' 'clinical_cases_spanish.csv')
seed=(42 60 50 46 55)


for i in "${!language[@]}"
do
    for s in "${seed[@]}"
    do
        if [ "${quest_sign_source_path[$i]}" = "QUEST_clinical_caseMIR_relations.csv" ]
        then
            python3 code/argumentAns.py  --l 2 --relations ./results_Wikidata/ compareData/questions/"${quest_sign_source_path[$i]}" compareData/"${check_path[$i]}" "${language[$i]}" "$s"
        else
            python3 code/argumentAns.py --l 2 ./results_Wikidata/ compareData/questions/"${quest_sign_source_path[$i]}" compareData/"${check_path[$i]}" "${language[$i]}" "$s"
        fi
    done
done
