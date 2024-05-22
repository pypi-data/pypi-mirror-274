# cspell:ignore jsons

from __future__ import annotations

import configparser
from enum import Enum
from logging import Logger
import pathlib
import re
import time
from typing import Optional, Union

from .list_components import list_components_for_orcad

from ..allspice import AllSpice
from ..apiobject import Ref, Repository
from ..exceptions import NotYetGeneratedException

REPETITIONS_REGEX = re.compile(r"Repeat\(\w+,(\d+),(\d+)\)")
QUANTITY_COLUMN_NAME = "Quantity"
DESIGNATOR_COLUMN_NAME = "Designator"


class VariationKind(Enum):
    FITTED_MOD_PARAMS = 0
    NOT_FITTED = 1
    ALT_COMP = 2


ColumnsMapping = dict[str, list[str] | str]
# Maps a sheet name to a list of tuples, where each tuple is a child sheet and
# the number of repetitions of that child sheet in the parent sheet.
SchdocHierarchy = dict[str, list[tuple[str, int]]]
ComponentAttributes = dict[str, str | None]
BomEntry = dict[str, str]
Bom = list[BomEntry]


def generate_bom(
    allspice_client: AllSpice,
    repository: Repository,
    source_file: str,
    columns: ColumnsMapping,
    group_by: Optional[list[str]] = None,
    variant: Optional[str] = None,
    ref: Ref = "main",
) -> Bom:
    """
    Generate a BOM for a project.

    :param allspice_client: The AllSpice client to use.
    :param repository: The repository to generate the BOM for.
    :param source_file: The path to the source file from the root of the
        repository. The source file must be a PrjPcb file for Altium projects
        and a DSN file for OrCAD projects. For example, if the source file is
        in the root of the repository and is named "Archimajor.PrjPcb", the
        path would be "Archimajor.PrjPcb"; if the source file is in a folder
        called "Schematics" and is named "Beagleplay.dsn", the path would be
        "Schematics/Beagleplay.dsn".
    :param columns: A mapping of the columns in the BOM to the attributes in the
        project. The attributes are tried in order, and the first one found is
        used as the value for that column.

        For example, if there should be a "Part Number" column in the BOM, and
        the value for that column can be in the "Part" or "MFN Part#" attributes
        in the project, the following mapping can be used:

                {
                    "Part Number": ["Part", "MFN Part#"]
                }

        In this case, the "Part" attribute will be checked first, and if it is
        not present, the "MFN Part#" attribute will be checked. If neither are
        present, the "Part Number" column in the BOM will be empty.
    :param group_by: A list of columns to group the BOM by. If this is provided,
        the BOM will be grouped by the values of these columns.
    :param variant: The variant of the project to generate the BOM for. If this
        is provided, the BOM will be generated for the specified variant. If
        this is not provided, or is None, the BOM will be generated for the
        default variant. Variants are not supported for OrCAD projects.
    :param ref: The ref, i.e. branch, commit or git ref from which to take the
        project files. Defaults to "main".
    :return: A list of BOM entries. Each entry is a dictionary where the key is
        a column name and the value is the value for that column.
    """

    if source_file.lower().endswith(".prjpcb"):
        project_tool = "altium"
    elif source_file.lower().endswith(".dsn"):
        project_tool = "orcad"
    else:
        raise ValueError(
            "The source file must be a PrjPcb file for Altium projects or a DSN file for OrCAD "
            "projects."
        )

    match project_tool:
        case "altium":
            return generate_bom_for_altium(
                allspice_client,
                repository,
                source_file,
                columns,
                group_by,
                variant,
                ref,
            )
        case "orcad":
            if variant:
                raise ValueError("Variant is not supported for OrCAD projects.")

            return generate_bom_for_orcad(
                allspice_client,
                repository,
                source_file,
                columns,
                group_by,
                ref,
            )


