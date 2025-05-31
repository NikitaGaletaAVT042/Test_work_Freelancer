import pytest
import pandas as pd
from freelance_nlqa.data_loader import load_data

def test_load_data_success(tmp_path):
    df = pd.DataFrame({
        "Freelancer_ID": [1],
        "Job_Category": ["Web Development"],
        "Platform": ["Upwork"],
        "Experience_Level": ["Expert"],
        "Client_Region": ["US"],
        "Payment_Method": ["PayPal"],
        "Job_Completed": [12],
        "Earnings_USD": [1000],
        "Hourly_Rate": [40],
        "Job_Success_Rate": [95],
        "Client_Rating": [4.8],
        "Job_Duration_Days": [30],
        "Project_Type": ["Fixed"],
        "Rehire_Rate": [0.2],
        "Marketing_Spend": [50]
    })
    file = tmp_path / "data.csv"
    df.to_csv(file, index=False)

    loaded_df = load_data(str(file))
    assert "Earnings_USD" in loaded_df.columns
    assert loaded_df.shape[0] == 1

def test_load_data_missing_columns(tmp_path):
    df = pd.DataFrame({
        "Freelancer_ID": [1],
        "Earnings_USD": [500]
        # пропущены остальные обязательные поля
    })
    file = tmp_path / "data.csv"
    df.to_csv(file, index=False)

    with pytest.raises(ValueError, match="Пропущены обязательные колонки"):
        load_data(str(file))
