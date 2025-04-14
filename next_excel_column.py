def next_excel_column(current_column, offset):
    """
    Calculate the Excel column letter that is 'offset' columns away from 'current_column'.
    
    Args:
        current_column (str): The starting Excel column letter (e.g., 'A', 'Z', 'AA')
        offset (int): Number of columns to move forward
    
    Returns:
        str: The resulting Excel column letter
    
    Examples:
        next_excel_column('A', 5) -> 'F'
        next_excel_column('Z', 1) -> 'AA'
        next_excel_column('AA', 26) -> 'BA'
    """
    # Convert column letters to a 1-based number
    def column_to_number(col_str):
        num = 0
        for c in col_str:
            num = num * 26 + (ord(c.upper()) - ord('A') + 1)
        return num
    
    # Convert a 1-based number back to column letters
    def number_to_column(num):
        result = ""
        while num > 0:
            num, remainder = divmod(num - 1, 26)
            result = chr(ord('A') + remainder) + result
        return result
    
    # Calculate the new column number
    current_number = column_to_number(current_column)
    new_number = current_number + offset
    
    # Convert back to column letters
    return number_to_column(new_number)