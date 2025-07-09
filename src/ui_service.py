from src.report_service import ReportService
import streamlit as st

class UiService:
    """UI layer for displaying sales reports using Streamlit."""

    def __init__(self, ui_service: ReportService) -> None:
        """Initializes the UiService with a report service.

        Args:
            ui_service (ReportService): Service providing processed report data.
        """
        self.ui = ui_service

    def show_ui(self) -> None:
        """Displays the user interface for selecting and visualizing sales reports.

        Provides a sidebar menu for report selection and displays the corresponding
        data as a styled table. Optionally allows the user to display the data as
        a bar chart or line chart using checkboxes.

        Reports available:
            - Daily total sales
            - Avg sales
            - Trend sales
            - Outlier
        """
        st.title('_Generate Report Sales_')
        st.sidebar.title('Menu')
        choice = st.sidebar.radio(
            "Please select a report",["Daily total sales", "Avg sales", "Trend sales", "Outlier"]
        )

        st.write("Your selected:", choice)
        b_ch = st.checkbox("Bar chart")
        l_ch = st.checkbox("Line chart")
        match choice:
            case "Daily total sales":
                df = self.ui.report_total_price_per_day()
                st.dataframe(df.style.highlight_max(axis=0).format(precision=2))
                if b_ch:
                    st.bar_chart(df.set_index("Day")["Total sales"])
                if l_ch:
                    st.line_chart(df.set_index("Day")["Total sales"])
            case "Avg sales":
                df = self.ui.report_calculate_avg_sales()
                st.dataframe(df.style.highlight_max(axis=0).format(precision=2))
                if b_ch:
                    st.bar_chart(df.set_index("Day")["Avg sales"])
                if l_ch:
                    st.line_chart(df.set_index("Day")["Avg sales"])
            case "Trend sales":
                df = self.ui.report_sales_trend()
                st.dataframe(df.style.highlight_max(axis=0).format(precision=2))
                if b_ch:
                    st.bar_chart(df.set_index("Day")["Sales"])
                if l_ch:
                    st.line_chart(df.set_index("Day")["Sales"])
            case "Outlier":
                df = self.ui.report_detect_outliers()
                st.dataframe(df.style.highlight_max(axis=0).format(precision=2))
                if b_ch:
                    st.bar_chart(df.set_index("Day")["Outlier"])
                if l_ch:
                    st.line_chart(df.set_index("Day")["Outlier"])