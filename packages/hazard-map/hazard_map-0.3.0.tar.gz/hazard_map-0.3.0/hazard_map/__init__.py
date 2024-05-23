import argparse
import os

from termcolor import colored


def main():
    from hazard_map.hazard_map import HazardMap, Kind, ListSheet, MappingSheet

    arguments = parse_arguments()

    print(f"Welcome to {colored('hazard-map', 'yellow')}!")

    print()

    print('The outputs of this script will be saved in the following directory:')
    print(f"\"{colored(arguments.output_directory, 'cyan')}\"")

    print()

    hazard_log = HazardMap(arguments.input_workbook)

    hazard_log.read_lists(
        {
            Kind.HAZARD: ListSheet(
                'HazardsREVISED',
                'Revised_Hazard_ID',
                'Hazard_Name',
                'Description',
                ['Category', 'Sub Category'],
                None,
                None,
            ),
            Kind.CAUSE: ListSheet(
                'CausesREVISED',
                'Revised_Cause_ID',
                'Cause_Name',
                'Description',
                ['Category', 'Sub Category'],
                None,
                None,
            ),
            Kind.CONTROL: ListSheet(
                'ControlsREVISED',
                'Revised_Control_ID',
                'Control_Name',
                'Control Description',
                ['Category', 'Sub Category'],
                'Default Control Strength',
                'Control Type',
            ),
        }
    )

    hazard_log.extract_sheet_mappings(
        [
            MappingSheet('HazardCause Mapping', (0, 0), (1, 1), (2, 2), False),
            MappingSheet('CauseControl Mapping', (0, 0), (1, 1), (2, 2), False),
        ],
        arguments.mapping_regex,
    )
    print(
        'Mappings were successfully extracted from the workbook '
        f"\"{colored(os.path.basename(arguments.input_workbook), 'cyan')}\"!"
    )

    print()

    print(hazard_log.report_kind_counts())
    disconnected_report = hazard_log.report_disconnected_nodes()
    if disconnected_report:
        print()
        print(disconnected_report)

    control_relevance_report = hazard_log.review_relevance(
        Kind.CONTROL, arguments.relevance_report_lines
    )
    if control_relevance_report:
        print()
        print(control_relevance_report)

    print()

    hazard_log.write_to_file(
        arguments.output_directory,
        arguments.output_json,
    )

    hazard_log.draw_graph()
    hazard_log.save_drawing(arguments.output_directory, arguments.plot_dpi)

    print()


def parse_arguments():
    """Uses the argparse library to create a command-line interface for the script."""
    parser = argparse.ArgumentParser(
        prog='hazard-map',
        description='Build and analyze a network model of hazards, causes, and controls',
    )

    parser.add_argument(
        'input_workbook',
        help='The hazard mapping excel file to evaluate',
    )

    parser.add_argument(
        '-o',
        '--output-directory',
        help='Set a directory for the script to save its outputs to',
        default='hazard-log',
        type=str,
    )

    parser.add_argument(
        '-j',
        '--output-json',
        help='Save a json description of the mappings alongside the hazard log',
        default=False,
        type=bool,
        action=argparse.BooleanOptionalAction,
    )

    parser.add_argument(
        '-m',
        '--mapping-regex',
        help='Set a custom regex for identifying mapping pairs',
        default='',
        type=str,
    )

    parser.add_argument(
        '-r',
        '--relevance-report-lines',
        help='Choose the number of lines in the relevance reports',
        default=10,
        type=int,
    )

    parser.add_argument(
        '-d',
        '--plot-dpi',
        help='Set a custom DPI (quality) for the plot output',
        default=None,
        type=int,
    )

    return parser.parse_args()


if __name__ == '__main__':
    main()
