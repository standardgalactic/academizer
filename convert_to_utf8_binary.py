input_file = "Tree of Self-reflection.mhtml"
output_file = "Tree of Self-reflection-utf8.mhtml"

with open(input_file, 'rb') as source_file:
        content = source_file.read()

        content = content.decode('ascii', errors='ignore').encode('utf-8')

        with open(output_file, 'wb') as target_file:
                target_file.write(content)

                print("Binary conversion to UTF-8 completed successfully.")


