#path_id=( "test_rm_ID.csv" "4_ans_only_ID_test_rm.csv" "4_5_ans_test_ID_rm.csv" )
seed=(42 60 50 46 55)


#for path in "${path_id[@]}"
#do
for s in "${seed[@]}"
do
  #python3 code/argumentAns.py --l 2 --id medmcqa/content/medmcqa_data/ID/$path ./results_Wikidata/ compareData/questions/QUEST_clinical_caseMIR_english.csv compareData/clinical_cases_translated_2_english.csv en "$s"
  python3 code/argumentAns.py --l 2  ./results_Wikidata/ compareData/questions/QUEST_clinical_caseMIR_english.csv compareData/clinical_cases_translated_2_english.csv en "$s"
  #python3 code/argumentAns.py --l 2  --relations ./results_Wikidata/ compareData/questions/QUEST_clinical_caseMIR_relations.csv compareData/clinical_cases_spanish.csv es "$s"
done
#done