def generate_bom_for_altium(
    allspice_client: AllSpice,
    repository: Repository,
    prjpcb_file: str,
    columns: ColumnsMapping,
    group_by: Optional[list[str]] = None,
    variant: Optional[str] = None,
    ref: Ref = "main",
) -> Bom:
    """
    Generate a BOM for an Altium project.

    :param allspice_client: The AllSpice client to use.
    :param repository: The repository to generate the BOM for.
    :param prjpcb_file: The path to the PrjPcb project file from the root of the
        repository.
    :param columns: A mapping of the columns in the BOM to the attributes in the
        Altium project. The attributes are tried in order, and the first one
        found is used as the value for that column.

        For example, if there  should be a "Part Number" column in the BOM, and
        the value for that column can be in the "Part" or "MFN Part#" attributes
        in the Altium project, the following mapping can be used:

            {
                "Part Number": ["Part", "MFN Part#"]
            }

        In this case, the "Part" attribute will be checked first, and if it is
        not present, the "MFN Part#" attribute will be checked. If neither are
        present, the "Part Number" column in the BOM will be empty.
    :param group_by: A list of columns to group the BOM by. If this is provided,
        the BOM will be grouped by the values of these columns.
    :param ref: The ref, i.e. branch, commit or git ref from which to take the
        project files. Defaults to "main".
    :param variant: The variant of the project to generate the BOM for. If this
        is provided, the BOM will be generated for the specified variant. If
        this is not provided, or is None, the BOM will be generated for the
        default variant.
    :return: A list of BOM entries. Each entry is a dictionary where the key is
        a column name and the value is the value for that column.
    """

    allspice_client.logger.info(
        f"Generating BOM for {repository.get_full_name()=} on {ref=} using {columns=}"
    )
    if group_by is not None:
        for group_column in group_by:
            if group_column not in columns:
                raise ValueError(f"Group by column {group_column} not found in selected columns")
    allspice_client.logger.info(f"Fetching {prjpcb_file=}")

    # Altium adds the Byte Order Mark to UTF-8 files, so we need to decode the
    # file content with utf-8-sig to remove it.
    prjpcb_file_contents = repository.get_raw_file(prjpcb_file, ref=ref).decode("utf-8-sig")

    prjpcb_ini = configparser.ConfigParser()
    prjpcb_ini.read_string(prjpcb_file_contents)

    if variant is not None:
        try:
            variant_details = _extract_variations(variant, prjpcb_ini)
        except ValueError:
            raise ValueError(
                f"Variant {variant} not found in PrjPcb file. "
                "Please check the name of the variant."
            )

    schdoc_files_in_proj = _extract_schdoc_list_from_prjpcb(prjpcb_ini)
    allspice_client.logger.info("Found %d SchDoc files", len(schdoc_files_in_proj))

    schdoc_jsons = {
        schdoc_file: _fetch_generated_json(
            repository,
            _resolve_prjpcb_relative_path(schdoc_file, prjpcb_file),
            ref,
            allspice_client.logger,
        )
        for schdoc_file in schdoc_files_in_proj
    }
    schdoc_entries = {
        schdoc_file: [value for value in schdoc_json.values() if isinstance(value, dict)]
        for schdoc_file, schdoc_json in schdoc_jsons.items()
    }
    schdoc_refs = {
        schdoc_file: [entry for entry in entries if entry.get("type") == "SheetRef"]
        for schdoc_file, entries in schdoc_entries.items()
    }
    independent_sheets, hierarchy = _build_schdoc_hierarchy(schdoc_refs)

    components = []

    for independent_sheet in independent_sheets:
        components.extend(
            _extract_components(
                independent_sheet,
                schdoc_entries,
                hierarchy,
            )
        )

    if variant is not None:
        components = _apply_variations(components, variant_details, allspice_client.logger)

    mapped_components = _map_attributes(components, columns)
    bom = _group_entries(mapped_components, group_by)

    return bom


