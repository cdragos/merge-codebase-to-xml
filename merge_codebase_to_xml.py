import argparse
import logging
from pathlib import Path
import xml.etree.ElementTree as ET
from xml.dom import minidom


logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

EXTENSIONS = {".py", ".ts", ".jsx", ".js", ".tsx"}


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    Supports --input-dir, --output-file, and multiple --file arguments.
    """
    parser = argparse.ArgumentParser(
        description="Merge specified code files into a single XML file."
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        help="Path to the input directory to scan."
    )
    parser.add_argument(
        "--file",
        type=Path,
        action='append',
        help="Path to an individual file to include. Can be used multiple times."
    )
    parser.add_argument(
        "--output-file",
        type=Path,
        required=True,
        help="Path to the output XML file."
    )
    args = parser.parse_args()

    if not args.input_dir and not args.file:
        parser.error("At least one of --input-dir or --file must be specified.")

    return args


def get_target_files(input_dir: Path, extensions: set[str]) -> list[Path]:
    """
    Recursively get all files in input_dir with the specified extensions.
    """
    return [p for p in input_dir.rglob('*') if p.suffix.lower() in extensions]


def filter_files_by_extension(files: list[Path], extensions: set[str]) -> list[Path]:
    """
    Filter the provided list of files by the specified extensions.
    """
    filtered_files = []
    for file in files:
        if file.suffix.lower() in extensions:
            if file.is_file():
                filtered_files.append(file.resolve())
            else:
                logging.warning(f"'{file}' is not a valid file and will be skipped.")
    return filtered_files


def create_xml_structure(files: set[Path]) -> ET.Element:
    """
    Create an XML structure with the given files.
    Each file is represented as a <file> element with <filename>, <filepath>, and <contents> sub-elements.
    """
    root = ET.Element("codebase")

    for file_path in files:
        file_element = ET.SubElement(root, "file")

        filename_element = ET.SubElement(file_element, "filename")
        filename_element.text = file_path.name

        filepath_element = ET.SubElement(file_element, "filepath")
        filepath_element.text = str(file_path.resolve())

        contents_element = ET.SubElement(file_element, "contents")
        try:
            contents = file_path.read_text(encoding="utf-8")
        except Exception as e:
            contents = f"Error reading file: {e}"

        contents_element.text = contents

    return root


def prettify_xml(elem: ET.Element) -> str:
    """
    Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, "utf-8")
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def main():
    args = parse_arguments()
    output_file = args.output_file

    all_target_files: set[Path] = set()

    # Process input directory if provided
    if args.input_dir:
        input_dir = args.input_dir
        logging.info(f"Scanning directory: {input_dir} for files with extensions: {EXTENSIONS}")
        target_files = get_target_files(input_dir, EXTENSIONS)
        logging.info(f"Found {len(target_files)} files in directory.")
        all_target_files.update(target_files)

    # Process individual files if provided
    if args.file:
        individual_files = filter_files_by_extension(args.file, EXTENSIONS)
        logging.info(f"Adding {len(individual_files)} individual files.")
        all_target_files.update(individual_files)

    logging.info(f"Total unique files to process: {len(all_target_files)}")

    if not all_target_files:
        logging.warning("No files to process. Exiting.")
        return

    logging.info("Creating XML structure...")
    xml_root = create_xml_structure(all_target_files)

    logging.info("Generating pretty XML...")
    pretty_xml = prettify_xml(xml_root)

    # Ensure the output directory exists
    output_dir = output_file.parent
    if not output_dir.exists():
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            logging.info(f"Created output directory: {output_dir}")
        except Exception as e:
            logging.error(f"Error creating output directory '{output_dir}': {e}")
            return

    logging.info(f"Writing to output file: {output_file}")
    try:
        output_file.write_text(pretty_xml, encoding="utf-8")
        logging.info("XML file creation complete.")
    except Exception as e:
        logging.error(f"Error writing to output file '{output_file}': {e}")


if __name__ == "__main__":
    main()
