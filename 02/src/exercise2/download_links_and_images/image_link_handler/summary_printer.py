class SummaryPrinter:
    # статический, потому что не зависит от состояния
    @staticmethod
    async def print_summary(results: list[tuple[str, str]]) -> None:
        print("\nSummary of succesful and unsuccessful downloads")

        max_url_len = max((len(url)
                          for url, _ in results), default=0)
        col_width_url = min(max(66, max_url_len), 80)
        col_width_status = 10

        border = "+" + "-" * (col_width_url + 2) + "+" + \
            "-" * (col_width_status + 2) + "+"
        header_url = "Link".ljust(col_width_url)
        header_status = "Status".ljust(col_width_status)

        print(border)
        print(f"| {header_url} | {header_status} |")
        print(border)

        for url, status in results:
            url_display = url.ljust(col_width_url)
            status_display = status.ljust(col_width_status)
            print(f"| {url_display} | {status_display} |")

        print(border)