def generate_bom_for_orcad(
    allspice_client: AllSpice,
    repository: Repository,
    dsn_path: str,
    columns: ColumnsMapping,
    group_by: Optional[list[str]] = None,
    ref: Ref = "main",
) -> Bom:
    """
    Generate a BOM for an OrCAD schematic.

    :param allspice_client: The AllSpice client to use.
    :param repository: The repository to generate the BOM for.
    :param dsn_path: The OrCAD DSN file. This can be a Content object returned
        by the AllSpice API, or a string containing the path to the file in the
        repo.
    :param columns: A mapping of the columns in the BOM to the attributes in the
        OrCAD schematic. The attributes are tried in order, and the first one
        found is used as the value for that column.

        For example, if there  should be a "Part Number" column in the BOM, and
        the value for that column can be in the "Part" or "MFN Part#" attributes
        in the OrCAD schematic, the following mapping can be used:

            {
                "Part Number": ["Part", "MFN Part#"]
            }

        In this case, the "Part" attribute will be checked first, and if it is
        not present, the "MFN Part#" attribute will be checked. If neither are
        present, the "Part Number" column in the BOM will be empty.
    :param group_by: A list of columns to group the BOM by. If this is provided,
        the BOM will be grouped by the values of these columns.
    :param ref: The ref, i.e. branch, commit or git ref from which to take the
        project files. Defaults to "main".
    :return: A list of BOM entries. Each entry is a dictionary where the key is
        a column name and the value is the value for that column.
    """

    allspice_client.logger.debug(
        f"Generating BOM for {repository.get_full_name()=} on {ref=} using {columns=}"
    )
    if group_by is not None:
        for group_column in group_by:
            if group_column not in columns:
                raise ValueError(f"Group by column {group_column} not found in selected columns")
    components = list_components_for_orcad(allspice_client, repository, dsn_path, ref)
    mapped_components = _map_attributes(components, columns)
    bom = _group_entries(mapped_components, group_by)

    return bom


def _get_first_matching_key_value(
    alternatives: Union[list[str], str],
    attributes: dict[str, str | None],
) -> Optional[str]:
    """
    Search for a series of alternative keys in a dictionary, and return the
    value of the first one found.
    """

    if isinstance(alternatives, str):
        alternatives = [alternatives]

    for alternative in alternatives:
        if alternative in attributes:
            return attributes[alternative]

    return None


def _extract_schdoc_list_from_prjpcb(prjpcb_ini: configparser.ConfigParser) -> set[str]:
    """
    Get a list of SchDoc files from a PrjPcb file.
    """

    return {
        section["DocumentPath"]
        for (_, section) in prjpcb_ini.items()
        if "DocumentPath" in section and section["DocumentPath"].endswith(".SchDoc")
    }


def _resolve_prjpcb_relative_path(schdoc_path: str, prjpcb_path: str) -> str:
    """
    Convert a relative path to the SchDoc file to an absolute path from the git
    root based on the path to the PrjPcb file.
    """

    # The paths in the PrjPcb file are Windows paths, and ASH will store the
    # paths as Posix paths. We need to resolve the SchDoc path relative to the
    # PrjPcb path (which is a Posix Path, since it is from ASH), and then
    # convert the result into a posix path as a string for use in ASH.
    schdoc = pathlib.PureWindowsPath(schdoc_path)
    prjpcb = pathlib.PurePosixPath(prjpcb_path)
    return (prjpcb.parent / schdoc).as_posix()


# TODO: Remove this after altium component listing has been refactored to
#   list_components.py.
def _fetch_generated_json(repo: Repository, file_path: str, ref: Ref, logger: Logger) -> dict:
    attempts = 0
    while attempts < 5:
        try:
            return repo.get_generated_json(file_path, ref=ref)
        except NotYetGeneratedException:
            logger.info(f"JSON for {file_path} is not yet generated. Retrying in 0.5s.")
            time.sleep(0.5)

    raise TimeoutError(f"Failed to fetch JSON for {file_path} after 5 attempts.")


