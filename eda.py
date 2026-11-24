import marimo

__generated_with = "0.24.0"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # Introvert vs. Extrovert: Exploratory Data Analysis

    **Project goal:** determine whether the available survey dataset is sufficient for the planned scrollytelling webpage, or whether supplemental data is necessary.

    The evaluation below considers:
    - dataset size and missing/duplicate records
    - class balance and population-context coverage
    - whether the variables contain clear, useful personality differences
    - redundancy among variables
    - whether findings are strong enough for a first prototype
    """)
    return


@app.cell
def _():
    from pathlib import Path

    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from scipy.stats import pointbiserialr

    pd.set_option("display.max_columns", None)
    pd.set_option("display.float_format", lambda value: f"{value:,.3f}")
    plt.style.use("seaborn-v0_8-whitegrid")
    sns.set_context("notebook")

    data_path = Path("data/personality_dataset.csv")
    df = pd.read_csv(data_path)

    print(f"Rows: {df.shape[0]:,}")
    print(f"Columns: {df.shape[1]}")
    print("Columns:", ", ".join(df.columns))
    df.head()
    return df, np, pd, plt, pointbiserialr, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Data quality and completeness
    """)
    return


@app.cell
def _(df, display, pd):
    missing = df.isna().sum()
    missing_pct = 100 * missing / len(df)
    quality = pd.DataFrame({
        "missing_count": missing,
        "missing_pct": missing_pct,
        "unique_values": df.nunique(dropna=True)
    })
    display(quality)

    print(f"Duplicate rows: {df.duplicated().sum():,}")
    print(f"Rows missing at least one value: {df.isna().any(axis=1).sum():,}")
    print(f"Rows missing no values: {df.notna().all(axis=1).sum():,}")

    df.info()
    return (quality,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Interpretation:** Missingness is small and mostly per-column. It is not necessarily a reason to add another dataset: listwise deletion or sensible imputation can preserve most of the sample. Duplicate rows should be checked because a synthetic or copied source may inflate apparent sample size.
    """)
    return


@app.cell
def _(df, plt, quality, sns):
    _fig, _axes = plt.subplots(2, 1, figsize=(12, 8), gridspec_kw={'height_ratios': [1, 1.4]})
    sns.heatmap(df.isna(), cbar=False, yticklabels=False, cmap=['#E7EEF6', '#E66A50'], ax=_axes[0])
    _axes[0].set_title('Missing-value map')
    quality['missing_pct'].sort_values().plot.barh(ax=_axes[1], color='#5B8DB8')
    _axes[1].set_xlabel('Percent missing')
    _axes[1].set_title('Missing values by column')
    plt.tight_layout()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Target balance
    """)
    return


@app.cell
def _(df, display, pd, plt):
    class_counts = df['Personality'].value_counts(dropna=False)
    class_pct = 100 * df['Personality'].value_counts(normalize=True)
    balance = pd.DataFrame({'count': class_counts, 'percent': class_pct})
    display(balance)
    _fig, _ax = plt.subplots(figsize=(7, 5))
    colors = ['#5B8DB8', '#E59F48']
    _ax.bar(balance.index.astype(str), balance['count'], color=colors)
    _ax.set_title('Personality class balance')
    _ax.set_xlabel('Personality')
    _ax.set_ylabel('Responses')
    for index, _count in enumerate(balance['count']):
        _ax.text(index, _count + 20, f'{_count:,}', ha='center')
    plt.tight_layout()
    return (class_pct,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Interpretation:** The target classes should be balanced enough to support fair descriptive comparisons. Do not rely on a large class-size difference to explain differences in visualized patterns.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Numeric variable distributions
    """)
    return


@app.cell
def _(df, display, plt, sns):
    numeric = ['Time_spent_Alone', 'Social_event_attendance', 'Going_outside', 'Friends_circle_size', 'Post_frequency']
    display(df[numeric].describe().T)
    _fig, _axes = plt.subplots(2, 3, figsize=(15, 8))
    _axes = _axes.ravel()
    for _ax, _column in zip(_axes, numeric):
        sns.histplot(data=df, x=_column, hue='Personality', bins=16, kde=True, palette={'Introvert': '#5B8DB8', 'Extrovert': '#E59F48'}, alpha=0.55, ax=_ax)
        _ax.set_title(_column.replace('_', ' '))
    _axes[-1].axis('off')
    plt.tight_layout()
    return (numeric,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Personality differences
    """)
    return


