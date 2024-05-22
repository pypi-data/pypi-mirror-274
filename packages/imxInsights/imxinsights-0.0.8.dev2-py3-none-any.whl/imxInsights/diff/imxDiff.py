from collections import OrderedDict
from datetime import datetime, timezone
from typing import Dict, List, Optional

import numpy as np
import pandas as pd
from shapely.geometry.base import BaseGeometry

from imxInsights import DiffStatusEnum
from imxInsights import __version__ as libary_version
from imxInsights.diff.compair import ImxObjectCompare
from imxInsights.repo.imxRepo import SituationRepo
from imxInsights.report.file_info import (
    sort_pandas_dataframe_columns,
    write_situation_info,
)
from imxInsights.report.refDisplay import ImxRefDisplay
from imxInsights.utils.log import logger
from imxInsights.utils.shapely_geojson import GeoJsonFeature, GeoJsonFeatureCollection
from imxInsights.utils.shapely_helpers import ShapelyTransform


class ImxDiff:
    """
    Calculated difference between two imx situations.

    Args:
        situation_repo_1 (SituationRepo):
        situation_repo_2 (SituationRepo):

    """

    def __init__(self, situation_repo_1: SituationRepo, situation_repo_2: SituationRepo):
        self.situation_repo_1 = situation_repo_1
        self.situation_repo_2 = situation_repo_2
        self._diff = list(ImxObjectCompare.object_tree_factory(self.situation_repo_1.tree, self.situation_repo_2.tree))
        self.added_color = "#ff0000"
        self.deleted_color = "#002aff"
        self.change_color = "#3deb34"
        self.no_change_color = "#d9d9d9"

    def _filter_by_types_or_path(self, object_type_or_path: str) -> List[ImxObjectCompare]:
        # TODO: make object_type_or_path a list input to filter sets of types
        search = "path" if "." in object_type_or_path else "tag"
        return [item for item in self._diff if item.__getattribute__(search) == object_type_or_path]

    @staticmethod
    def _create_record_dict(item, geometry: Optional[bool] = False, compact_view: Optional[bool] = True) -> Dict:
        def _get_areas(item: ImxObjectCompare):
            area_a = ""
            area_b = ""

            if item.area_status.name == "INDETERMINATE":
                area_a = "INDETERMINATE"
                area_b = "INDETERMINATE"

            else:
                if item.a is not None:
                    area_a = item.a.area.name
                if item.b is not None:
                    area_b = item.b.area.name
            return area_a, area_b

        def _get_parent(item: ImxObjectCompare):
            parent = ""
            if hasattr(item.a, "parent") and hasattr(item.b, "parent"):
                if item.a.parent is not None and item.b.parent is not None:
                    if item.a.parent.puic != item.b.parent.puic:
                        parent = f"{item.a.parent.puic}->{item.b.parent.puic}"
                    else:
                        parent = f"{item.a.parent.puic}"
            elif hasattr(item.a, "parent") and item.a.parent is not None:
                parent = f"{item.a.parent.puic}"
            elif hasattr(item.b, "parent") and item.b.parent is not None:
                parent = f"{item.b.parent.puic}"

            return parent

        def _get_km(item):
            KM_dict = {}
            if geometry is not None:
                if item.a is not None and item.a.km_values is not None:
                    _ = item.a.km_values
                    KM_dict["lr_km_values_a"] = _[0] if len(_) == 1 else "\n".join(_)
                else:
                    KM_dict["lr_km_values_a"] = None

                if item.b is not None and item.b.km_values is not None:
                    _ = item.b.km_values
                    KM_dict["lr_km_values_b"] = _[0] if len(_) == 1 else "\n".join(_)
                else:
                    KM_dict["lr_km_values_b"] = None
            return KM_dict

        area_a, area_b = _get_areas(item)
        parent = _get_parent(item)
        km_dict = _get_km(item)

        props = {
            "puic": item.puic,
            "path": item.path,
            "tag": item.tag,
            "area_a": area_a,
            "area_b": area_b,
            "area_status": item.area_status.name,
            "diff_status": item.diff_status.name,
        }

        imx_props = item.changes.to_dict(compact=compact_view)

        if "@puic" in imx_props.keys():
            del imx_props["@puic"]

        return props | imx_props | {"parent": parent} | km_dict  # | geometry_dict

    def _get_all_as_record_dict_path_is_key(self, geometry: Optional[bool] = False) -> OrderedDict[str, List[Dict]]:
        record_dict = OrderedDict()

        for item in self._diff:
            record = self._create_record_dict(item, geometry)

            if item.path in record_dict.keys():
                record_dict[item.path].append(record)
            else:
                record_dict[item.path] = [record]

        return record_dict

    @staticmethod
    def _get_dataframe_from_records(records: List[Dict]):
        df = pd.DataFrame.from_records(records)
        df["index"] = df["puic"]
        df.set_index("index", inplace=True)
        df = df.fillna("")
        return df

    def get_by_status(self, status: Optional[List[DiffStatusEnum]] = None, object_type_or_path: Optional[str] = None) -> List[ImxObjectCompare]:
        data = self._filter_by_types_or_path(object_type_or_path) if object_type_or_path else self._diff
        return [item for item in data if item.diff_status in status]

    def get_by_puic(self, puic: str) -> ImxObjectCompare:
        return [item for item in self._diff if item.puic == puic][0]

    def get_by_type(self, imx_types: List[str]) -> List[ImxObjectCompare]:
        return [item for item in self._diff if item.tag in imx_types]

    def get_by_path(self, paths: List[str]) -> List[ImxObjectCompare]:
        return [item for item in self._diff if item.path in paths]

    @classmethod
    def _add_zero_index(cls, df):
        # todo: move to utils and use in population view of situation as well
        # Check if there's a column containing ".0."
        if any(".0." in path for path in df.columns):
            # Extract the column without ".0."
            columns_with_zero = [_ for _ in list(df.columns) if ".0." in _]
            # replace the .0. and find the non zero'ed colum
            columns_without_zero = [_.replace(".0.", ".") for _ in columns_with_zero]
            columns_to_change = [_ for _ in df.columns if _ in columns_without_zero]
            column_mapping = list(zip(columns_to_change, columns_with_zero))

            for item in column_mapping:
                df[item[1]].replace("", np.nan, inplace=True)
                df[item[1]].fillna(df[item[0]], inplace=True)
                df[item[1]].replace(np.nan, "", inplace=True)
                del df[item[0]]

        return df

    def pandas_dataframe_dict(self, geometry: Optional[bool] = False) -> Dict[str, pd.DataFrame]:
        """
        Returns a dictionary of all difference as pandas dataframe, key is path of imx object.

        Args:
            geometry: boolean if True include wkt_hex.

        Returns
            dict of all object pandas dataframes.
        """
        dataframe_dict = {key: self._get_dataframe_from_records(value) for key, value in self._get_all_as_record_dict_path_is_key(geometry).items()}
        return {key: self._add_zero_index(value) for key, value in dataframe_dict.items()}

    def pandas_dataframe(self, object_type_or_path: str = None, geometry: Optional[bool] = False) -> pd.DataFrame:
        """
        Returns the differences as a pandas DataFrame.

        Args:
            object_type_or_path (str): The object type or path to return the differences, defaults to None .
            geometry (Optional[bool]): Whether to include the shapely geometry in the DataFrame, defaults to False.

        Returns:
            (pd.DataFrame): A pandas DataFrame representing the filtered differences.
        """
        dataframe = self._get_dataframe_from_records(
            [self._create_record_dict(item, geometry) for item in self._filter_by_types_or_path(object_type_or_path)]
        )
        return self._add_zero_index(dataframe)

    def generate_excel(self, file_path: str, colors: bool = True, ref_display: bool = True, parent_path: bool = True, overview: bool = True) -> None:
        """
        Generates an Excel file that highlights the differences between datasets.

        Each difference is stylized according to its nature (e.g., created, updated, deleted) and can be further
        annotated with references and parent paths if specified.

        This function utilizes formatting to visualize these differences within the Excel file, supporting better
        understanding and analysis of the changes. The coloring scheme (green for updates, red for creations,
        blue for deletions, and gray for no changes), sorts and formats the data according to the specified conditions,
        and then generates an Excel workbook with multiple sheets, each corresponding to different segments
        of the dataset being compared. Each sheet includes a detailed breakdown of changes, with optional reference
        and parent path information, and is formatted for clarity and ease of analysis.

        Args:
            file_path (str): The output file path where the Excel file will be saved.
            colors (bool, optional): If True, applies conditional coloring to highlight different types of
                differences. Defaults to True.
            ref_display (bool, optional): If True, includes reference display information within the Excel
                sheet, enhancing contextual understanding of the differences. Defaults to True.
            parent_path (bool, optional): If True, includes the parent path for each item, providing additional
                hierarchical context. Defaults to True.
            overview (bool, optional): If True, includes a metadata overview sheet.

        """
        sort_status_list = ["CREATED", "UPDATED", "UPGRADED", "NO_CHANGE", "DELETED"]

        def format_diff_status(val):
            if val in ["CREATED"]:
                return f"border: 5px solid {self.added_color}"
            elif val in ["UPDATED", "UPGRADED"]:
                return f"border: 5px solid {self.change_color}"
            elif val in ["DELETED"]:
                return f"border: 3px solid {self.deleted_color}"
            return ""

        def format_moved(val):
            if val in ["MOVED"]:
                return "background-color: #e0e33c"
            return ""

        def format_diff_value(val):
            if isinstance(val, str):
                if val[:3] == "++ ":
                    return f"border: 3px solid {self.added_color}"
                elif " -> " in val:
                    return f"border: 3px solid {self.change_color}"
                elif val[:3] == "-- ":
                    return f"border: 2px solid {self.deleted_color}"
                else:
                    return f"background-color: {self.no_change_color}"
            return ""

        def gray_out_no_change_row(row):
            if row["diff_status"] in ["NO_CHANGE"]:
                return [f"background-color: {self.no_change_color}"] * len(row)
            return [""] * len(row)

        def center_values(val):
            return "text-align: center"

        logger.info("generate Excel diff")
        df_dict = self.pandas_dataframe_dict()

        writer = pd.ExcelWriter(file_path, engine="xlsxwriter")
        workbook = writer.book

        worksheet_info = workbook.add_worksheet("info")

        worksheet_info.set_column(0, 0, 25)
        worksheet_info.set_column(1, 1, 150)

        worksheet_info.write(0, 0, "info")
        worksheet_info.write(1, 0, "process datestamp")
        worksheet_info.write(1, 1, datetime.now().astimezone(timezone.utc).strftime("%Y-%m-%d %H:%M:%S.%f"))
        worksheet_info.write(2, 0, "imxInsight version")
        worksheet_info.write(2, 1, libary_version)

        write_situation_info(worksheet_info, self.situation_repo_1, 4, "a")
        write_situation_info(worksheet_info, self.situation_repo_2, 11, "b")

        worksheet_info.set_tab_color("#6699ff")

        #####################################
        # todo: refactor below to make more readable
        def create_puic_path(df: pd.DataFrame):

            def construct_parent_path(row):
                parent = row["parent"]
                if parent:
                    parent_row = df[df["puic"] == parent].iloc[0]
                    temp = construct_parent_path(parent_row) + "." + parent
                    if temp[0] == ".":
                        return temp[1:]
                    return temp
                else:
                    return ""

            def construct_index(row):
                if "." in row["path"]:
                    path_first = row["path"].split(".")[0]
                    path_last = row["path"].split(".")[-1]
                else:
                    path_first = row["path"]
                    path_last = row["path"]

                if path_first == path_last:
                    return path_first + row["parent_path"] + "." + row["puic"] + ".00000." + row["diff_status"]

                return path_first + "." + row["parent_path"] + "." + row["puic"] + ".00000." + path_last + ".00000." + row["diff_status"]

            # Apply the function to each row
            df["parent_path"] = df.apply(construct_parent_path, axis=1)
            df["new_index"] = df.apply(construct_index, axis=1)

            max_levels = df["path"].str.count(r"\.") + 1
            max_levels = max_levels.max()
            split_columns = [f"lvl{i + 1}" for i in range(max_levels)]
            df[split_columns] = df["path"].str.split(".", expand=True)

            sorted_df = df.sort_values(by=["new_index"])

            sorted_df.set_index("new_index", inplace=False)
            sorted_df.reset_index(drop=True, inplace=True)
            sorted_df = sorted_df[
                ["new_index", "path", "tag", "puic", "area_status", "diff_status"]
                + split_columns
                + ["Metadata.@lifeCycleStatus", "Metadata.@source", "Metadata.@isInService", "Metadata.@registrationTime", "@name"]
            ]

            return sorted_df, split_columns

        basic_columns = ["path", "tag", "puic", "parent", "area_a", "area_b", "area_status", "diff_status", "@name"]
        metadata_columns = list(set([col for key, df in df_dict.items() for col in df.columns if col.startswith("Metadata")]))
        columns_to_keep = basic_columns + [col for col in metadata_columns if col not in basic_columns]
        dfs_with_selected_columns = {
            key: df[[col for col in columns_to_keep if col in columns_to_keep and col in df.columns]] for key, df in df_dict.items()
        }
        concatenated_df = pd.concat(dfs_with_selected_columns.values())

        concatenated_df, split_columns = create_puic_path(concatenated_df)

        overview_sheet = workbook.add_worksheet("meta-overview")

        tree_not_visible_style = workbook.add_format({"font_color": "#FFFFFF"})
        created_style = workbook.add_format({"font_color": "red", "bold": True})
        deleted_style = workbook.add_format({"font_color": "blue", "bold": True, "font_strikeout": True})
        changed_style = workbook.add_format({"font_color": "green", "bold": True})
        error_style = workbook.add_format({"font_color": "purple", "bold": True})

        first_after_levels = 5 + len(split_columns)

        overview_sheet.write(0, 0, "index")
        overview_sheet.write(0, 1, "path")
        overview_sheet.write(0, 2, "tag")
        overview_sheet.write(0, 3, "puic")
        overview_sheet.write(0, 4, "area_status")
        overview_sheet.write(0, 5, "diff_status")
        for i in range(6, (6 + len(split_columns))):
            overview_sheet.write(0, i, f"lvl_{i - len(split_columns)}")

        overview_sheet.write(0, first_after_levels + 1, "@name")
        overview_sheet.write(0, first_after_levels + 2, "Metadata.@lifeCycleStatus")
        overview_sheet.write(0, first_after_levels + 3, "Metadata.@source")
        overview_sheet.write(0, first_after_levels + 4, "Metadata.@isInService")
        overview_sheet.write(0, first_after_levels + 5, "Metadata.@registrationTime")

        for index, row in concatenated_df.iterrows():
            index = index + 1
            status = row["diff_status"]
            if status == "NO_CHANGE":
                cell_format = None
            elif status == "CREATED":
                cell_format = created_style
            elif status == "DELETED":
                cell_format = deleted_style
            elif status in ["UPDATED", "UPGRADED"]:
                cell_format = changed_style
            else:
                cell_format = error_style

            overview_sheet.write(index, 0, index)
            overview_sheet.write(index, 1, row["path"])
            overview_sheet.write(index, 2, row["tag"])
            overview_sheet.write(index, 3, row["puic"])
            overview_sheet.write(index, 4, row["area_status"])
            overview_sheet.write(index, 5, row["diff_status"], cell_format)

            overview_sheet.write(index, first_after_levels + 1, str(row["@name"]))
            overview_sheet.write(index, first_after_levels + 2, str(row["Metadata.@lifeCycleStatus"]))
            overview_sheet.write(index, first_after_levels + 3, str(row["Metadata.@source"]))
            overview_sheet.write(index, first_after_levels + 4, str(row["Metadata.@isInService"]))
            overview_sheet.write(index, first_after_levels + 5, str(row["Metadata.@registrationTime"]))

            for idx, value in enumerate(split_columns, start=1):
                if idx < len(split_columns):
                    if row[split_columns[idx]] is None:
                        overview_sheet.write(index, 5 + idx, row[value], cell_format)
                    else:
                        overview_sheet.write(index, 5 + idx, row[value], tree_not_visible_style)
                else:
                    overview_sheet.write(index, 5 + idx, row[value], cell_format)

        overview_sheet.autofit()

        for i in range(6, (6 + len(split_columns))):
            if i == (6 + len(split_columns) - 1):
                overview_sheet.set_column(i, i, 50)
            else:
                overview_sheet.set_column(i, i, 3)

        overview_sheet.set_column(1, 2, options={"level": 1, "collapsed": True})
        overview_sheet.set_tab_color("#6699ff")

        #####################################

        puic_ref_display = ImxRefDisplay(self.situation_repo_1, self.situation_repo_2)
        wrapped_text = workbook.add_format({"text_wrap": True})

        for key, df in sorted(df_dict.items()):
            logger.info(f"generating sheet {key}")
            # first column order
            column_order_list = ["puic", "path", "tag", "parent", "area_a", "area_b", "area_status", "diff_status", "@name"]
            df = sort_pandas_dataframe_columns(df, column_order_list)

            # todo: get all columns containing a path ".x." and check if one with .0. is present.

            # sort on diff status
            df["diff_status"] = pd.Categorical(df["diff_status"], categories=sort_status_list, ordered=True)
            df = df.sort_values("diff_status")
            df = df.reset_index(drop=True)

            # make color book 😂
            if colors:
                styler = (
                    df.style.map(format_diff_status, subset=["diff_status"])
                    .map(format_moved, subset=["area_status"])
                    .map(format_diff_value)
                    .apply(gray_out_no_change_row, axis=1)
                    .map(center_values, subset=["area_a", "area_b", "area_status", "diff_status"])
                    .set_properties(**{"font-size": "10pt"})
                )
            else:
                styler = df

            if ref_display:
                exclude_columns = ["puic", "parent"]
                df.loc[:, ~df.columns.isin(exclude_columns)] = df.loc[:, ~df.columns.isin(exclude_columns)].map(puic_ref_display.get_display)

            if parent_path:
                df["parent"] = df["parent"].map(puic_ref_display.get_parent_display)

            shorten_sheet_name = f"{key[:14]}...{key[-14:]}" if len(key) > 30 else key
            styler.to_excel(excel_writer=writer, sheet_name=shorten_sheet_name)
            worksheet = writer.sheets[shorten_sheet_name]

            # gray out sheets with no changes
            if list(set(df["diff_status"])) == ["NO_CHANGE"]:
                worksheet.set_tab_color(self.no_change_color)

            # Get the dimensions of the dataframe.
            (max_row, max_col) = df.shape

            worksheet.set_column(0, max_col - 1, None, cell_format=wrapped_text)

            # Set the auto filter.
            worksheet.autofilter(0, 0, max_row, max_col)

            # autofit and freeze header
            worksheet.autofit()
            worksheet.freeze_panes(1, 0)
            if colors:
                worksheet.protect("", {"autofilter": True, "format_cells": True, "objects": True})

        logger.info("save Excel diff as .xlsx file")
        writer.close()

    def as_geojson(self, object_type_or_path: str) -> GeoJsonFeatureCollection:
        """
        Returns a GeoJSON of the differences.

        Args:
            object_type_or_path (str): The object type or path to filter the differences.

        Returns:
            (GeoJsonFeatureCollection): A GeoJsonFeatureCollection representing the filtered differences.
        """
        features = []
        for item in self._filter_by_types_or_path(object_type_or_path):
            difference_dict = item.changes.to_dict()

            if item.b is not None and item.b.km_values:
                km_value_b = item.b.km_values[0] if len(item.b.km_values) == 1 else ", ".join(item.b.km_values) if len(item.b.km_values) != 0 else ""
            else:
                km_value_b = None

            if item.diff_status.value == "DELETED":
                if item.a.km_values:
                    km_value_a = (
                        item.a.km_values[0] if len(item.a.km_values) == 1 else ", ".join(item.a.km_values) if len(item.a.km_values) != 0 else ""
                    )
                else:
                    km_value_a = None
                features.append(
                    GeoJsonFeature(
                        geometry_list=[ShapelyTransform.rd_to_wgs(item.a.shapely if item.a.shapely is not None else BaseGeometry())],
                        properties=difference_dict
                        | {"diff_status": item.diff_status.value, "color": self.deleted_color, "km_a": km_value_a, "path": item.path},
                    )
                )
            elif item.diff_status.value == "CREATED":
                features.append(
                    GeoJsonFeature(
                        geometry_list=[ShapelyTransform.rd_to_wgs(item.b.shapely if item.b.shapely is not None else BaseGeometry())],
                        properties=difference_dict
                        | {"diff_status": item.diff_status.value, "color": self.added_color, "km_b": km_value_b, "path": item.path},
                    )
                )
            elif item.diff_status.value == "UPDATED" or item.diff_status.value == "UPGRADED":
                features.append(
                    GeoJsonFeature(
                        geometry_list=[ShapelyTransform.rd_to_wgs(item.b.shapely if item.b.shapely is not None else BaseGeometry())],
                        properties=difference_dict
                        | {"diff_status": item.diff_status.value, "color": self.change_color, "km_b": km_value_b, "path": item.path},
                    )
                )

            else:
                features.append(
                    GeoJsonFeature(
                        geometry_list=[ShapelyTransform.rd_to_wgs(item.b.shapely if item.b.shapely is not None else BaseGeometry())],
                        properties=difference_dict
                        | {"diff_status": item.diff_status.value, "color": self.no_change_color, "km_b": km_value_b, "path": item.path},
                    )
                )
        return GeoJsonFeatureCollection(geojson_features=features)

    def _get_all_paths(self):
        return list(set([item.path for item in self._diff]))

    def _get_all_types(self):
        return list(set([item.tag for item in self._diff]))

    def generate_geojson_dict(self, key_based_on_type: bool = False) -> Dict[str, GeoJsonFeatureCollection]:
        """
        Generates all GeoJSONs of the differences.

        Args:
            key_based_on_type (bool): Whether to use object type as the key in the dictionary, defaults to False.

        Returns:
            (Dict[str, GeoJsonFeatureCollection]): A dictionary of GeoJsonFeatureCollections representing the differences.
        """
        # TODO: add area and schema geojson

        out_dict = {}
        if key_based_on_type:
            for imx_type in self._get_all_types():
                out_dict[imx_type] = self.as_geojson(imx_type)

        for imx_path in self._get_all_paths():
            out_dict[imx_path] = self.as_geojson(imx_path)

        return out_dict
