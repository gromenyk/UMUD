from pathlib import Path
import os
import pandas as pd
import tempfile
import openpyxl

# Option 1 from the menu: open de submission's CSV
def open_submission_csv(model_name):

    submissions_folder = (
        Path(__file__).parent.parent
        / "benchmark_data"
        / "submissions"
    )

    csv_path = submissions_folder / f"{model_name}.csv"

    os.startfile(csv_path)

# Option 2 from the menu: generate the benchmark comparison report

def load_benchmark():

    benchmark_folder = (
        Path(__file__).parent.parent
        / "benchmark_data"
    )

    benchmark_path = (
        benchmark_folder
        / "35_images_benchmark_summary.csv"
    )

    benchmark_df = pd.read_csv(
        benchmark_path,
        sep=";"
    )

    return benchmark_df

def build_imagewise_comparison(
    submission_df,
    benchmark_df,
    model_name
):

    merged_df = pd.merge(submission_df, benchmark_df, on = 'image_id', how = 'left')

    comparison_df = pd.DataFrame({
        'Image': merged_df['image_id'],
        'FL Experts': 
            merged_df['AVG_FL'].round(1).astype(str)
            + ' ± '
            + merged_df['SD_FL'].round(1).astype(str),
        f'{model_name} FL':
            merged_df['fl_mm'].round(1),
        f'{model_name} FL Error':
            (merged_df['AVG_FL'] - merged_df['fl_mm']).abs().round(1),
        'MT Experts':
            merged_df['AVG_MT'].round(1).astype(str)
            + ' ± '
            + merged_df['SD_MT'].round(1).astype(str),
        f'{model_name} MT':
            merged_df['mt_mm'].round(1),
        f'{model_name} MT Error':
            (merged_df['AVG_MT'] - merged_df['mt_mm']).abs().round(1),
        'PA Experts':
            merged_df['AVG_PA'].round(1).astype(str)
            + ' ± '
            + merged_df['SD_PA'].round(1).astype(str),
        f'{model_name} PA':
            merged_df['pa_deg'].round(1),
        f'{model_name} PA Error':
            (merged_df['AVG_PA'] - merged_df['pa_deg']).abs().round(1)
    })

    return comparison_df

def build_summary_dataframe(comparison_df, model_name):
    summary_df = pd.DataFrame({
        'Model': [model_name],
        'FL MAE (mm)': [
            comparison_df[f'{model_name} FL Error'].mean()
        ],
        'MT MAE (mm)': [
            comparison_df[f'{model_name} MT Error'].mean()
        ],
        'PA MAE (°)': [
            comparison_df[f'{model_name} PA Error'].mean()
        ]
    })

    return summary_df

def export_comparison(
    summary_df,
    comparison_df,
    model_name
):

    with tempfile.NamedTemporaryFile(
        suffix=".xlsx",
        prefix=f"{model_name}_",
        delete=False
    ) as tmp:

        report_path = tmp.name

    with pd.ExcelWriter(report_path) as writer:

        summary_df.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        comparison_df.to_excel(
            writer,
            sheet_name="Image-wise Comparison",
            index=False
        )

    return report_path