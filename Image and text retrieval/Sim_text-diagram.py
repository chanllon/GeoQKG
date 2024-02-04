import pandas as pd
import random
from tqdm import tqdm
from Similar.Similar_cal import relationship_similarity, node_similarity, pure_node_similarity, sim_cal_one

text_csv_file = 'NEW_Text_Graph_data.csv'
diagram_csv_file = 'NEW_Diagram_Graph_data.csv'
output_csv_file = 'sim_text-diagram.csv'



result_data = pd.DataFrame(columns=['StandardDataID','IsTrue_30','IsTrue_20','IsTrue_10'])



df1 = pd.read_csv(text_csv_file, encoding='latin1')
df2 = pd.read_csv(diagram_csv_file, encoding='latin1')
text_data_ids = set(df1.iloc[:, 0])
diagram_data_ids = set(df2.iloc[:, 0])
print(len(set(text_data_ids)),len(set(diagram_data_ids)))
result_data = pd.DataFrame()

for standard_data_index in tqdm(text_data_ids, desc="Processing"):

    num = 0
    G_1 = sim_cal_one(text_csv_file, standard_data_index)
    sim_scores = []
    for comparison_data_index in diagram_data_ids:
        num += 1
        print('c:',comparison_data_index,'---num:',num)

        G_2 = sim_cal_one(diagram_csv_file, comparison_data_index)
        edge_sim = relationship_similarity(G_1, G_2)
        # node_sim = node_similarity(G_1, G_2)
        pure_node_sim = pure_node_similarity(G_1,G_2)
        similarity = 0.5 * edge_sim + 0.5 * pure_node_sim
        sim_scores.append((comparison_data_index, similarity))
    top_30_similarities = sorted(sim_scores, key=lambda x: x[1], reverse=True)[:30]
    target_in_top_30 = [index for index, _ in top_30_similarities]
    IsTrue_30 = any(index == standard_data_index for index in target_in_top_30)

    top_20_similarities = sorted(sim_scores, key=lambda x: x[1], reverse=True)[:20]
    target_in_top_20 = [index for index, _ in top_20_similarities]
    IsTrue_20 = any(index == standard_data_index for index in target_in_top_20)

    top_10_similarities = sorted(sim_scores, key=lambda x: x[1], reverse=True)[:10]
    target_in_top_10 = [index for index, _ in top_10_similarities]
    IsTrue_10 = any(index == standard_data_index for index in target_in_top_10)

    result_data = pd.concat(
        [result_data,
         pd.DataFrame({
             'StandardDataID': [standard_data_index],
             'IsTrue_30': [IsTrue_30],
             'IsTrue_20': [IsTrue_20],
             'IsTrue_10': [IsTrue_10]})],
        ignore_index=True)

        # result_data.to_csv(output_csv_file, mode='a', index=False)


result_data.to_csv(output_csv_file, index=False)