def _build_schdoc_hierarchy(
    sheets_to_refs: dict[str, list[dict]],
) -> tuple[set[str], SchdocHierarchy]:
    """
    Build a hierarchy of sheets from a mapping of sheet names to the references
    of their children.

    The output of this function is a tuple of two values:

    1. A set of "independent" sheets, which can be taken to be roots of the
    hierarchy.

    2. A mapping of each sheet that has children to a list of tuples, where each
    tuple is a child sheet and the number of repetitions of that child sheet in
    the parent sheet. If a sheet has no children and is not a child of any other
    sheet, it will be mapped to an empty list.
    """

    hierarchy = {}

    # We start by assuming all sheets are independent.
    independent_sheets = set(sheets_to_refs.keys())
    # This is what we'll use to compare with the sheet names in repetitions.
    sheet_names_downcased = {sheet.lower(): sheet for sheet in independent_sheets}

    for parent_sheet, refs in sheets_to_refs.items():
        if not refs or len(refs) == 0:
            continue

        repetitions = _extract_repetitions(refs)
        for child_sheet, count in repetitions.items():
            child_path = _resolve_child_relative_path(child_sheet, parent_sheet)
            child_name = sheet_names_downcased[child_path.lower()]
            if parent_sheet in hierarchy:
                hierarchy[parent_sheet].append((child_name, count))
            else:
                hierarchy[parent_sheet] = [(child_name, count)]
            independent_sheets.discard(child_name)

    return (independent_sheets, hierarchy)


def _resolve_child_relative_path(child_path: str, parent_path: str) -> str:
    """
    Converts a relative path in a sheet ref to a relative path from the prjpcb
    file.
    """

    child = pathlib.PureWindowsPath(child_path)
    parent = pathlib.PureWindowsPath(parent_path)

    return str(parent.parent / child)


def _extract_repetitions(sheet_refs: list[dict]) -> dict[str, int]:
    """
    Takes a list of sheet references and returns a dictionary of each child
    sheet to the number of repetitions of that sheet in the parent sheet.
    """

    repetitions = {}
    for sheet_ref in sheet_refs:
        sheet_name = (sheet_ref.get("sheet_name", {}) or {}).get("name", "") or ""
        try:
            sheet_file_name = sheet_ref["filename"]
        except Exception:
            raise ValueError(f"Could not find sheet filename in {sheet_ref=}")
        if sheet_file_name is None:
            raise ValueError(
                "Sheet filename is null in for a sheet. Please check sheet references in this "
                "project for an empty file path."
            )
        if match := REPETITIONS_REGEX.search(sheet_name):
            count = int(match.group(2)) - int(match.group(1)) + 1
            if sheet_file_name in repetitions:
                repetitions[sheet_file_name] += count
            else:
                repetitions[sheet_file_name] = count
        else:
            if sheet_file_name in repetitions:
                repetitions[sheet_file_name] += 1
            else:
                repetitions[sheet_file_name] = 1
    return repetitions


def _component_attributes(component: dict) -> ComponentAttributes:
    """
    Extract the attributes of a component into a dict.

    This also adds two properties of the component that are not attributes into
    the dict.
    """

    attributes = {}

    for key, value in component["attributes"].items():
        attributes[key] = value["text"]

    # The properties `part_id` and `description` are present in the top level of
    # the component.
    try:
        attributes["_part_id"] = component["part_id"]
    except KeyError:
        pass
    try:
        attributes["_description"] = component["description"]
    except KeyError:
        pass
    try:
        attributes["_unique_id"] = component["unique_id"]
    except KeyError:
        pass

    return attributes


def _letters_for_repetition(rep: int) -> str:
    """
    Generate the letter suffix for a repetition number. If the repetition is
    more than 26, the suffix will be a combination of letters.
    """

    first = ord("A")
    suffix = ""

    while rep > 0:
        u = (rep - 1) % 26
        letter = chr(u + first)
        suffix = letter + suffix
        rep = (rep - u) // 26

    return suffix


