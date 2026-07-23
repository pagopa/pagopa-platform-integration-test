
import requests
from requests.auth import HTTPBasicAuth
import json
import os
import re
import sys
from pathlib import Path
from src.utility.confluence_utils import create_confluence_auth, upload_page_content, get_existing_page_content


PAGE_COMPONENTS_DIR = Path(__file__).resolve().parents[1] / 'page_components'

context_block = ''
scenario_header = ''
table_header = ''
table_cell = ''
step_content = ''
scenario_link = ''
code_block = ''
inline_code = ''

KEYWORD_CONTEXT = 'Contesto:'
KEYWORD_WHEN = 'Quando'
KEYWORD_THEN = 'Allora'
KEYWORD_GIVEN = 'Dato'
KEYWORD_EXAMPLES = 'Esempi'
KEYWORD_AND = 'E'
KEYWORD_SCENARIO = 'Scenario'
KEYWORD_LANGUAGE = '#language:'
KEYWORD_PIPE = '|'
LINK_PREFIX = '#link:'
TABLE_CLOSURE = '</tr></tbody></table>'
INLINE_CODE_PATTERN = re.compile(r'<\s*([A-Za-z0-9_]+)\s*>')
SUITE_SCENARIO_ID = re.compile(r'^@([A-Za-z0-9]+_(?:[A-Za-z0-9]+)*)_(\d{3})_(\d{2})$')
EMPTY_TABLE_CELL = '<td data-highlight-colour="#ffffff"></td>'



# function used to replace the inline code with the inline code block, containing the inline code inside the block
def replace_inline_code(value):
    return INLINE_CODE_PATTERN.sub(lambda m: inline_code.replace('{inline_code}', m.group(1).strip()), value)


def get_page_components():
    try:
        global scenario_header, table_header, table_cell, step_content, scenario_link, code_block, inline_code, context_block

        # get the header block for the scenario (title and link)
        with open(PAGE_COMPONENTS_DIR / 'context_block.txt', 'r', encoding='utf-8') as f:
            context_block = f.read()
        # get the header block for the scenario (title and link)
        with open(PAGE_COMPONENTS_DIR / 'scenario_header.txt', 'r', encoding='utf-8') as f:
            scenario_header = f.read()
        # get the table header block
        with open(PAGE_COMPONENTS_DIR / 'table_header.txt', 'r', encoding='utf-8') as f:
            table_header = f.read()
        # get the table cell block
        with open(PAGE_COMPONENTS_DIR / 'table_cell.txt', 'r', encoding='utf-8') as f:
            table_cell = f.read()
        # get the step content block
        with open(PAGE_COMPONENTS_DIR / 'step_content.txt', 'r', encoding='utf-8') as f:
            step_content = f.read()
        # get the scenario link block to put inside the scenario header
        with open(PAGE_COMPONENTS_DIR / 'scenario_link.txt', 'r', encoding='utf-8') as f:
            scenario_link = f.read()
        # get the code block for the outline scenarios
        with open(PAGE_COMPONENTS_DIR / 'code_macro.txt', 'r', encoding='utf-8') as f:
            code_block = f.read()
        # get the inline code block for the steps
        with open(PAGE_COMPONENTS_DIR / 'inline_code.txt', 'r', encoding='utf-8') as f:
            inline_code = f.read().strip()
    except Exception as e:
        raise RuntimeError(f"Failed to read page components from {PAGE_COMPONENTS_DIR}. Error: {str(e)}")

def check_language(line,fileIn):
    if line.startswith(KEYWORD_LANGUAGE):
        if not line.endswith('it'):
            raise RuntimeError(f"Unsupported language: {line}. Only Italian language is supported, in file {fileIn}")
    else:
        raise RuntimeError(f"Language not specified. The second line of the feature file must specify the language using the format: {KEYWORD_LANGUAGE} <language_code>, in file {fileIn}")


# Function used to add the step content to the table
def add_step_content(content_to_add,keyword,last_ins,line,data):
    last_ins = keyword if keyword is not None else last_ins
   
    if keyword != KEYWORD_GIVEN:
        if len(content_to_add) > 0:
            data += table_cell.replace('{step}', ''.join(content_to_add))
        else:
            data += EMPTY_TABLE_CELL
        content_to_add.clear()
    if keyword is not None:
        content_to_add.append(step_content.replace('{step}', line))
    return data, last_ins

