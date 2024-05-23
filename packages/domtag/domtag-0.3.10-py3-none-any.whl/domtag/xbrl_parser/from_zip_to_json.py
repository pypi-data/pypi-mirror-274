"""HTML table extractor"""
import copy
import json
import logging
import os
import re
import unicodedata
import uuid
from operator import attrgetter
from pathlib import Path
from typing import Union, List, Optional
from zipfile import ZipFile

import bs4
import numpy as np
from bs4 import BeautifulSoup, element, Tag, Comment

from domtag.utils.enums import TagAttrs


def add_pt_suffix_to_integers(func):
    def wrap(*args, **kwargs):
        padding = func(*args, **kwargs)
        try:
            padding = int(padding.strip())
            return f'{padding}pt'
        except:
            return padding

    return wrap


class HtmlExtractor:
    """HTML tables information extraction module"""

    NUMERIC_REGEX_PATTERN = re.compile(r"[0-9,)(.]+")
    CELL_ONLY_NUMERIC_REGEX_PATTERN = re.compile(
        r'^([+\-])?([{(])?(\d)+(\.|,\d+)?([})])?([^A-Za-z]*)')

    def __init__(self, path: Union[str, Path]):
        self._path = Path(path)
        self._zip_path = None
        self._htm_path = None
        self._json_path = None
        self.file_type = 'archive'
        self.resolve_paths()
        self.html = self.read_html()
        self.metalinks = self.get_metalinks()
        self.soup_raw = BeautifulSoup(self.html, features='lxml')
        self.soup = self.set_id_to_tags_when_missing(soup=self.soup_raw)
        soup_copy = copy.copy(self.soup)
        self.soup = self.annotate_page_breaks(soup=self.soup)
        self.save_html()
        self.soup = soup_copy
        self.soup = self.remove_empty_tables(soup=self.soup)
        self.soup = self.add_xpath_attr_to_soup(soup=self.soup)

    @staticmethod
    def remove_empty_tables(soup: BeautifulSoup) -> BeautifulSoup:
        """Remove empty tables from a soup object inplace
        """
        for table in soup.find_all('table'):
            if all([not i.text.strip()
                    for i in table.find_all('td')]):
                table.decompose()
        return soup

    def save_html(self) -> None:
        """Saves html file in the predefined html path"""
        with open(self._htm_path, 'w') as f:
            f.write(str(self.soup))

    def resolve_paths(self) -> None:
        """Resolve the zipfile, html and json paths"""
        for path in self._path.iterdir():
            if path.is_file() and str(path).lower().endswith('.zip'):
                self._zip_path = path
                break
        self._htm_path = self._path / "source.html"
        self._json_path = self._path / "tables.json"

    def read_html(self) -> Optional[Union[str, bytes]]:
        """Read html file. If the file_type attribute is 'archive', will
        identify and read it from the zip file
        """
        html = None
        if self.file_type == 'html':
            html = self._read_from_html()
        elif self.file_type == 'archive':
            html = self._read_from_zip()
        return html

    def extract_tables(self) -> List[dict]:
        """
        Extract tables information from html file or zipped folder
        :return: A list of dictionaries containing tables information
        """

        tables_dict = self.extract_tables_from_html(soup=self.soup)
        self.__save_table_info(tables_dict, self._json_path)
        return tables_dict

    def _read_from_html(self) -> str:
        with open(self._path, 'r') as file:
            return file.read()

    def _read_from_zip(self) -> dict:
        with ZipFile(self._zip_path) as zip_file:
            htmls_in_zip = filter(lambda x: (
                    x.filename.endswith('.html') or x.filename.endswith('.htm')
                ), zip_file.filelist)
            largest_html = max(htmls_in_zip, key=attrgetter('file_size'))
            return zip_file.read(largest_html)

    def get_metalinks(self) -> bytes:
        """Get metalinks from the html file"""
        with ZipFile(self._zip_path) as zip_file:
            if 'MetaLinks.json' in zip_file.namelist():
                meta_links_file = zip_file.extract('MetaLinks.json')
                with open(meta_links_file, 'r') as file:
                            meta_links_data = json.load(file)
                            return meta_links_data
            else:
                return None



    @classmethod
    def add_xpath_attr_to_soup(cls, soup: BeautifulSoup) -> BeautifulSoup:
        """Create a copy of the soup object and add xpath attributes to all
        table, tr and td tags"""
        soup = copy.copy(soup)
        tables = soup.find_all('table')
        for table in tables:
            table.attrs['xpath'] = cls.__xpath_soup(table)
            for tr in table.find_all('tr'):
                tr.attrs['xpath'] = cls.__xpath_soup(tr)
                for td in tr.find_all('td'):
                    td.attrs['xpath'] = cls.__xpath_soup(td)
        return soup

    def match_with_name_and_contextref(self, table_element, financial_tables):
        match = False
        unique_anchor = financial_tables.get('uniqueAnchor', {})
        if not unique_anchor:
            unique_anchor = financial_tables.get('firstAnchor', {})
        if unique_anchor is not None:
            context_ref = unique_anchor.get('contextRef', None)
            name = unique_anchor.get('name', None)
            if table_element and table_element.get('contextref') == context_ref \
                    and table_element.get('name') == name:
                match = True
        else:
            match = False

        return match

    def filter_tables(self, tables, financial_tables):
        if not financial_tables:
            logging.log(logging.WARNING, "Metalinks.json not found")
            return tables
        filtered_tables = []
        for table in tables:
            match_found = False
            for parent in table.parents:
                if parent.has_attr('contextref') and parent.has_attr('name'):
                    for R, fin_table in financial_tables.items():
                        match = self.match_with_name_and_contextref(parent,
                                                                    fin_table)
                        if match:
                            filtered_tables.append(table)
                            match_found = True
                            break
                else:
                    pass
            if match_found:
                continue
            children = table.descendants
            for child in children:
                if isinstance(child, Tag) and child.has_attr('contextref') \
                        and child.has_attr('name'):
                    for R, fin_table in financial_tables.items():
                        match = self.match_with_name_and_contextref(child,
                                                                    fin_table)
                        if match:
                            filtered_tables.append(table)
                            break
                else:
                    pass

        return filtered_tables

    def filter_dictionaries(self, reports, list_of_groups, subgroup):
        """Filters dictionaries by list of groups and subgroup"""
        filtered_dicts = {report_num: report for report_num, report
                          in reports.items()
                          if report.get('groupType') in list_of_groups
                          and report.get('subGroupType') in subgroup}

        return filtered_dicts

    def get_financial_tables(self):
        dicts = {}
        reports = {}

        list_of_groups = ['statement', 'Statements', 'disclosure', 'Notes',
                          'notes',
                          'Tables', 'Details']
        subgroup = ['tables', 'details', '']

        metalinks = self.metalinks.get('instance', None)
        if metalinks:
            doc_key = list(metalinks.keys())[0]
            reports = metalinks.get(doc_key, {}).get('report', None)

        if reports:
            dicts = self.filter_dictionaries(reports, list_of_groups, subgroup)

        return dicts


    def extract_tables_from_html(self, soup: BeautifulSoup) -> List[dict]:
        """
        Extract tables information from html instance string
        :param soup: BeautifulSoup object
        :return: A list of dictionaries containing tables information
        """
        soup = self.set_left_padding(soup=soup)
        soup = self.add_styles_to_tables(soup=soup)
        soup = self.merge_table_cells_heuristic(soup=soup)
        soup = self.add_border_attributes_to_tables(soup=soup)
        self.soup = soup

        financial_tables = {}
        if self.metalinks:
            financial_tables = self.get_financial_tables()
        tables = soup.find_all('table')
        tables = self.filter_tables(tables, financial_tables)

        tables = [self.remove_empty_merges(table=table) for table in tables]
        tables = [
            self.flip_table(
                self.remove_empty_merges(
                    self.flip_table(table=table)
                )
            ) for table in tables]
        tables_data = []

        left_indent = TagAttrs.left_indentation.value
        is_italic = TagAttrs.is_italic.value
        is_bold = TagAttrs.is_bold.value
        has_top_border = TagAttrs.has_top_border.value
        has_bottom_border = TagAttrs.has_bottom_border.value

        for table in tables:
            has_number = self._check_table_has_number(table)
            if not has_number:
                continue
            trs = []
            n_cols = 0
            for row_idx, tr in enumerate(table.find_all('tr')):
                col_idx = 0
                tds = [{"rowIndex": row_idx,
                        "colIndex": col_idx,
                        "colspan": 1,
                        "rowspan": 1}]
                col_idx += 1
                for td in tr.find_all('td'):
                    value = self._extract_value(td)

                    td_data = {'id': td.attrs['id'].split(';'),
                               'xpath': td.attrs['xpath'],
                               "rowIndex": row_idx,
                               "colIndex": col_idx,
                               "value": value}
                    if left_indent.lower() in td.attrs:
                        td_data[left_indent] = td.attrs[left_indent.lower()]
                    if is_italic.lower() in td.attrs:
                        td_data[is_italic] = (
                            True
                            if td.attrs[is_italic.lower()].lower() == 'true'
                            else False
                        )
                    if is_bold.lower() in td.attrs:
                        td_data[is_bold] = (
                            True
                            if td.attrs[is_bold.lower()].lower() == 'true'
                            else False
                        )
                    if has_top_border.lower() in td.attrs:
                        td_data[has_top_border] = (
                            True
                            if td.attrs[has_top_border.lower()] is True
                               or td.attrs[has_top_border.lower()]
                               .lower()=='true' else False)
                    if has_bottom_border.lower() in td.attrs:
                        td_data[has_bottom_border] = (
                            True
                            if td.attrs[has_bottom_border.lower()] is True
                               or td.attrs[has_bottom_border.lower()]
                               .lower() == 'true' else False)
                    search_res = td.find_all('ix:nonFraction')
                    if search_res:
                        if 'id' in search_res[0].attrs:
                            td_data['id'] = search_res[0].attrs['id']
                        if 'contextref' in search_res[0].attrs:
                            td_data['contextRef'] = search_res[0]['contextref']
                        if 'name' in search_res[0].attrs:
                            td_data['name'] = search_res[0]['name']

                    if 'colspan' in td.attrs:
                        col_idx += int(td.attrs['colspan'])
                        td_data['colspan'] = int(td.attrs['colspan'])
                    else:
                        col_idx += 1
                        td_data['colspan'] = 1

                    if 'rowspan' in td.attrs:
                        td_data['rowspan'] = int(td.attrs['rowspan'])
                    else:
                        td_data['rowspan'] = 1

                    tds.append(td_data)
                n_cols = sum(td['colspan'] for td in tds)
                trs.append({
                    'id': tr.attrs['id'],
                    'xpath': tr.attrs['xpath'],
                    'td': tds,
                })
            title = self._extract_title(table)
            tables_data.append({
                'id': table.attrs['id'],
                'xpath': table.attrs['xpath'],
                'title': title,
                'thead': {
                    'tr': [{
                        "td": [],
                        "th": [{} for _ in range(n_cols)]
                    }]},
                'tbody': {
                    'tr': trs,
                }})
        return tables_data

    def _extract_value(self, td: bs4.Tag) -> str:
        value = td.attrs.get('merged_text', td.get_text())
        value = re.sub('[ \n]+', ' ', value).strip()
        value = self.__normalize_unicode(value)
        return value

    def _extract_title(self, tag) -> str:
        for i in range(50):
            tag = tag.previous
            if not tag:
                break
            title = self._clean_text(tag.text)
            if title and self._has_bold_text(tag):
                if self._is_inside(tag, 'table'):
                    break
                return title
        return ''

    def _clean_text(self, text: str) -> str:
        text = re.sub('[ \n]+', ' ', text).strip()
        return self.__normalize_unicode(text)

    @classmethod
    def _has_bold_text(cls, tag) -> bool:
        if cls._has_bold_in_style_attribute(tag):
            return True

        parents = tag.find_parents()

        for parent in parents:
            if cls._has_bold_in_style_attribute(parent) or parent.name == 'b':
                return True

        return False

    @classmethod
    def _has_bold_in_style_attribute(cls, tag) -> bool:
        if not tag.get('style', None):
            return False

        if 'font-weight' not in tag['style']:
            return False

        font_weight_value = tag['style'].split('font-weight:')[1].split(
            ';')[0].strip()

        is_numeric_and_bold = font_weight_value.isnumeric() and int(
            font_weight_value) > 449
        is_text_and_bold = (font_weight_value == 'bold'
                            or font_weight_value == 'bolder')
        return is_numeric_and_bold or is_text_and_bold

    @classmethod
    def _has_italic_in_style_attribute(cls, tag) -> bool:
        if not tag.get('style', None):
            return False

        if 'font-style' not in tag['style']:
            return False

        font_style_value = tag['style'].split('font-style:')[1].split(
            ';')[0].strip()
        return font_style_value == 'italic'

    @classmethod
    def _has_italic_text(cls, tag) -> bool:
        if cls._has_italic_in_style_attribute(tag):
            return True

        parents = tag.find_parents()

        for parent in parents:
            if (cls._has_italic_in_style_attribute(parent)
                or parent.name == 'i' or parent.name == 'em'):
                return True

        return False

    @staticmethod
    def _is_inside(child_tag, parent_name: str) -> bool:
        for parent_tag in child_tag.parents:
            if parent_tag.name == parent_name:
                return True

    @staticmethod
    def __xpath_soup(html_element: Union[element.Tag, element.NavigableString]
                     ) -> str:
        """
        Generate xpath from BeautifulSoup4 element.
        :param html_element: BeautifulSoup4 element.
        :return: xpath as string
        """
        components = []
        child = html_element if html_element.name else html_element.parent
        for parent in child.parents:  # type: BeautifulSoup.element.Tag
            siblings = parent.find_all(child.name, recursive=False)
            components.append(
                child.name if len(siblings) == 1 else '%s[%d]' % (
                    child.name,
                    next(i for i, s in enumerate(siblings, start=1) if s is child)
                    )
                )
            child = parent
        components.reverse()
        return '/%s' % '/'.join(components)

    @staticmethod
    def __normalize_unicode(text: str):
        text = unicodedata.normalize('NFKD', text)
        text = text.encode('ascii', 'ignore').decode('utf-8')
        return text

    @staticmethod
    def __save_table_info(tables_info: list, save_dir: str) -> None:
        with open(save_dir, "w") as file:
            json.dump(tables_info, file, indent=2)

    @staticmethod
    def create_table_html_empty_cell_grid(table: BeautifulSoup
                                          ) -> tuple[Optional[np.ndarray],
                                                     BeautifulSoup]:
        """Create a copy of the table tag and create a matrix with where each
        value represents a deconstructed cell (without merges) and the value
        represents is 1 if the cell is empty, 0 otherwise
        """
        table = copy.copy(table)
        table_structure = []
        empty_trs = []
        trs = list(table.find_all('tr'))
        for tr_idx, tr in enumerate(trs):
            tds = list(tr.find_all('td'))
            if all([not td.text for td in tds]):
                empty_trs.append(tr_idx)
                tr.decompose()
                continue
            row_structure = []
            for td_idx, td in enumerate(tds):
                colspan = int(td.attrs.get('colspan', 1))
                if td.text.strip():
                    row_structure.append(1)
                else:
                    row_structure.append(0)
                for _ in range(1, colspan):
                    row_structure.append(0)
            table_structure.append(row_structure)
        if not table_structure:
            return None, table
        row_len = len(table_structure[0])
        for row in table_structure[1:]:
            if len(row) != row_len:
                max_len = max(len(x) for x in table_structure)  # find the maximum length among all sublists
                table_structure = [x + [0] * (max_len - len(x)) for x in table_structure]
                break
        table_structure = np.array(table_structure)
        return table_structure, table

    @classmethod
    def _is_display_none(cls, tag: bs4.Tag) -> bool:
        if not tag.get('style', None):
            return False

        if 'display' not in tag['style']:
            return False

        display_value = tag['style'].split('display:')[1].split(';')[0].strip()

        return display_value == 'none'

    @classmethod
    def remove_hidden_cells(cls, table: BeautifulSoup
                            ) -> (BeautifulSoup, bool):
        """Remove cells that should not be displayed"""
        row_width = None
        for tr in table.find_all('tr'):
            current_width = 0
            for td in tr.find_all('td'):
                if cls._is_display_none(td):
                    continue

                current_width += int(td.get('colspan', 1))

            if current_width == 0:
                continue

            if row_width is None:
                row_width = current_width

            if current_width != row_width:
                return table, False

        for td in table.find_all('td'):
            if cls._is_display_none(td):
                td.decompose()

        return table, True

    @classmethod
    def remove_empty_merges(cls, table: BeautifulSoup) -> BeautifulSoup:
        """Remove unnecessary merges with no content from the table from left
        to right"""
        table_structure, table = cls.create_table_html_empty_cell_grid(table)
        if table_structure is None:
            return table
        table_structure = np.array(table_structure)
        empty_col_indices = []
        for col_idx, col in enumerate(table_structure.T):
            if not np.any(col):
                empty_col_indices.append(col_idx)
        empty_col_indices = set(empty_col_indices)
        trs = table.find_all('tr')
        for tr_idx, tr in enumerate(trs):
            tds = list(tr.find_all('td'))
            cursor_idx = 0
            for td_idx, td in enumerate(tds):
                indices = {cursor_idx}
                col_span_int = int(td.attrs.get('colspan', 1))
                for _ in range(1, col_span_int):
                    cursor_idx += 1
                    indices.add(cursor_idx)
                matching_cols = empty_col_indices & indices
                if matching_cols:
                    for _ in matching_cols:
                        col_span_int = int(td.attrs.get('colspan', 1))
                        if col_span_int > 1:
                            # logging.debug(f"Removing a single span in {tr_idx
                            # }, {td_idx}")
                            td.attrs['colspan'] = str(col_span_int - 1)
                        elif td.text.strip():
                            logging.warning(f"Text exists: {tr_idx}, {td_idx}:"
                                            f" {td.text}")
                        else:
                            td.decompose()
                cursor_idx += 1
        return table

    @classmethod
    def _generate_random_id(cls) -> str:
        return str(uuid.uuid4())

    @classmethod
    def set_id_to_tags_when_missing(cls, soup: BeautifulSoup) -> BeautifulSoup:
        """Add a copy of the soup elements with added id attribute
        to every tag"""
        soup = copy.copy(soup)
        tags = soup.find_all(id=False)
        for tag in tags:
            tag['id'] = cls._generate_random_id()
        return soup

    @staticmethod
    def _is_child_row(anchor_colspan: int, row: bs4.Tag) -> bool:
        cells = row.find_all('td')
        cells_colspan = 0
        if not cells[0].get_text().strip() == '':
            return False
        for cell in cells:
            cells_colspan += int(cell.attrs.get('colspan', 1))
            if not cell.get_text().strip() == '':
                break
        return cells_colspan == anchor_colspan

    def _is_anchor(self, row_idx: int, rows: list[bs4.Tag]):
        cell = rows[row_idx].find('td')
        if cell is None:
            return False
        colspan = int(cell.attrs.get('colspan', 1))
        if cell.get_text().strip() == '':
            return False
        return self._is_child_row(colspan, rows[row_idx + 1])

    @staticmethod
    def _merge_cells(row: bs4.Tag, anchor_colspan: int) -> None:
        cells = row.find_all('td')[:anchor_colspan + 1]
        i = 0
        if len(cells) == 1:
            return
        while i < len(cells) and cells[i].get_text().strip() == '':
            cells[i].decompose()
            i += 1
        if i in cells:
            cells[i].attrs['leftIndentation'] = i
            cells[i].attrs['colspan'] = anchor_colspan

    def _remove_indents(self, table: bs4.Tag):
        rows = table.find_all('tr')
        anchor_idx = 0
        while anchor_idx < len(rows) - 1:
            if not self._is_anchor(anchor_idx, rows):
                anchor_idx += 1
                continue
            anchor_td = rows[anchor_idx].find('td')
            anchor_colspan = int(anchor_td.attrs.get('colspan', 1))
            anchor_td.attrs['leftIndentation'] = 0
            child_idx = anchor_idx + 1
            while child_idx < len(rows):
                if self._is_child_row(anchor_colspan, rows[child_idx]):
                    self._merge_cells(rows[child_idx], anchor_colspan)
                child_idx += 1
            anchor_idx = child_idx

    def _check_table_has_number(self, table):
        has_number = False
        rows = table.find_all("tr")
        for row in rows:
            all_cells = row.find_all("td")
            for cell in all_cells:
                text = cell.get_text().strip()
                if text and re.fullmatch(
                        self.CELL_ONLY_NUMERIC_REGEX_PATTERN, text):
                    has_number = True
        return has_number

    @staticmethod
    @add_pt_suffix_to_integers
    def _get_padding_in_cell(cell: bs4.Tag) -> str:
        padding_left = '0pt'
        if 'style' in cell.attrs:
            child_div = cell.find('div')
            child_text = cell.find('p')
            # Check the case if table cell has div element inside
            # which has padding-left styling for indentation
            if child_div and 'style' in child_div.attrs:
                div_attributes = child_div.attrs['style'].split(';')
                padding = [i for i in div_attributes if
                           i.startswith('padding-left:')]
                if len(padding) > 0:
                    padding_left = padding[0].split(':')[1]
                    return padding_left
            # Check the case if table cell has p element inside
            # which has margin-left styling for indentation
            elif child_text and 'style' in child_text.attrs:
                div_attributes = child_text.attrs['style'].split(';')
                padding = [i for i in div_attributes if
                           i.startswith('margin-left:')]
                if len(padding) > 0:
                    padding_left = padding[0].split(':')[1]
                    return padding_left
            # Check the case if table cell has no div or p element inside
            # but has padding/padding-left/text-indent styling for indentation
            cell_attributes = cell.attrs['style'].split(';')
            padding = [i for i in cell_attributes if
                       i.startswith('padding:')]
            padding_with_left = [i for i in cell_attributes if
                                 i.startswith('padding-left:')]
            text_indent = [i for i in cell_attributes if
                           i.startswith('text-indent:')]
            if len(padding) > 0:
                padding = padding[0].split(' ')
                if len(padding) == 4:
                    padding_left = padding[3]
            elif len(padding_with_left) > 0:
                padding_left = padding_with_left[0].split(':')[1]
            elif len(text_indent) > 0:
                padding_left = text_indent[0].split(':')[1]

        return padding_left

    def set_left_padding(self, soup: BeautifulSoup) -> BeautifulSoup:
        """Remove leading tds, if they are used for text indentation"""
        all_tables = soup.find_all('table')
        for table in all_tables:
            has_number = self._check_table_has_number(table)
            if not has_number:
                continue
            rows = table.find_all("tr")
            table_first_col_paddings = []
            for row in rows:
                cell = row.find("td")
                if cell:
                    padding_left = self._get_padding_in_cell(cell)
                    table_first_col_paddings.append(padding_left)
            unique_paddings = sorted(set(table_first_col_paddings),
                                     key=lambda x: float(x[:-2]))
            padding_indexes = {padding: idx for
                               idx, padding
                               in enumerate(unique_paddings)}

            if len(unique_paddings) == 1 and unique_paddings[0] != '0pt':
                self._remove_indents(table)

            if padding_indexes:
                for row in rows:
                    cell = row.find("td")
                    if cell:
                        padding_left = self._get_padding_in_cell(cell)
                        cell.attrs['leftIndentation'] = padding_indexes[
                            padding_left]
        return soup

    @staticmethod
    def merge_row_tds(td_left: bs4.Tag, td_right: bs4.Tag) -> bs4.Tag:
        """Add the text in right td to left td and mark it with 'merged_text'
        attribute. In the next step the right td will be removed.
        Left td is changed inplace."""
        left_text = td_left.attrs.get('merged_text', td_left.get_text())
        td_left.attrs['merged_text'] = left_text + td_right.get_text()
        for child in td_right.descendants:
            if not isinstance(child, Tag):
                continue
            if child.get('contextref') and child.get('name'):
                td_left['contextref'] = child.get('contextref')
                td_left['name'] = child.get('name')
        td_left.attrs['colspan'] = str(
            int(td_left.attrs.get('colspan', 1))
            + int(td_right.attrs.get('colspan', 1)))
        sep = ';'
        xpath = sep.join([td_left.attrs.get('xpath', ''),
                          td_right.attrs.get('xpath', '')])
        td_id = sep.join([td_left.attrs.get('id', ''),
                          td_right.attrs.get('id', '')])
        if xpath != sep:
            td_left.attrs['xpath'] = xpath
        if td_id != sep:
            td_left.attrs['id'] = td_id
        return td_left

    @classmethod
    def is_row_merge_case(cls, first: str, second: str) -> bool:
        """Identify whether the first and second cell contents should be merged
        into one. This uses heuristcics identified from xbrl samples"""
        merge = False
        first_is_num = re.fullmatch(cls.NUMERIC_REGEX_PATTERN, first)
        second_is_num = re.fullmatch(cls.NUMERIC_REGEX_PATTERN, second)
        if first == "$" and second_is_num:
            merge = True
        # if first == '' and second in ['-', '—']:
        #     merge = True
        elif first == '$' and second in ['-', '—']:
            merge = True
        elif first_is_num and second.endswith('%'):
            merge = True
        elif first_is_num and second in ['%)', ')'] and first.startswith("("):
            merge = True
        elif (first.startswith('(') and not first.endswith(')') and second_is_num
              and not second.startswith('(')):
            merge = True
        return merge

    def merge_table_cells_heuristic(self,
                                    soup: BeautifulSoup) -> BeautifulSoup:
        """Identify and merge cells using heuristcics identified from xbrl
        samples"""
        soup = copy.copy(soup)
        previous_td = None
        for table in soup.find_all('table'):
            for tr_idx, tr in enumerate(table.find_all('tr')):
                for td_idx, td in enumerate(tr.find_all('td')):
                    if td_idx == 0:
                        previous_td = td
                        continue
                    first = previous_td.text.strip()
                    second = td.text.strip()
                    if self.is_row_merge_case(first=first, second=second):
                        previous_td = self.merge_row_tds(td_left=previous_td,
                                                         td_right=td)
                        td.decompose()
                    else:
                        previous_td = td
        return soup

    def add_styles_to_tables(self, soup: BeautifulSoup) -> BeautifulSoup:
        """Create a copy of the soup object"""
        soup = copy.copy(soup)
        for table in soup.find_all('table'):
            for td in table.find_all('td'):
                if any([self._has_italic_text(i) for i in td.descendants
                        if isinstance(i, bs4.Tag)]):
                    td.attrs['isItalic'] = True
                if any([self._has_bold_text(i) for i in td.descendants
                        if isinstance(i, bs4.Tag)]):
                    td.attrs['isBold'] = True
        return soup

    def _has_top_border(self, tag: bs4.Tag) -> bool:
        if not tag.get('style', None):
            return False

        if 'border-top:' in tag['style']:
            border_value = tag['style'].split(
                'border-top:')[1].split(';')[0].strip()
        elif 'border:' in tag['style']:
            border_value = tag['style'].split(
                'border:')[1].split(';')[0].strip()
        elif 'border-width' in tag['style']:
            border_value = tag['style'].split(
                'border-width:')[1].split(';')[0].strip()
        else:
            return False

        parts = border_value.split(' ')
        width = self.get_numeric_part(parts[0].strip())

        return width > 0

    @staticmethod
    def get_numeric_part(width_value: str) -> int:
        """Return the numeric characters from the width_value of the tag
        style"""
        res = ''
        for char in width_value:
            if char.isdigit():
                res += char
        if not res:
            return 0
        return int(res)

    def _has_bottom_border(self, tag: bs4.Tag) -> bool:
        if not tag.get('style', None):
            return False

        if 'border-bottom:' in tag['style']:
            border_bottom_value = tag['style'].split(
                'border-bottom:')[1].split(';')[0].strip()

            parts = border_bottom_value.split(' ')
            bottom_value = parts[0]
        elif 'border:' in tag['style']:
            border_value = tag['style'].split(
                'border:')[1].split(';')[0].strip()
            parts = border_value.split(' ')
            if len(parts) > 2:
                bottom_value = parts[2]
            else:
                bottom_value = parts[0]
        elif 'border-width' in tag['style']:
            border_value = tag['style'].split(
                'border-width:')[1].split(';')[0].strip()
            parts = border_value.split(' ')
            if len(parts) > 2:
                bottom_value = parts[2]
            else:
                bottom_value = parts[0]
        else:
            return False

        width = self.get_numeric_part(bottom_value.strip())

        return width > 0

    def add_border_attributes_to_tables(self,
                                        soup: BeautifulSoup) -> BeautifulSoup:
        """Create a copy of the soup object, identify and mark tds with
        borders using 'hasTopBorder' and 'hasBottomBorder' attributes"""
        soup = copy.copy(soup)
        for table in soup.find_all('table'):
            for td in table.find_all('td'):
                if self._has_top_border(td):
                    td['hasTopBorder'] = True
                if self._has_bottom_border(td):
                    td['hasBottomBorder'] = True
        return soup

    @staticmethod
    def flip_table(table: BeautifulSoup) -> BeautifulSoup:
        """Make a copy of the table object, flip all the tds accross the
        vertical axis and return the modified table soup object"""
        table = copy.copy(table)
        for tr in table.find_all('tr'):
            tr_reversed = tr.contents[::-1]
            tr.clear()
            tr.extend(tr_reversed)
        return table

    @classmethod
    def _has_page_brake_after(cls, tag: BeautifulSoup) -> bool:
        if not tag.get('style', None):
            return False
        style = tag.get('style').lower()
        if 'page-break-after:' not in style:
            return False
        page_break_value = style.split(
                'page-break-after:')[1].split(';')[0].strip()
        return page_break_value == 'always'

    @classmethod
    def _has_page_brake_before(cls, tag: BeautifulSoup) -> bool:
        if not tag.get('style', None):
            return False
        style = tag.get('style').lower()
        if 'page-break-before:' in style:
            page_break_value = style.split('page-break-before:')
            if len(page_break_value) > 1:
                page_break_value = page_break_value[1].split(';')[0].strip()
                return page_break_value == 'always'
        elif 'break-before:' in style:
            return True
            # page_break_value = style.split('break-before:')
            # if len(page_break_value) > 1:
            #     page_break_value = page_break_value[1].split(';')[0].strip()
            #     return page_break_value == 'always'
        return False

    @classmethod
    def _annotate_page_break_w_page_break_after(
            cls, soup: BeautifulSoup) -> tuple[BeautifulSoup, bool]:
        hrs = soup.find_all('hr')
        annotated = False
        for index, hr in enumerate(hrs):
            if cls._has_page_brake_after(hr):
                is_in_PGBK = 'PGBK' in hr.parent.get('class', [])
                previous_div = hr.find_previous_sibling('div')
                previous_sibling_classes = previous_div.get(
                    'class', []) if previous_div else []
                is_after_pgftr = 'PGFTR' in previous_sibling_classes
                is_after_pgnum = 'PGNUM' in previous_sibling_classes
                if is_in_PGBK or is_after_pgftr or is_after_pgnum:
                    base_element = hr.parent
                else:
                    base_element = hr
                page_break = soup.new_tag('page-break')
                base_element.insert_after(page_break)
                annotated = True
        return soup, annotated

    @classmethod
    def _annotate_page_break_w_page_break_before(
            cls, soup: BeautifulSoup) -> tuple[BeautifulSoup, bool]:
        divs = soup.find_all('div')
        annotated = False
        for div in divs:
            if cls._has_page_brake_before(div):
                div.insert_before(soup.new_tag('page-break'))
                annotated = True
        return soup, annotated

    @classmethod
    def _annotate_page_w_comment(
            cls, soup: BeautifulSoup) -> tuple[BeautifulSoup, bool]:
        """Select the element after html
         comment `<!-- Field: /Page -->` and add page-break tag"""
        annotated = False
        comments = soup.find_all(string=lambda text: isinstance(text, Comment))
        for comment in comments:
            if 'Field: /Page' in comment:
                page_break = soup.new_tag('page-break')
                comment.previous_sibling.insert_before(page_break)
                annotated = True
        return soup, annotated

    @classmethod
    def annotate_page_breaks(cls, soup: BeautifulSoup) -> BeautifulSoup:
        """Annotate page breaks with 'page-break' tag"""
        soup = copy.copy(soup)
        soup, annotated = cls._annotate_page_break_w_page_break_after(soup)
        if not annotated:
            soup, _ = cls._annotate_page_w_comment(soup)
        return soup


if __name__ == '__main__':
    import sys
    zip_path = sys.argv[1]
    for zip_file_ in os.listdir(zip_path):
        if not zip_file_.endswith('.zip'):
            continue
    extractor = HtmlExtractor(path=os.path.join(zip_path))
    extractor.extract_tables()