def _append_designator_letters(
    component_attributes: ComponentAttributes,
    repetitions: int,
) -> list[ComponentAttributes]:
    """
    Append a letter to the designator of each component in a list of components
    based on the number of repetitions of each component in the parent sheet.
    """

    if repetitions == 1:
        return [component_attributes]

    try:
        designator = component_attributes[DESIGNATOR_COLUMN_NAME]
    except KeyError:
        raise ValueError(f"Designator not found in {component_attributes=}")

    if designator is None:
        return [component_attributes] * repetitions

    return [
        {
            **component_attributes,
            DESIGNATOR_COLUMN_NAME: f"{designator}{_letters_for_repetition(i)}",
        }
        for i in range(1, repetitions + 1)
    ]


def _extract_components(
    sheet_name: str,
    sheets_to_entries: dict[str, list[dict]],
    hierarchy: SchdocHierarchy,
) -> list[ComponentAttributes]:
    components = []
    if sheet_name not in sheets_to_entries:
        return components

    for entry in sheets_to_entries[sheet_name]:
        if entry["type"] != "Component":
            continue

        component = _component_attributes(entry)
        components.append(component)

    if sheet_name not in hierarchy:
        return components

    for child_sheet, count in hierarchy[sheet_name]:
        child_components = _extract_components(child_sheet, sheets_to_entries, hierarchy)
        if count > 1:
            for component in child_components:
                components.extend(_append_designator_letters(component, count))
        else:
            components.extend(child_components)

    return components


def _map_attributes(
    components: list[ComponentAttributes],
    columns: dict[str, list[str]],
) -> list[BomEntry]:
    """
    Map the attributes of the components to the columns of the BOM using the
    columns mapping. This takes a component as we get it from the JSON and
    returns a dict that can be used as a BOM entry.
    """

    return [
        {
            key: str(_get_first_matching_key_value(value, component) or "")
            for key, value in columns.items()
        }
        for component in components
    ]


def _group_entries(
    components: list[BomEntry],
    group_by: list[str] | None = None,
) -> list[BomEntry]:
    """
    Group components based on a list of columns. The order of the columns in the
    list will determine the order of the grouping.

    :returns: A list of rows which can be used as the BOM.
    """

    # If grouping is off, we just add a quantity of 1 to each component and
    # return early.
    if group_by is None:
        for component in components:
            component[QUANTITY_COLUMN_NAME] = "1"
        return components

    grouped_components = {}
    for component in components:
        key = tuple(component[column] for column in group_by)
        if key in grouped_components:
            grouped_components[key].append(component)
        else:
            grouped_components[key] = [component]

    rows = []

    for components in grouped_components.values():
        row = {}
        for column in group_by:
            # The RHS here shouldn't fail as we've validated the group by
            # columns are all in the column selection.
            row[column] = components[0][column]
        non_group_by = set(components[0].keys()) - set(group_by)
        for column in non_group_by:
            # For each of the values in the non-group-by columns, we take the
            # unique values from all the components and join them with a comma.
            # This is better than taking the non-unique values and joining them
            # with a comma, because it means a user wouldn't have to group by
            # more columns than they want to.
            row[column] = ", ".join(
                # dict.fromkeys retains the insertion order; set doesn't.
                dict.fromkeys(str(component[column]) for component in components).keys()
            )
        row["Quantity"] = str(len(components))
        rows.append(row)

    return rows


def _extract_variations(
    variant: str,
    prjpcb_ini: configparser.ConfigParser,
) -> configparser.SectionProxy:
    """
    Extract the details of a variant from a PrjPcb file.
    """

    available_variants = set()

    for section in prjpcb_ini.sections():
        if section.startswith("ProjectVariant"):
            if prjpcb_ini[section].get("Description") == variant:
                return prjpcb_ini[section]
            else:
                available_variants.add(prjpcb_ini[section].get("Description"))
    raise ValueError(
        f"Variant {variant} not found in PrjPcb file.\n"
        f"Available variants: {', '.join(available_variants)}"
    )