@app.cell
def _(df, display, numeric, plt, sns):
    group_means = df.groupby('Personality')[numeric].mean().T
    display(group_means)
    _fig, _axes = plt.subplots(2, 3, figsize=(15, 8), sharex=False)
    _axes = _axes.ravel()
    for _ax, _column in zip(_axes, numeric):
        sns.boxplot(data=df, x='Personality', y=_column, hue='Personality', palette={'Introvert': '#5B8DB8', 'Extrovert': '#E59F48'}, legend=False, ax=_ax)
        _ax.set_title(_column.replace('_', ' '))
    _axes[-1].axis('off')
    plt.tight_layout()
    return


@app.cell
def _(df, np, numeric, plt):
    # Normalized group profiles make all variables comparable on one visual.
    normalized = df[numeric].join(df['Personality']).groupby('Personality').mean()
    normalized = (normalized - df[numeric].min()) / (df[numeric].max() - df[numeric].min())
    _fig, _ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(numeric))
    width = 0.38
    _ax.bar(x - width / 2, normalized.loc['Introvert'], width, label='Introvert', color='#5B8DB8')
    _ax.bar(x + width / 2, normalized.loc['Extrovert'], width, label='Extrovert', color='#E59F48')
    _ax.set_xticks(x, [_column.replace('_', ' ') for _column in numeric], rotation=25, ha='right')
    _ax.set_ylabel('Average, scaled 0-1')
    _ax.set_title('Average behavioral profile by personality')
    _ax.legend()
    plt.tight_layout()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Binary behavior variables
    """)
    return


@app.cell
def _(df, display, pd, plt):
    binary_columns = ['Stage_fear', 'Drained_after_socializing']
    for _column in binary_columns:
        ctab = pd.crosstab(df[_column], df['Personality'], normalize='columns') * 100
        display(ctab.rename(columns={'Introvert': 'Introvert %', 'Extrovert': 'Extrovert %'}))
    binary_pct = df.groupby('Personality')[binary_columns].apply(lambda frame: (frame == 'Yes').mean() * 100).T
    binary_pct.plot(kind='bar', figsize=(8, 5), color={'Introvert': '#5B8DB8', 'Extrovert': '#E59F48'})
    plt.ylabel('Percent answering Yes')
    plt.title('Social discomfort indicators')
    plt.xticks(rotation=25, ha='right')
    plt.tight_layout()
    return (binary_columns,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Relationships and redundancy
    """)
    return


