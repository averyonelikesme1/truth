import streamlit as st
import pandas as pd
from pathlib import Path
from utils.logger import logger
from services.verifier import FactVerifier
from config.settings import MAX_FILE_SIZE_MB
from services.report_generator import (
    ReportGenerator
)

from services.pdf_extractor import PDFExtractor
from services.claim_extractor import ClaimExtractor



st.set_page_config(
    page_title="Truth Layer",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ Fact checker")
st.subheader("AI Powered Fact Checking Platform")

st.markdown(
    """
Upload a PDF document and automatically:

- Extract claims
- Verify facts
- Analyze statistics
- Generate evidence-backed reports
"""
)

uploaded_file = st.file_uploader(
    "Upload PDF",
    type=["pdf"]
)
with open(
    f"temp_{uploaded_file.name}",
    "wb"
) as f:
    f.write(uploaded_file.getbuffer())

pdf_data = PDFExtractor.extract(
    f"temp_{uploaded_file.name}"
)

extractor = ClaimExtractor()

claims = extractor.extract_claims(
    pdf_data["full_text"]
)

st.write(claims)
if uploaded_file:

    file_size_mb = (
        uploaded_file.size
        / 1024
        / 1024
    )

    if file_size_mb > MAX_FILE_SIZE_MB:
        st.error(
            f"File exceeds "
            f"{MAX_FILE_SIZE_MB} MB limit."
        )
        st.stop()

    st.success(
        f"Uploaded: {uploaded_file.name}"
    )

    st.info(
        f"Size: {file_size_mb:.2f} MB"
    )

    progress_bar = st.progress(0)

    for i in range(100):
        progress_bar.progress(i + 1)

    st.success(
        "PDF ready for processing."
    )

    dashboard_placeholder = st.empty()

    sample_data = pd.DataFrame({
        "Claim": [],
        "Verdict": [],
        "Confidence": []
    })

    dashboard_placeholder.dataframe(
        sample_data,
        use_container_width=True
    )

st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Claims",
        "0"
    )

with col2:
    st.metric(
        "Verified",
        "0"
    )

with col3:
    st.metric(
        "Inaccurate",
        "0"
    )

with col4:
    st.metric(
        "False",
        "0"
    )



verifier = FactVerifier()

with st.spinner(
    "Verifying claims..."
):
    verified_claims = (
        verifier.verify_batch(
            claims
        )
    )

results_df = pd.DataFrame(
    verified_claims
)

st.subheader(
    "Fact Check Results"
)

st.dataframe(
    results_df,
    use_container_width=True
)


if len(results_df) > 0:

    verified_count = len(
        results_df[
            results_df["verdict"] == "VERIFIED"
        ]
    )

    inaccurate_count = len(
        results_df[
            results_df["verdict"] == "INACCURATE"
        ]
    )

    false_count = len(
        results_df[
            results_df["verdict"] == "FALSE"
        ]
    )

    avg_confidence = round(
        results_df[
            "confidence"
        ].mean(),
        2
    )

    st.markdown("---")

    c1, c2, c3, c4, c5 = st.columns(5)

    c1.metric(
        "Total Claims",
        len(results_df)
    )

    c2.metric(
        "Verified",
        verified_count
    )

    c3.metric(
        "Inaccurate",
        inaccurate_count
    )

    c4.metric(
        "False",
        false_count
    )

    c5.metric(
        "Avg Confidence",
        f"{avg_confidence}%"
    )

    st.markdown("---")

    verdict_filter = st.multiselect(
        "Filter by Verdict",
        options=[
            "VERIFIED",
            "INACCURATE",
            "FALSE"
        ],
        default=[
            "VERIFIED",
            "INACCURATE",
            "FALSE"
        ]
    )

    filtered_df = results_df[
        results_df["verdict"]
        .isin(verdict_filter)
    ]

    st.dataframe(
        filtered_df,
        use_container_width=True
    )

    st.subheader(
        "Verdict Distribution"
    )

    verdict_chart = (
        filtered_df["verdict"]
        .value_counts()
    )

    st.bar_chart(
        verdict_chart
    )

    report_generator = (
        ReportGenerator()
    )

    report_path = (
        report_generator.generate(
            verified_claims
        )
    )

    with open(
        report_path,
        "rb"
    ) as pdf_file:

        st.download_button(
            label="Download PDF Report",
            data=pdf_file,
            file_name="truth_layer_report.pdf",
            mime="application/pdf"
        )
