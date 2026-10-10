import pandas as pd
from datasets import Dataset
from setfit import SetFitModel, Trainer, TrainingArguments

def balance(df, max_per_class=40):
    parts = []
    for label, group in df.groupby("label"):
        n = min(len(group), max_per_class)
        parts.append(group.sample(n=n, random_state=42))
    return pd.concat(parts).reset_index(drop=True)

def main():
    df = pd.read_csv("training_data.csv")
    extra = pd.read_csv("extra_training.csv")

    df = pd.concat([df, extra], ignore_index=True)
    df = df.drop_duplicates(subset=["text"]).reset_index(drop=True)
    df = df.dropna(subset=["text", "label"])
    df["text"] = df["text"].astype(str)
    df["label"] = df["label"].astype(str)

    print(f"Before balance: {len(df)} rows")
    print(df["label"].value_counts())
    print()

    df = balance(df, max_per_class=40)

    print(f"After balance: {len(df)} rows")
    print(df["label"].value_counts())
    print()

    train_ds = Dataset.from_pandas(df.reset_index(drop=True))

    model = SetFitModel.from_pretrained("BAAI/bge-base-en-v1.5")

    args = TrainingArguments(
        batch_size=16,
        num_epochs=1,
        num_iterations=10,
        eval_strategy="no",
    )

    trainer = Trainer(
        model=model,
        args=args,
        train_dataset=train_ds,
    )
    trainer.train()

    model.save_pretrained("skinwise-setfit-model")
    print("\nModel saved.")

    print("\n── Manual smoke test ──")
    test_cases = [
        ("Retinol", "RETINOID"),
        ("Glycolic Acid", "DIRECT_ACID"),
        ("Niacinamide", "NIACINAMIDE"),
        ("Aqua", "NON_TARGET"),
        ("Adapalene", "RETINOID"),
        ("Tretinoin", "RETINOID"),
        ("Malic Acid", "DIRECT_ACID"),
        ("Tocopherol", "ANTIOXIDANT"),
        ("Ceramide NP", "BARRIER_SUPPORT"),
        ("Sodium Hyaluronate", "HUMECTANT"),
        ("Zinc Oxide", "UV_FILTER"),
        ("Argan Oil", "EMOLLIENT"),
        ("Chamomile Extract", "SOOTHING"),
        ("Matrixyl", "PEPTIDE"),
        ("Tranexamic Acid", "PIGMENT_REGULATOR"),
        ("Glycerin", "HUMECTANT"),
    ]
    correct = 0
    for text, expected in test_cases:
        pred = model([text])[0]
        ok = "✅" if pred == expected else "❌"
        if pred == expected:
            correct += 1
        print(f"  {ok}  {text:25s} → {pred:20s} (expected {expected})")

    print(f"\nManual smoke test: {correct}/{len(test_cases)} correct")

if __name__ == "__main__":
    main()