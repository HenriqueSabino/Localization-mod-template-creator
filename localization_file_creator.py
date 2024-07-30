import glob
import pandas as pd
import json

mod_template = open("./ModTemplate.template", "r", encoding="utf-8")

mod_class_name = input("Enter the desired class name: ")
mod_guid = input("Enter the desired mod GUID: ")
mod_title = input("Enter the desired mod title: ")
mod_description = input("Enter the desired mod description: ")

template_text = "".join(mod_template.readlines())

output_text = template_text.replace("{mod_class_name}", mod_class_name)
output_text = output_text.replace("{mod_guid}", mod_guid)
output_text = output_text.replace("{mod_title}", mod_title)
output_text = output_text.replace("{mod_description}", mod_description)

translation_files = glob.glob("*.csv")
translation_tables = [x.split('.')[0] for x in translation_files]

localization_methods_calls = ""
for file in translation_tables:
    file_no_spaces = file.replace(" ", "")
    localization_methods_calls += f"this.Set{file_no_spaces}Localizations();\n            "

output_text = output_text.replace("{localization_methods_calls}", localization_methods_calls.strip())

localization_methods = ""
for file in translation_files:
    translation = pd.read_csv(f"./{file}")

    file_no_extension = file.split(".")[0]
    file_no_spaces = file_no_extension.replace(" ", "")

    localization_methods += f"private void Set{file_no_spaces}Localizations()\n        "
    localization_methods += "{\n            "
    localization_methods += f"var table = LocalizationHelper.GetCollection(\"{file_no_extension}\", ModLanguage);\n            "
    localization_methods += "\n            "

    for entry in translation.itertuples():
        localization_methods += f"table.AddEntry(\"{entry.Key}\", {json.dumps(entry.Value)});\n            "

    localization_methods = localization_methods.strip() + "\n        }\n\n        "

output_text = output_text.replace("{localization_methods}", localization_methods.strip()).strip()

output_file = open(f"./{mod_class_name}.cs", "w", encoding="utf-8")
output_file.write(output_text)