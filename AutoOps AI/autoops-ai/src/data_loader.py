import pandas as pd


def load_invoice_data(file_path: str) -> pd.DataFrame:
    """
    Load invoice CSV data and perform basic validation + cleaning.
    """

    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

    # Required columns
    required_columns = [
        "invoice_id",
        "customer_name",
        "customer_email",
        "invoice_date",
        "due_date",
        "amount",
        "status",
        "last_reminder_sent",
        "priority",
    ]

    # Check missing columns
    missing_columns = [col for col in required_columns if col not in df.columns]

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    # 🔹 Data Cleaning (important for real-world)
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    # Convert dates
    date_cols = ["invoice_date", "due_date", "last_reminder_sent"]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce")

    # Normalize text columns
    df["status"] = df["status"].str.lower().str.strip()
    df["priority"] = df["priority"].str.lower().str.strip()

    # Fill missing values safely
    df["last_reminder_sent"] = df["last_reminder_sent"].fillna(pd.NaT)

    return df