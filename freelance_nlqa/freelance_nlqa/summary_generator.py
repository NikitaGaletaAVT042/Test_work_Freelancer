import pandas as pd

def generate_data_summary(df: pd.DataFrame, max_categories: int = 10) -> str:
    summary_lines = []

    for col in df.columns:
        summary_lines.append(f"Поле: {col}")
        if pd.api.types.is_numeric_dtype(df[col]):
            desc = df[col].describe()
            median = df[col].median()
            summary_lines.append(
                f"  Тип: числовой\n"
                f"  Среднее: {desc['mean']:.2f}, Медиана: {median:.2f}, "
                f"Стандартное отклонение: {desc['std']:.2f}, Мин: {desc['min']}, Макс: {desc['max']}"
            )
        elif pd.api.types.is_object_dtype(df[col]) or pd.api.types.is_categorical_dtype(df[col]):
            value_counts = df[col].value_counts(normalize=True).head(max_categories)
            summary_lines.append("  Тип: категориальный\n  Топ значений:")
            for val, freq in value_counts.items():
                summary_lines.append(f"    {val}: {freq*100:.1f}%")
        else:
            summary_lines.append(f"  Тип: {df[col].dtype}")
        summary_lines.append("")  # Пустая строка для разделения

    return "\n".join(summary_lines)
