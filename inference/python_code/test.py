import json
import pandas as pd
path = '/home/ljj/Downloads/hanshin_inference/cfg.json'
with open(path, "rt", encoding="utf-8") as f:
    cfg = json.load(f)

all_data = {
    "liver_ast": 12,
    "liver_alt": 12,
    "r_gtp": 23,
    "liver_alp": 45,
    "tri_gly": 35,
    "bmi" : 12
}
person_private = pd.DataFrame(columns=cfg["output"]["private"])
for key, value in cfg["output"]["cols"].items():
    disease = pd.DataFrame(columns=value)
    output_df = pd.concat([person_private, disease], axis=1)
    # output_df["predict"] = pd.DataFrame(data=rf.predict(X), index=output_df.index) # Result 
    for col in output_df.columns.tolist():
        output_df[col] = pd.DataFrame(all_data[col])
    output_df["predict"] = pd.DataFrame(data=89, index=output_df.index) # Result 
    # output_df["89"] = pd.DataFrame(data="89", index=output_df.index) # Result 
    print(output_df)
import pandas as pd
path = '/home/ljj/workspace/hanshin_inference/inference_data/zxcv.xlsx'
xlsx = pd.read_excel(path)
xlsx.to_csv('/home/ljj/workspace/hanshin_inference/inference_data/service_data_1person.csv')