# Function used to add the code macro content to the page
def add_code_content(content_to_add,keyword,last_ins,line,data):
    content_to_add.append(line + '\n')
    last_ins = keyword if keyword is not None else last_ins
    return data, last_ins

# Function used to build the page content from the feature file, by iterating over the lines of the file and, line by line,
# adding the content to the page, based on the keywords found in the line
def build_page_content(data,feature_file):
    print(f"[INFO][buildPageContent] Building page content from feature file: {feature_file}")
    try:
        with open(feature_file, 'r', encoding='utf-8') as f:
            last_ins = ''
            content_to_add= list()
            link_to_add = ''
            scenario_id = ''
            is_context = False
            for line in f.readlines() + ['\n']:
                line = line.strip()
                line = replace_inline_code(line)
                if SUITE_SCENARIO_ID.match(line):
                    scenario_id = line.split('_').pop()
                elif line.startswith(KEYWORD_SCENARIO):
                    data += scenario_header.replace("{scenario_title}", line.replace('Scenario',f'Scenario {scenario_id}')).replace("{link}", link_to_add)
                    data += table_header
                elif line.startswith(LINK_PREFIX):
                    link_vars = line[len(LINK_PREFIX):].split('|')
                    link_to_add = scenario_link.replace('{anchor}',link_vars[0]).replace('{space}',link_vars[1]).replace('{page}',link_vars[2])
                elif line.startswith(KEYWORD_CONTEXT):
                    is_context = True
                elif line.startswith(KEYWORD_GIVEN[0:len(KEYWORD_GIVEN)-1]):
                    data, last_ins = add_step_content(content_to_add,KEYWORD_GIVEN,last_ins,line,data)
                elif line.startswith(KEYWORD_WHEN):
                    data, last_ins = add_step_content(content_to_add,KEYWORD_WHEN,last_ins,line,data)
                elif line.startswith(KEYWORD_THEN):
                    data, last_ins = add_step_content(content_to_add,KEYWORD_THEN,last_ins,line,data)
                elif line.startswith(KEYWORD_EXAMPLES):
                    data, last_ins = add_code_content(content_to_add,KEYWORD_EXAMPLES,last_ins,line,data)
                elif line.startswith(KEYWORD_PIPE) and last_ins == KEYWORD_EXAMPLES:
                    data, last_ins = add_code_content(content_to_add,None,last_ins,line,data)
                elif line.startswith(KEYWORD_AND):
                    content_to_add.append(step_content.replace('{step}', line))
                else :
                    if last_ins == KEYWORD_THEN:
                        data, last_ins = add_step_content(content_to_add,None,'',line,data)
                        data += TABLE_CLOSURE
                    elif last_ins == KEYWORD_EXAMPLES:
                        data += code_block.replace('{code_block}', ''.join(content_to_add))
                        content_to_add.clear()
                        last_ins = ''
                    elif is_context:
                        data += context_block.replace('{context_point}', ''.join(content_to_add))
                        content_to_add.clear()
                        is_context = False
                        
        return data
    except Exception as e:
        raise RuntimeError(f"Failed to build page content from feature file: {feature_file}. Error: {str(e)}")


def main():
    if len(sys.argv) > 1:
        fileIn = sys.argv[1]
        with open(fileIn, 'r', encoding='utf-8') as f:
            confluencePageId = f.readline()[1:].strip('\n ')
            check_language(f.readline().strip('\n '), fileIn)
        auth = create_confluence_auth()
        existing_page = get_existing_page_content(fileIn, page_id=confluencePageId, auth_obj=auth)
        get_page_components()
        h2_index = existing_page['body']['storage']['value'].find('<h2>')
        if h2_index != -1: # if the <h2> tag is found, we use it to keep only the header section of the page, else we just append the new content
            existing_page['body']['storage']['value'] = existing_page['body']['storage']['value'][:h2_index]
        data = build_page_content(existing_page['body']['storage']['value'],fileIn)
        upload_page_content(existing_page, data, auth)
    else:
        raise FileNotFoundError("No file provided. Please provide a file as an argument.")


if __name__ == "__main__":
    main()
