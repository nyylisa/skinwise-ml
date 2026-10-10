import pandas as pd

# Manual mapping of ingredient name -> category.
# Based on the 13 categories defined in actives.ts.
# We label the relevant actives and leave the rest as NON_TARGET.

LABEL_MAP = {
    # RETINOID
    "Retinol": "RETINOID",
    "Retinaldehyde": "RETINOID",
    "Retinyl Palmitate": "RETINOID",
    "Retinyl Retinoate": "RETINOID",
    "Retinyl Propionate": "RETINOID",
    "Hydroxypinacolone Retinoate": "RETINOID",
    "Tretinoin": "RETINOID",
    "Adapalene": "RETINOID",
    "Vitamin A": "RETINOID",

    # DIRECT_ACID
    "Glycolic Acid": "DIRECT_ACID",
    "Salicylic Acid": "DIRECT_ACID",
    "Lactic Acid": "DIRECT_ACID",
    "Mandelic Acid": "DIRECT_ACID",
    "Gluconolactone": "DIRECT_ACID",
    "Lactobionic Acid": "DIRECT_ACID",
    "Tartaric Acid": "DIRECT_ACID",
    "Citric Acid": "DIRECT_ACID",
    "Phytic Acid": "DIRECT_ACID",
    "Willow Bark Extract": "DIRECT_ACID",

    # VITAMIN_C
    "Ascorbic Acid": "VITAMIN_C",
    "L-Ascorbic Acid": "VITAMIN_C",
    "Ascorbyl Glucoside": "VITAMIN_C",
    "Ascorbyl Palmitate": "VITAMIN_C",
    "Magnesium Ascorbyl Phosphate": "VITAMIN_C",
    "Sodium Ascorbyl Phosphate": "VITAMIN_C",
    "Ethyl Ascorbic Acid": "VITAMIN_C",
    "Tetrahexyldecyl Ascorbate": "VITAMIN_C",
    "Vitamin C": "VITAMIN_C",

    # NIACINAMIDE
    "Niacinamide": "NIACINAMIDE",
    "Nicotinamide": "NIACINAMIDE",
    "Vitamin B3": "NIACINAMIDE",

    # PIGMENT_REGULATOR
    "Dioic Acid": "PIGMENT_REGULATOR",
    "Azelaic Acid": "PIGMENT_REGULATOR",
    "Potassium Azeloyl Diglycinate": "PIGMENT_REGULATOR",
    "Arbutin": "PIGMENT_REGULATOR",
    "Kojic Acid": "PIGMENT_REGULATOR",
    "Tranexamic Acid": "PIGMENT_REGULATOR",
    "Thiamidol": "PIGMENT_REGULATOR",
    "Licorice Extract": "PIGMENT_REGULATOR",
    "Neoglucosamine": "PIGMENT_REGULATOR",

    # PEPTIDE
    "Copper Peptide": "PEPTIDE",
    "Copper Palmitoyl Heptapeptide": "PEPTIDE",
    "Copper Heptapeptide-14 Pantothenate": "PEPTIDE",
    "Palmitoyl Oligopeptide": "PEPTIDE",
    "Palmitoyl Nonapeptide": "PEPTIDE",
    "Palmitoyl Pentapeptide": "PEPTIDE",
    "Palmitoyl Glycine": "PEPTIDE",
    "Palmitoyl Heptapeptide": "PEPTIDE",
    "Palmitoyl Decapeptide": "PEPTIDE",
    "Palmitoyl Tetrapeptide": "PEPTIDE",
    "Palmitoyl Tripeptide": "PEPTIDE",
    "Palmitoyl Tripeptide-1": "PEPTIDE",
    "Oligopeptide": "PEPTIDE",
    "Pentapeptide": "PEPTIDE",
    "Dipeptide": "PEPTIDE",
    "Acetyl Tetrapeptide": "PEPTIDE",
    "Acetylarginyltryptophyl Diphenylglycine": "PEPTIDE",
    "Acetyl Tyrosinamide": "PEPTIDE",
    "Arginine/Lysine Polypeptide": "PEPTIDE",
    "Azelaoyl Bis-Dipeptide": "PEPTIDE",
    "Dipeptide Diaminobutyroyl Benzylamide Diacetate": "PEPTIDE",
    "Ferric Hexapeptide": "PEPTIDE",
    "Heptapeptide-15 Palmitate": "PEPTIDE",
    "Myristoyl Nonapeptide": "PEPTIDE",
    "Myristol Pentapeptide": "PEPTIDE",
    "Myristol Hexapeptide": "PEPTIDE",
    "Sh-Oligopeptide": "PEPTIDE",
    "Anti-Ageing Peptides": "PEPTIDE",
    "Carnosine": "PEPTIDE",
    "Symsitive": "PEPTIDE",

    # ANTIOXIDANT
    "Ferulic Acid": "ANTIOXIDANT",
    "Resveratrol": "ANTIOXIDANT",
    "Vitamin E": "ANTIOXIDANT",
    "Green Tea": "ANTIOXIDANT",
    "EGCG": "ANTIOXIDANT",
    "Quercetin": "ANTIOXIDANT",
    "Superoxide Dismutase": "ANTIOXIDANT",
    "Caffeic Acid": "ANTIOXIDANT",
    "Vitamin K1": "ANTIOXIDANT",
    "Moringa Seed Extract": "ANTIOXIDANT",
    "Coffee Seed Extract": "ANTIOXIDANT",
    "Ginkgo Biloba": "ANTIOXIDANT",

    # BARRIER_SUPPORT
    "Ceramides": "BARRIER_SUPPORT",
    "Cholesterol": "BARRIER_SUPPORT",
    "Phytosphingosine": "BARRIER_SUPPORT",
    "Caprooyl Phytosphingosine": "BARRIER_SUPPORT",
    "Caprooyl Sphingosine": "BARRIER_SUPPORT",
    "Squalane": "BARRIER_SUPPORT",
    "Linoleic Acid": "BARRIER_SUPPORT",
    "Linolenic Acid": "BARRIER_SUPPORT",
    "Lecithin": "BARRIER_SUPPORT",
    "Glycosphingolipids": "BARRIER_SUPPORT",
    "Glycoproteins": "BARRIER_SUPPORT",
    "Glycolipids": "BARRIER_SUPPORT",
    "Phospholipids": "BARRIER_SUPPORT",
    "Essential Lipids": "BARRIER_SUPPORT",

    # HUMECTANT
    "Hyaluronic Acid": "HUMECTANT",
    "Vitamin B5": "HUMECTANT",
    "Sodium Lactate": "HUMECTANT",
    "Urea": "HUMECTANT",
    "Trehalose": "HUMECTANT",
    "Natural Moisturising Factors": "HUMECTANT",
    "Humectants": "HUMECTANT",
    "Amino Acids": "HUMECTANT",
    "Alanine": "HUMECTANT",
    "Arginine": "HUMECTANT",
    "Arginine HCL": "HUMECTANT",
    "Arginine PCA": "HUMECTANT",
    "Glycine": "HUMECTANT",
    "Histidine": "HUMECTANT",
    "Isoleucine": "HUMECTANT",
    "Leucine": "HUMECTANT",
    "Lysine": "HUMECTANT",
    "Proline": "HUMECTANT",
    "Serine": "HUMECTANT",
    "Taurine": "HUMECTANT",
    "Threonine": "HUMECTANT",
    "Valine": "HUMECTANT",
    "Yeast Amino Acids": "HUMECTANT",
    "Acetyl Glucosamine": "HUMECTANT",
    "Ectoin": "HUMECTANT",

    # SOOTHING
    "Bisabolol": "SOOTHING",
    "Allantoin": "SOOTHING",
    "Centella Asiatica": "SOOTHING",
    "Chamomile Extract": "SOOTHING",
    "Aloe Vera": "SOOTHING",
    "Avene Thermal Water": "SOOTHING",
    "Oat Extract": "SOOTHING",
    "Marshmallow Root": "SOOTHING",
    "Milk Thistle Extract": "SOOTHING",
    "Willow Herb Extract": "SOOTHING",
    "Blue Mallow Extract": "SOOTHING",
    "Blue Lotus Extract": "SOOTHING",
    "Lily Extract": "SOOTHING",
    "Prickly Pear Extract": "SOOTHING",
    "Endothelyol": "SOOTHING",
    "Golden-Eye Grass Complex": "SOOTHING",
    "Horse Chestnut": "SOOTHING",
    "Naringenin Chalcone": "SOOTHING",
    "Magnesium Sulfate": "SOOTHING",
    "Spent Grain Wax": "SOOTHING",

    # EMOLLIENT
    "Argan Oil": "EMOLLIENT",
    "Jojoba Oil": "EMOLLIENT",
    "Shea Butter": "EMOLLIENT",
    "Avocado Oil": "EMOLLIENT",
    "Sweet Almond Oil": "EMOLLIENT",
    "Sunflower Oil": "EMOLLIENT",
    "Sesame Seed Oil": "EMOLLIENT",
    "Safflower Seed Oil": "EMOLLIENT",
    "Meadowfoam Seed Oil": "EMOLLIENT",
    "Mango Seed Butter": "EMOLLIENT",
    "Evening Primrose Oil": "EMOLLIENT",

    # UV_FILTER
    "Avobenzone": "UV_FILTER",
    "Butyl Methoxydibenzoylmethane": "UV_FILTER",
    "Octinoxate": "UV_FILTER",
    "Octocrylene": "UV_FILTER",
    "Octisalate": "UV_FILTER",
    "Homosalate": "UV_FILTER",
    "Ethylhexyl Salicylate": "UV_FILTER",
    "Ethylhexyl Triazone": "UV_FILTER",
    "Bis-Ethylhexyloxyphenol Methoxyphenyl Triazine": "UV_FILTER",
    "Triazine Diethyl Butamidotriazone": "UV_FILTER",
    "Zinc Oxide": "UV_FILTER",
    "Titanium Dioxide": "UV_FILTER",
    "Mineral UV Filters": "UV_FILTER",
    "Chemical UV Filters": "UV_FILTER",

    # EXTRA
    "Bakuchiol": "RETINOID",
    "Adenosine": "SOOTHING",
    "Beta Glucan": "SOOTHING",
    "Zinc PCA": "PIGMENT_REGULATOR",
    "Zinc": "PIGMENT_REGULATOR",
    "Zinc Gluconate": "PIGMENT_REGULATOR",
    "Zinc Sulfate": "PIGMENT_REGULATOR",
    "Sulfur": "PIGMENT_REGULATOR",
    "Tea Tree Oil": "SOOTHING",
    "Caffeine": "ANTIOXIDANT",
    "Perfluorodecalin": "SOOTHING",
}

def main():
    df = pd.read_csv("data/ingredientsList.csv")
    df = df[df["name"].notna() & (df["name"].str.strip() != "")]

    rows = []
    unmatched = []

    for _, row in df.iterrows():
        name = str(row["name"]).strip()
        category = LABEL_MAP.get(name)
        if category:
            rows.append({"text": name, "label": category})
        else:
            unmatched.append(name)

    # Everything not explicitly mapped is NON_TARGET
    for name in unmatched:
        rows.append({"text": name, "label": "NON_TARGET"})

    # --- ADD MISSING NIACINAMIDE ROWS ---
    rows.extend([
        {"text": "Niacinamide", "label": "NIACINAMIDE"},
        {"text": "Nicotinamide", "label": "NIACINAMIDE"},
        {"text": "Vitamin B3", "label": "NIACINAMIDE"},
    ])

    out = pd.DataFrame(rows)
    out.to_csv("training_data.csv", index=False)

    print(f"Total rows: {len(out)}")
    print()
    print(out["label"].value_counts())
    print()
    print(f"Unmatched (labeled NON_TARGET): {len(unmatched)}")

if __name__ == "__main__":
    main()