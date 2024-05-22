import time

from allspice.exceptions import NotYetGeneratedException
from ..allspice import AllSpice
from ..apiobject import Repository

PCB_FOOTPRINT_ATTR_NAME = "PCB Footprint"
PART_REFERENCE_ATTR_NAME = "Part Reference"


def list_components_for_orcad(
    allspice_client: AllSpice,
    repository: Repository,
    dsn_path: str,
    ref: str = "main",
) -> list[dict[str, str]]:
    """
    Get a list of all components in an OrCAD DSN schematic.

    :param client: An AllSpice client instance.
    :param repository: The repository containing the OrCAD schematic.
    :param dsn_path: The path to the OrCAD DSN file from the repo root. For
        example, if the schematic is in the folder "Schematics" and the file
        is named "example.dsn", the path would be "Schematics/example.dsn".
    :param ref: Optional git ref to check. This can be a commit hash, branch
        name, or tag name. Default is "main", i.e. the main branch.
    :return: A list of all components in the OrCAD schematic. Each component is
        a dictionary with the keys being the attributes of the component and the
        values being the values of the attributes. A `_name` attribute is added
        to each component to store the name of the component.
    """

    allspice_client.logger.debug(
        f"Listing components in {dsn_path=} from {repository.get_full_name()} on {ref=}"
    )

    # Get the generated JSON for the schematic.
    dsn_json = _fetch_generated_json(repository, dsn_path, ref)
    pages = dsn_json["pages"]
    components = []

    for page in pages:
        for component in page["components"].values():
            component_attributes = {}
            component_attributes["_name"] = component["name"]
            for attribute in component["attributes"].values():
                component_attributes[attribute["name"]] = attribute["value"]
            components.append(component_attributes)

    return components


def _fetch_generated_json(repo: Repository, file_path: str, ref: str) -> dict:
    attempts = 0
    while attempts < 5:
        try:
            return repo.get_generated_json(file_path, ref=ref)
        except NotYetGeneratedException:
            time.sleep(0.5)

    raise TimeoutError(f"Failed to fetch JSON for {file_path} after 5 attempts.")
