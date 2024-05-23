"""XBLR parser for GAAP taxonomy"""
import re
from typing import Optional

import anytree
import pandas as pd
from bs4 import BeautifulSoup

from domtag.common import save_to_excel_sheets_output
from domtag.xbrl_parser.concepts import USGAAPAccount


class XBRLGAAPParser:
    """Parse XBRL files with GAAP taxonomy"""
    US_GAAP_RE = re.compile('us-gaap:')

    def __init__(self, instance_xml_path: str,
                 cal_arc_xml_path: Optional[str], output_excel_path: str):
        self.instance_xml_path = instance_xml_path
        self.calc_arc_xml_path = cal_arc_xml_path
        self.output_excel_path = output_excel_path
        self.instance_xml_soup = self._read_instance_xml()
        self.gaap_accounts = self._extract_us_gaap(self.instance_xml_soup)
        if cal_arc_xml_path:
            self.calc_arc_xml_soup = self._read_calc_arc_xml()
            self.nodes = self._construct_tree()
            self.hierarchy_data = self._extract_hierarchy_data()
            self.separate_accounts()
            self.taxonomy = self._extract_taxonomy()

    def _read_instance_xml(self) -> BeautifulSoup:
        with open(self.instance_xml_path, 'r') as f:
            return BeautifulSoup(f.read(), features="xml")

    def _read_calc_arc_xml(self) -> BeautifulSoup:
        with open(self.calc_arc_xml_path, 'r') as f:
            return BeautifulSoup(f.read(), features="xml")

    @classmethod
    def _extract_us_gaap(cls, soup: BeautifulSoup) -> list[USGAAPAccount]:
        us_gaap_accounts = []
        context_map = {}
        for el in soup.find_all():
            if el.prefix != 'us-gaap':
                continue
            if 'unitRef' not in el.attrs or not el.text.strip():
                continue
            name = el.name
            context_ref = el.attrs['contextRef']
            decimals = el.attrs.get('decimals')
            idx = el.attrs.get('id', '')
            unit_ref = el.attrs['unitRef']
            value = el.text.strip()
            if context_ref in context_map:
                context = context_map[context_ref]
            else:
                context = soup.find(
                    'context', attrs={'id': context_ref})
                context_map[context_ref] = context
            if not context:
                continue
            entity_id = context.entity.text.strip()
            if context.period.instant:
                start_date = end_date = context.period.instant.text.strip()
            else:
                start_date = context.period.startDate.text.strip()
                end_date = context.period.endDate.text.strip()
            us_gaap_accounts.append(
                USGAAPAccount(
                    name=name,
                    context_ref=context_ref,
                    decimals=decimals,
                    id=idx,
                    unit_ref=unit_ref,
                    value=float(value),
                    entity_id=entity_id,
                    start_date=pd.to_datetime(start_date),
                    end_date=pd.to_datetime(end_date),
                )
            )
        return us_gaap_accounts

    @staticmethod
    def add_weights(nodes: dict[str, anytree.Node]):
        """Add plus or minus weight to each node based on node weight value"""
        for node in nodes.values():
            if 'weight' in node.__dict__:
                # noinspection PyUnresolvedReferences
                if node.weight == 1.0:
                    node.sign = '+'
                elif node.weight == -1.0:
                    node.sign = '-'
                else:
                    # noinspection PyUnresolvedReferences
                    raise Exception(f"Unknown weight {node.weight}")
            else:
                node.sign = ''
        return nodes

    def _construct_tree(self) -> dict[str, anytree.Node]:
        links = self.calc_arc_xml_soup.find_all('link:calculationArc')
        nodes = {}
        for link in links:
            parent_name = link.attrs['xlink:from'].rsplit(
                '_', 1)[0].rsplit('_', 1)[-1]
            child_name = link.attrs['xlink:to'].rsplit(
                '_', 1)[0].rsplit('_', 1)[-1]
            weight = float(link.attrs['weight'])
            if parent_name not in nodes:
                nodes[parent_name] = anytree.Node(parent_name)
            parent_node = nodes[parent_name]
            if child_name not in nodes:
                nodes[child_name] = anytree.Node(child_name)
            child_node = nodes[child_name]
            child_node.parent = parent_node
            child_node.weight = weight
        nodes = self.add_weights(nodes)
        return nodes

    def filter_root_nodes(self) -> list[anytree.Node]:
        """
        Returns root nodes from all nodes
        """
        return [node for node in self.nodes.values()
                if not node.parent and node.children]

    def _extract_hierarchy_data(self) -> dict[str, pd.DataFrame]:
        all_tables = {}
        root_nodes = self.filter_root_nodes()
        for node in root_nodes:
            table_data = []
            for pre, fill, sub_node in anytree.RenderTree(node):
                level = "%s%s %s" % (
                    pre,
                    sub_node.sign,
                    sub_node.name
                )
                items = [i for i in self.gaap_accounts
                         if i.name == sub_node.name]
                table_row = {'parent': (sub_node.parent.name
                                        if sub_node.parent else ''),
                             'level_numeric': sub_node.depth,
                             'name': sub_node.name}
                for item in items:
                    date = item.end_date.strftime("%Y-%m-%d")
                    if date in table_row:
                        continue
                        # acc[date].append({'value': item.value,
                        #                   'id': item.id})
                        # table_row[date].append({'value': item.value,
                        #                         'id': item.id})
                    else:
                        table_row[date] = {'value': item.value,
                                           'id': item.id}
                table_row["level"] = level
                table_data.append(table_row)
            table_df = pd.DataFrame.from_records(table_data)
            # table_df.set_index('name', inplace=True)
            all_tables[node.name] = table_df
        return all_tables

    def _extract_taxonomy(self) -> pd.DataFrame:
        accounts = [df.drop(['level_numeric', 'parent'], axis=1)
                    for df in self.hierarchy_data.values()]
        hierarchy_df = pd.concat(accounts)
        hierarchy_df.sort_index(axis=1, ascending=False, inplace=True)
        hierarchy_df.set_index('level', inplace=True)
        return hierarchy_df

    def separate_accounts(self, save=True) -> dict[str, pd.DataFrame]:
        """Returns dictionary where keys are accounts,
            values are DataFramems of that account. And if save=True
            the result is saved to Excel file
        """
        separate_accounts = {
            node_name: df.drop(['level'], axis=1).set_index('name')
            for node_name, df in self.hierarchy_data.items()}
        if save:
            excel_file = save_to_excel_sheets_output(separate_accounts)
            with open(self.output_excel_path, 'wb') as f:
                # noinspection PyUnresolvedReferences
                f.write(excel_file.getbuffer())
        return separate_accounts


