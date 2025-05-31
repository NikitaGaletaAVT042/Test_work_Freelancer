import pandas as pd
import logging

logger = logging.getLogger(__name__)

REQUIRED_COLUMNS = {
    "Freelancer_ID",
    "Job_Category",
    "Platform",
    "Experience_Level",
    "Client_Region",
    "Payment_Method",
    "Job_Completed",
    "Earnings_USD",
    "Hourly_Rate",
    "Job_Success_Rate",
    "Client_Rating",
    "Job_Duration_Days",
    "Project_Type",
    "Rehire_Rate",
    "Marketing_Spend",
}


def load_data(filepath: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(filepath)
        missing = REQUIRED_COLUMNS - set(df.columns)
        if missing:
            raise ValueError(f"Пропущены обязательные колонки: {', '.join(missing)}")

        return df
    except Exception as e:
        logger.error(f"Ошибка загрузки данных: {e}")
        raise
