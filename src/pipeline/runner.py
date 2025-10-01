from src.pipeline.steps import load_inputs, fetch_leads, export_leads


def run_pipeline(
    config: str | None = None,
    sector: str | None = None,
    provincia: str | None = None,
    municipio: str | None = None,
    apiKey: str | None = None,
    max: int | None = None,
    timeoutMs: int | None = None,
    outputDir: str | None = None,
) -> list[dict]:
    """Pipeline 1) load_inputs → 2) fetch_leads → 3) export_leads"""

    # 1) load_inputs
    ctx = load_inputs(
        config=config,
        sector=sector,
        provincia=provincia,
        municipio=municipio,
        apiKey=apiKey,
        max_results=max,
        timeoutMs=timeoutMs,
        outputDir=outputDir,
    )

    # 2) fetch_leads
    leads = fetch_leads(ctx)

    # 3) export_leads
    export_leads(leads, ctx)
    return leads


