from __future__ import annotations

from pathlib import Path
from typing import List, Dict

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak,
    Table,
    TableStyle
)

from config.settings import REPORT_DIR
from utils.logger import logger


class ReportGenerator:

    def generate(
        self,
        results: List[Dict]
    ) -> str:

        report_path = (
            REPORT_DIR /
            "fact_check_report.pdf"
        )

        doc = SimpleDocTemplate(
            str(report_path)
        )

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "Truth Layer - Fact Checking Report",
                styles["Title"]
            )
        )

        elements.append(Spacer(1, 20))

        total_claims = len(results)

        verified = len([
            x for x in results
            if x["verdict"] == "VERIFIED"
        ])

        inaccurate = len([
            x for x in results
            if x["verdict"] == "INACCURATE"
        ])

        false_claims = len([
            x for x in results
            if x["verdict"] == "FALSE"
        ])

        avg_confidence = round(
            sum(
                x["confidence"]
                for x in results
            ) / max(total_claims, 1),
            2
        )

        summary_data = [
            ["Metric", "Value"],
            ["Total Claims", total_claims],
            ["Verified", verified],
            ["Inaccurate", inaccurate],
            ["False", false_claims],
            ["Average Confidence", avg_confidence]
        ]

        summary_table = Table(summary_data)

        summary_table.setStyle(
            TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.white),
                ('GRID', (0,0), (-1,-1), 1, colors.black)
            ])
        )

        elements.append(summary_table)

        elements.append(
            PageBreak()
        )

        elements.append(
            Paragraph(
                "Detailed Findings",
                styles["Heading1"]
            )
        )

        for index, claim in enumerate(results, start=1):

            elements.append(
                Paragraph(
                    f"<b>Claim {index}</b>",
                    styles["Heading2"]
                )
            )

            elements.append(
                Paragraph(
                    f"Original Claim: {claim['claim']}",
                    styles["BodyText"]
                )
            )

            elements.append(
                Paragraph(
                    f"Verdict: {claim['verdict']}",
                    styles["BodyText"]
                )
            )

            elements.append(
                Paragraph(
                    f"Confidence: {claim['confidence']}%",
                    styles["BodyText"]
                )
            )

            elements.append(
                Paragraph(
                    f"Correct Fact: {claim['correct_fact']}",
                    styles["BodyText"]
                )
            )

            elements.append(
                Paragraph(
                    f"Explanation: {claim['explanation']}",
                    styles["BodyText"]
                )
            )

            elements.append(
                Paragraph(
                    "Sources:",
                    styles["Heading3"]
                )
            )

            for source in claim["sources"]:
                elements.append(
                    Paragraph(
                        source,
                        styles["BodyText"]
                    )
                )

            elements.append(
                Spacer(1, 10)
            )

        doc.build(elements)

        logger.info(
            "PDF report generated successfully."
        )

        return str(report_path)
    