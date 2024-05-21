from .gakuen_parser import parse_messages


def gakuen_txt_to_sc_csv(gakuen_txt: str, txt_name_without_ext: str) -> str:
    parsed = parse_messages(gakuen_txt)
    sc_csv = "id,name,text,trans\n"
    for line in parsed:
        if line["__tag__"] == "message":
            sc_csv += f"0000000000000,{line['name']},{line['text']},\n"
        if line["__tag__"] == "choicegroup":
            for choice in line["choices"]:
                sc_csv += f"select,,{choice['text']},\n"
    sc_csv += f"info,${txt_name_without_ext}.txt,,"
    sc_csv += f"译者,,,"
    return sc_csv