@app.cell
def _(df, numeric, pd, plt, pointbiserialr, sns):
    corr = df[numeric].corr()
    _fig, _ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(corr, annot=True, fmt='.2f', cmap='vlag', center=0, vmin=-1, vmax=1, square=True, ax=_ax)
    _ax.set_title('Correlation among numeric variables')
    plt.tight_layout()
    target_binary = (df['Personality'] == 'Extrovert').astype(int)
    effects = {}
    for _column in numeric:
    # Encode the target as a numeric indicator for point-biserial correlations.
        pair = pd.DataFrame({'x': df[_column], 'y': target_binary}).dropna()
        effects[_column] = pointbiserialr(pair['x'], pair['y']).statistic
    effects = pd.Series(effects).sort_values()
    effects.plot.barh(figsize=(8, 5), color='#8064A2')
    plt.xlabel('Correlation with Extrovert (0 = Introvert, 1 = Extrovert)')
    plt.title('Numeric variables: association with personality')
    plt.tight_layout()
    return (effects,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Potential outliers
    """)
    return


@app.cell
def _(df, display, numeric, pd):
    outlier_summary = []
    for _column in numeric:
        values = df[_column].dropna()
        q1, q3 = values.quantile([0.25, 0.75])
        iqr = q3 - q1
        low, high = (q1 - 1.5 * iqr, q3 + 1.5 * iqr)
        _count = ((values < low) | (values > high)).sum()
        outlier_summary.append({'variable': _column, 'IQR_low': low, 'IQR_high': high, 'outlier_count': _count, 'outlier_pct': 100 * _count / len(values)})
    display(pd.DataFrame(outlier_summary).set_index('variable').round(3))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Sufficiency assessment

    Use the following evidence-based checklist for a first scrollytelling prototype:

    - **Narrative coverage:** 2900-scale data can support several comparison and distribution stories.
    - **Missingness:** assess the missing percentages and duplicate count above.
    - **Balance:** a materially imbalanced target may limit how fairly the two groups are compared.
    - **Behavioral signal:** strong separation in this dataset is useful for visual storytelling.
    - **Context:** the source description is limited; there are no clear demographic or geographic columns. It should not be presented as representative of all introverts.

    The final decision is printed below and can be reproduced whenever the dataset changes.
    """)
    return


@app.cell
def _(binary_columns, class_pct, df, effects, pd, quality):
    missing_pct_max = quality['missing_pct'].max()
    duplicate_pct = 100 * df.duplicated().sum() / len(df)
    smallest_class_pct = class_pct.min()
    strongest_numeric_signal = abs(pd.Series(effects)).max()
    has_relevant_binary_variables = all((_column in df.columns for _column in binary_columns))
    prototype_ready = len(df) >= 1000 and missing_pct_max <= 10 and (smallest_class_pct >= 35) and (strongest_numeric_signal >= 0.35) and has_relevant_binary_variables
    # A prototype is sufficient if it has ample records, acceptable missingness,
    # comparable classes, and a clear behavioral signal.
    supplement_needed_for_general_claims = not any((_column.lower() in {'age', 'country', 'gender', 'geography', 'location'} for _column in df.columns))
    print('=== SUPPLEMENTAL-DATA DECISION ===')
    if prototype_ready:
        print('Prototype/EDA verdict: NO supplemental data is needed for the first prototype.')
    else:
        print('Prototype/EDA verdict: Supplemental data is recommended before building the full visualization.')
    if supplement_needed_for_general_claims:
        print('General-population claim verdict: YES — supplement with an independent, context-rich dataset.')
    # Population/generalizability claims require context columns or an independent source.
        print('Reason: the file does not provide age, location/geography, or other demographic context.')
    else:
        print('General-population claim verdict: May be sufficient for claims confined to the represented population.')
    print(f'Rows: {len(df):,}')
    print(f'Largest missing-column percentage: {missing_pct_max:.2f}%')
    print(f'Duplicate-row percentage: {duplicate_pct:.2f}%')
    print(f'Smallest class percentage: {smallest_class_pct:.2f}%')
    print(f'Strongest numeric association with personality: {strongest_numeric_signal:.3f}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Final takeaway

    The notebook should be treated as a decision report, not merely a collection of plots:

    - **For the prototype:** use this dataset to develop the scrollytelling structure and compare core behaviors.
    - **For broad conclusions:** do not describe the respondents as representative of all people or all introverts without a source for that representation.
    - **For the second data pass:** if the project is to claim generalizability, seek independent, non-synthetic survey data with demographics and survey methodology.
    - **For the visualization:** emphasize patterns in the recorded behaviors, explicitly label the data as a survey sample, and avoid treating personality as a rigid category.
    """)
    return


if __name__ == "__main__":
    app.run()