def _apply_variations(
    components: list[dict[str, str | None]],
    variant_details: configparser.SectionProxy,
    logger: Logger,
) -> list[dict[str, str | None]]:
    """
    Apply the variations of a specific variant to the components. This should be
    done before the components are mapped to columns or grouped.

    :param components: The components to apply the variations to.
    :param variant_details: The section of the config file dealing with a
        specific variant.

    :returns: The components with the variations applied.
    """

    # Each item in the list is a pairing of (unique_id, designator), as both are
    # required to identify a component.
    components_to_remove: list[tuple[str, str]] = []
    # When patching components, the ParamVariation doesn't have the unique ID,
    # only a designator. However, ParamVariations follow the Variation entry, so
    # if we note down the last unique id we saw for a designator when going
    # through the variations, we can use that unique id when handling a param
    # variation. This dict holds that information.
    patch_component_unique_id: dict[str, str] = {}
    # The keys are the same as above, and the values are a key-value of the
    # parameter to patch and the value to patch it to.
    components_to_patch: dict[tuple[str, str], tuple[str, str]] = {}

    for key, value in variant_details.items():
        # Note that this is in lowercase, as configparser stores all keys in
        # lowercase.
        if re.match(r"variation[\d+]", key):
            variation_details = dict(details.split("=", 1) for details in value.split("|"))
            try:
                designator = variation_details["Designator"]
                # The unique ID field is a "path" separated by backslashes, and
                # the the unique id we want is the last entry in that path.
                unique_id = variation_details["UniqueId"].split("\\")[-1]
                kind = variation_details["Kind"]
            except KeyError:
                logger.warn(
                    "Designator, UniqueId, or Kind not found in details of variation "
                    f"{variation_details}; skipping this variation."
                )
                continue
            try:
                kind = VariationKind(int(variation_details["Kind"]))
            except ValueError:
                logger.warn(
                    f"Kind {variation_details['Kind']} of variation {variation_details} must be "
                    "either 0, 1 or 2; skipping this variation."
                )
                continue

            if kind == VariationKind.NOT_FITTED:
                components_to_remove.append((unique_id, designator))
            else:
                patch_component_unique_id[designator] = unique_id
        elif re.match(r"paramvariation[\d]+", key):
            variation_id = key.split("paramvariation")[-1]
            designator = variant_details[f"ParamDesignator{variation_id}"]
            variation_details = dict(details.split("=", 1) for details in value.split("|"))
            try:
                unique_id = patch_component_unique_id[designator]
            except KeyError:
                # This can happen sometimes - Altium allows param variations
                # even when the component is not fitted, so we just log and
                # ignore.
                logger.warn(
                    f"ParamVariation{variation_id} found for component {designator} either before "
                    "the corresponding Variation or for a component that is not fitted.\n"
                    "Ignoring this ParamVariation."
                )
                continue

            try:
                parameter_patch = (
                    variation_details["ParameterName"],
                    variation_details["VariantValue"],
                )
            except KeyError:
                logger.warn(
                    f"ParameterName or VariantValue not found in ParamVariation{variation_id} "
                    "details."
                )
                continue

            if (unique_id, designator) in components_to_patch:
                components_to_patch[(unique_id, designator)].append(parameter_patch)
            else:
                components_to_patch[(unique_id, designator)] = [parameter_patch]

    final_components = []

    for component in components:
        identifying_pair = (component["_unique_id"], component[DESIGNATOR_COLUMN_NAME])
        if identifying_pair in components_to_remove:
            continue

        if identifying_pair in components_to_patch:
            new_component = component.copy()
            for parameter, value in components_to_patch[identifying_pair]:
                new_component[parameter] = value
            final_components.append(new_component)
        else:
            final_components.append(component)

    return final_components
