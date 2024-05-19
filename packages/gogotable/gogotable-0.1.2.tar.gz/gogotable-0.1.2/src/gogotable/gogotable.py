def gogotable(headers, rows):  # noqa
    """
    Go Go Table

    :param headers: headers of the table
    :param rows: the data of the table
    :return: a list of strings representing the table
    """

    content_widths = _find_content_widths(headers, rows)
    table = _build_table(content_widths, headers, rows)
    return table


def _build_table(content_widths, headers, rows):
    vb = "|"  # Vertical Border
    hb = "-"  # Horizontal Border
    p = 1  # Padding

    horizontal_border = vb + hb.join(hb * (p + cw + p) for cw in content_widths) + vb
    header_cells = [
        f" {header:^{length}} " for header, length in zip(headers, content_widths)
    ]
    header_line = vb + vb.join(header_cells) + vb

    table = [horizontal_border, header_line, horizontal_border]

    for row in rows:
        cells = [f" {data:>{length}} " for data, length in zip(row, content_widths)]
        table.append(vb + vb.join(cells) + vb)

    table.append(horizontal_border)

    return table


def _find_content_widths(headers, rows):
    """
    Finds the content width for each column content.
    """
    # Initialize the content widths with the length of the headers
    content_widths = [len(header) for header in headers]

    for row in rows:
        for i, cell in enumerate(row):
            content_widths[i] = max(content_widths[i], len(str(cell)))

    return content_widths
