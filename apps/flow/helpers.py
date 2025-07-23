def latex_escape(text):
    """LaTeX için özel karakterleri escape eder."""
    if not isinstance(text, str):
        text = str(text)
    replace_map = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
        "\\": r"\textbackslash{}",
    }
    for char, repl in replace_map.items():
        text = text.replace(char, repl)
    return text