if __name__ == "__main__":
    import os
    from domtag.resources import __file__ as RESOURCE_INIT_FILE
    from domtag.temp import __file__ as TEMP_FOLDER_INIT_FILE

    RESOURCE_PATH = os.path.dirname(RESOURCE_INIT_FILE)
    TEMP_PATH = os.path.dirname(TEMP_FOLDER_INIT_FILE)
    OUTPUT_PATH = os.path.join(TEMP_PATH, 'output_gaap_csvs')
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    XBRL_INSTANCES_PATH = os.path.join(RESOURCE_PATH, 'xbrl_instances')
    OUTPUT_EXCEL_PATH = os.path.join(TEMP_PATH, 'xbrl_excel_outputs')
    os.makedirs(OUTPUT_EXCEL_PATH, exist_ok=True)
    for xml_name in os.listdir(XBRL_INSTANCES_PATH):
        cal_arc_xml_path_ = None
        if xml_name.endswith('neu-20211231_htm.xml'):
            cal_arc_xml_path_ = os.path.join(
                RESOURCE_PATH, 'newmarketcorp/neu-20211231_cal.xml')
        else:
            continue
        if not xml_name.endswith('xml'):
            continue
        xml_path = os.path.join(XBRL_INSTANCES_PATH, xml_name)
        xbrl_name = xml_name.rsplit('.', 1)[0]
        output_excel_path_ = os.path.join(OUTPUT_EXCEL_PATH,
                                          f"{xbrl_name}.xlsx")
        parser = XBRLGAAPParser(instance_xml_path=xml_path,
                                cal_arc_xml_path=cal_arc_xml_path_,
                                output_excel_path=output_excel_path_
                                )
        parser.taxonomy.to_excel(f"/tmp/{xbrl_name}_hierarchy.xlsx")
        df_ = pd.DataFrame.from_records([i.dict()
                                        for i in parser.gaap_accounts])
        if df_.shape[0] < 1:
            print(f"Failed for {xml_name}")
            continue
        df_.set_index('name', inplace=True)
        df_.to_csv(os.path.join(OUTPUT_PATH, xbrl_name + '.csv'))
        print(f"Finished {xml_name}")
        ...
