import codecs

input_file = "Tree of Self-reflection.mhtml"
output_file = "Tree of Self-reflection-utf8.mhtml"

with codecs.open(input_file, 'r', encoding='ascii', errors='ignore') as source_file:
        content = source_file.read()

        with codecs.open(output_file, 'w', encoding='utf-8') as target_file:
                target_file.write(content)

                print("Conversion to UTF-8 completed successfully.")

