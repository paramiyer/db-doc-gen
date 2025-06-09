import pandas as pd
import os
import subprocess

def generate_dbml_file(df_schema: pd.DataFrame, output_file_path: str):
    lines = []
    lines.append("// Use DBML to define your database structure")
    lines.append("// Docs: https://dbml.dbdiagram.io/docs\n")

    grouped = df_schema.groupby('Table')

    for table, group in grouped:
        lines.append(f"Table {table} {{")
        for _, row in group.iterrows():
            line = f"  {row['Col']} {row['Data Type'].lower()}"
            annotations = []

            if row['Key'] == 'PK':
                annotations.append("primary key")
            if row.get('Description') and isinstance(row['Description'], str):
                annotations.append(f"note: '{row['Description']}'")

            if annotations:
                line += " [" + ", ".join(annotations) + "]"

            lines.append(line)
        lines.append("}\n")

    # Generate foreign key references
    for _, row in df_schema.iterrows():
        if row['Key'] == 'FK':
            fk_table = row['Table']
            fk_col = row['Col']
            pk_match = df_schema[(df_schema['Col'] == fk_col) & (df_schema['Key'] == 'PK')]
            if not pk_match.empty:
                pk_table = pk_match.iloc[0]['Table']
                pk_col = pk_match.iloc[0]['Col']
                lines.append(f"Ref: {fk_table}.{fk_col} > {pk_table}.{pk_col}")

    # Write to file
    with open(output_file_path, "w") as f:
        f.write("\n".join(lines))

    print(f"✅ DBML file written to: {output_file_path}")


def publish_dbdocs(dbml_file_path: str, project_name: str, username: str):
    try:
        username = username.split("@")[0]
        result = subprocess.run(
            ["dbdocs", "build", dbml_file_path, "--project", project_name],
            check=True,
            capture_output=True,
            text=True
        )
        print("✅ DBML published successfully.")
        print(result.stdout)
        print(f"🔗 View your schema: https://dbdocs.io/{username}/{project_name}")
    except subprocess.CalledProcessError as e:
        print("❌ Failed to publish DBML:")
        print(e.stderr)

