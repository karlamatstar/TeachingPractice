import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

def get_docx_text(path):
    document = zipfile.ZipFile(path)
    xml_content = document.read('word/document.xml')
    document.close()
    tree = ET.XML(xml_content)
    
    WORD_NAMESPACE = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    PARA = WORD_NAMESPACE + 'p'
    TEXT = WORD_NAMESPACE + 't'
    
    paragraphs = []
    for paragraph in tree.iter(PARA):
        texts = [node.text
                 for node in paragraph.iter(TEXT)
                 if node.text]
        if texts:
            paragraphs.append(''.join(texts))
            
    return '\n'.join(paragraphs)

project_dir = Path(__file__).resolve().parents[2]
output_dir = project_dir / "_OUTPUT" / "final_report_source"
text = get_docx_text(output_dir / "StyleMall_QA_Report.docx")
with open(output_dir / "extracted_text.txt", 'w', encoding='utf-8') as f:
    f.write(text)
print("Extraction complete.")
