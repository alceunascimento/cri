import subprocess
import os


def convert_md_to_docx(input_file, output_file, reference_docx='./pre_cri/output/reference.docx'):
    try:
        # Using reference-doc parameter to apply the template
        subprocess.run([
            'pandoc',
            input_file,
            '-o', output_file,
            '--reference-doc', reference_docx,
            '--standalone'  # Ensures complete document structure
        ], check=True)
        print(f"File {output_file} created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_file} to {output_file}: {e}")

def convert_docx_to_pdf(input_file, output_file):
    try:
        subprocess.run(['pandoc', input_file, '-o', output_file], check=True)
        print(f"File {output_file} created successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Error converting {input_file} to {output_file}: {e}")


# Path to your markdown file
md_file = './pre_cri/output/memorial.md'
docx_file = './pre_cri/output/memorial.docx'

# Convert markdown to docx using the reference document
convert_md_to_docx(md_file, docx_file)