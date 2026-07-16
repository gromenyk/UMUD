import os
from pathlib import Path
from submission_storage import (
    list_pending_submissions, 
    load_submission, 
    approve_submission, 
    reject_submission,
    upload_benchmark
)
from review_tools import (
    open_submission_csv,
    load_image_benchmark,
    load_video_benchmark,
    build_imagewise_comparison,
    build_video_framewise_comparison,
    build_summary_dataframe,
    build_video_summary_dataframe,
    export_comparison,
    load_acsa_benchmark,
    build_acsa_imagewise_comparison,
    build_acsa_summary_dataframe,
    )

def main():

    while True:

        pending = list_pending_submissions()

        print('=' * 50)
        print("UMUD Benchmark Administration")
        print('=' * 50)
        print()

        print("1) Review pending submissions")
        print("2) Upload benchmark")
        print("0) Exit")
        print()

        main_option = input("Select option: ")

        if main_option == "0":
            break
        
        elif main_option == "2":

            print()
            print("=" * 50)
            print("Upload Benchmark")
            print("=" * 50)
            print()

            print("1) Muscle Architecture (Images)")
            print("2) Muscle Architecture (Video)")
            print("3) ACSA Quantification")
            print()

            benchmark_option = input(
                "Select benchmark: "
            )

            if benchmark_option == "1":

                benchmark_task = (
                    "Muscle Architecture (Images)"
                )

            elif benchmark_option == "2":

                benchmark_task = (
                    "Muscle Architecture (Video)"
                )

            elif benchmark_option == "3":

                benchmark_task = (
                    "ACSA Quantification"
                )

            else:

                print("Invalid option.")
                continue

            csv_path = input(
                "CSV path: "
            )

            upload_benchmark(
                benchmark_task,
                csv_path
            )

            print()
            print("Benchmark uploaded successfully.")

            input(
                "\nPress ENTER to continue..."
            )

            continue
        
        if main_option != "1":
            continue

        if len(pending) == 0:
            print("No pending submissions for review")
            input("\nPress ENTER...")
            continue

        print()
        print(f"Pending submissions: {len(pending)}")
        print()

        for index, submission in enumerate(pending, start=1):

            print(f"{index}) {submission['model_name']}")
            print(f"Benchmark: {submission['benchmark_task']}")
            print(f"Submission Date: {submission['submission_date']}")
            print()

        print('0) Back')
        print()

        selection = int(input('Select Submission: '))

        if selection == 0:
            continue
        
        if (
            selection < 1
            or selection > len(pending)
        ):
            print("Invalid selection.")
            input("\nPress ENTER...")
            continue

        selected_submission = pending[selection - 1]

        print()
        print(
            f"You selected: Index {selection}, Model Name: {selected_submission['model_name']}"
        )

        while True:

            print()
            print('=' * 50)
            print('Available Actions')
            print('=' * 50)

            print(f'1) Open submission CSV')
            print(f'2) Generate benchmark comparison report')
            print(f'3) Approve submission')
            print(f'4) Reject submission')
            print(f'5) Go back')
            print()

            action = input("Select action: ")

            if action == '1':
                open_submission_csv(
                    selected_submission['model_name']
                )

            elif action == '2':
                submission = load_submission(
                selected_submission["model_name"]
            )

                if (
                    selected_submission["benchmark_task"]
                    == "Muscle Architecture (Images)"
                ):

                    benchmark = load_image_benchmark()

                    comparison_df = build_imagewise_comparison(
                        submission["predictions"],
                        benchmark,
                        selected_submission["model_name"]
                    )

                    summary_df = build_summary_dataframe(
                        comparison_df,
                        selected_submission["model_name"]
                    )

                elif (
                    selected_submission["benchmark_task"]
                    == "Muscle Architecture (Video)"
                ):

                    benchmark = load_video_benchmark()

                    comparison_df = build_video_framewise_comparison(
                        submission["predictions"],
                        benchmark,
                        selected_submission["model_name"]
                    )

                    summary_df = build_video_summary_dataframe(
                        comparison_df,
                        selected_submission["model_name"]
                    )

                elif (
                    selected_submission["benchmark_task"]
                    == "ACSA Quantification"
                ):

                    benchmark = load_acsa_benchmark()

                    comparison_df = build_acsa_imagewise_comparison(
                        submission["predictions"],
                        benchmark,
                        selected_submission["model_name"]
                    )

                    summary_df = build_acsa_summary_dataframe(
                        comparison_df,
                        selected_submission["model_name"]
                    )

                else:

                    print("Unsupported benchmark task.")
                    continue

                print(comparison_df)
                print()
                print(summary_df)

                if (
                    selected_submission["benchmark_task"]
                    == "Muscle Architecture (Images)"
                ):

                    report_path = export_comparison(
                        summary_df,
                        comparison_df,
                        selected_submission["model_name"]
                    )

                elif (
                    selected_submission["benchmark_task"]
                    == "Muscle Architecture (Video)"
                ):

                    report_path = export_comparison(
                        summary_df,
                        comparison_df,
                        selected_submission["model_name"]
                    )

                elif (
                    selected_submission["benchmark_task"]
                    == "ACSA Quantification"
                ):

                    report_path = export_comparison(
                        summary_df,
                        comparison_df,
                        selected_submission["model_name"]
                    )

            elif action == '3':
                approve_submission(
                    selected_submission['model_name']
                )

                print()
                print(f'{selected_submission["model_name"]} approved succesfully')
                
                input(
                    '\nPress ENTER to return to the submissions list...'
                )

                break

            elif action == '4':
                reject_submission(
                    selected_submission['model_name']
                )

                print()
                print(f'{selected_submission["model_name"]} rejected succesfully')

                input(
                    '\nPress ENTER to return to the submissions list...'
                )

                break

            elif action == '5':
                break

            else:
                print("Invalid option.")
                input("\nPress ENTER...")

if __name__ == '__main__':
    main()