from typing import Any
import requests
from bs4 import BeautifulSoup, Tag
from urllib.parse import urlparse

cache = {}


def get_data_from_url(url: str):
    """
    Takes a url and returns the data associated with that url.
    
    Args:
        - url: The content that will be extracted from the url
    
    """
    if (not url or not isinstance(url, str)):
        raise ValueError(f"The url must not be empty and must be a string. Expected a string but got {type(url)}")
    
    if not(is_url_valid(url)):
        raise ValueError("The url entered is not a valid url")
    
    try:
        resp = requests.get(url)
        if resp.ok:
            return resp.content
    except requests.ConnectionError as e:
        raise ValueError(e)
   

def fetch_table_from_raw_data(raw_data: bytes, element_to_find: str="table") -> BeautifulSoup:
    """
    Takes raw data in bytes, the element to extract from the raw data, and returns
    that element using BeautifulSoup.
    
    Args:
        - raw_data (bytes): The raw data in bytes that will be used by BeautifulSoup.
        - element_to_find (str): The name of the element to search for in the raw data.
        
    Errors:
        - Raises a ValueError if `raw_data` is not in bytes.
        - Raises a TypeError if `element_to_find` is not a string.
    
    Returns:
        - BeautifulSoup element: The first element found that matches `element_to_find`, 
          or None if the element is not found.
    """
    
    if not isinstance(raw_data, bytes):
        raise ValueError(f"The data received must be in bytes. Expected bytes but got {type(raw_data)}")
    if not isinstance(element_to_find, str):
        raise TypeError(f"The element to find must be a string. Expected a string but got {type(element_to_find)}")
    
    soup = BeautifulSoup(raw_data, 'html.parser')
    
    # Check if soup is empty
    if not soup.body or not soup.body.contents:
        return None
    
    return soup.find(element_to_find)


def parse_bs4_coordinate_table(table):
    """
    Extracts coordinate data from a BeautifulSoup table element.

    This function takes a table with three columns and extracts the 'X' and 'Y'
    coordinate columns, excluding the table headers.

    Args:
        table (bs4.element.Tag): A BeautifulSoup table element to extract the coordinates from.

    Dependencies:
        - validate_table

    Raises:
        TypeError: If `table` is not a BeautifulSoup Tag element.
        ValueError: If `table` is not a <table> element or doesn't contain any rows.

    Returns:
        tuple: A tuple containing:
            - A list of dictionaries, where each dictionary contains `x` and `y` coordinates and the pixel character for that position.
            - An integer representing the number of columns in the table. This is used to determine the dimensions of the resulting grid.
    """

    validate_table(table)
     
    data   = []
    column = 0
        
    for row in table.find_all("tr")[1:]:
    
        cells = row.find_all('td')
     
        if (cells):
              
            coordinates = {}
            
            cell1 = cells[0].get_text(strip=True)
            cell2 = cells[1].get_text(strip=True)
            cell3 = cells[2].get_text(strip=True)
         
            if (cell1 and cell2 and cell3):
                    
                coordinates["x"], coordinates["character"], coordinates["y"] = int(cell1), cell2, int(cell3)
                data.append(coordinates)
    
                if coordinates["x"] > column:
                    column = coordinates["x"]
                
    return data, column 


def create_two_dimension_grid(num_rows: int, num_cols: int) -> list:
    """
    Creates a two-dimensional grid (matrix) with the specified number of rows and columns.

    Args:
        num_rows (int): The number of rows (height of the grid).
        num_cols (int): The number of columns (width of each row).

    Raises:
        TypeError: If either argument is not an integer.

    Returns:
        list: A two-dimensional list filled with empty strings.

    Example:
        >>> grid = create_two_dimension_grid(3, 4)
        >>> pprint(grid)
        [['', '', '', ''],
         ['', '', '', ''],
         ['', '', '', '']]
    """

    if not isinstance(num_rows, int) or not isinstance(num_cols, int):
        raise TypeError(f"Both num_rows and num_cols must be integers. Got {type(num_rows)} and {type(num_cols)}")
    
    return [ _create_col(num_cols) for _ in range(num_rows)]



def _create_col(num_cols):
    """
    Creates a one-dimensional row (matrix) with the specified number of columns.

    Args:
        num_cols (int): The number of columns (width of each row).

    Raises:
        TypeError: If either argument is not an integer.

    Returns:
        list: A two-dimensional list filled with  empty X amount of strings for columns.

    Example:
        >>> from pprint import pprint
        
        >>> col = _create_col(4)
        >>> pprint(col)
        ['', '', '', '']
        
        >>> col = _create_col(7)
        >>> pprint(col)
        ['', '', '', '', '', '', '']
          
    """
    
    if not isinstance(num_cols, int):
        raise TypeError(f"num_cols must be integers. Got columns type for columns {type(num_cols)}")
    
    return [''] * num_cols


def add_pixels_to_two_dimensional_grid(grid: list, pixel_data: list[dict]) -> None:
    """
    Plots characters onto a two-dimensional grid using pixel data.

    Args:
        grid (list): A 2D matrix (list of lists) representing the grid.
        pixel_data (list of dict): A list of dictionaries, each containing:
            - 'x' (int): The X-coordinate (column index).
            - 'y' (int): The Y-coordinate (row index).
            - 'character' (str): The character to plot at (x, y).

    Raises:
        ValueError: If grid is not a list or is empty.
        ValueError: If pixel_data is not a list of dictionaries.
        IndexError: If any coordinate is out of bounds.

    Returns:
        None. The grid is modified in place.
    """
    if not isinstance(grid, list) or not grid:
        raise ValueError(f"The grid must be a non-empty list. Got: {type(grid)}")

    if not isinstance(pixel_data, list):
        raise ValueError(f"Pixel data must be a list of dictionaries. Got: {type(pixel_data)}")

    for row in grid:
        if not isinstance(row, list):
            raise ValueError("Each row in the grid must be a list.")
        if not row:
            raise ValueError("Grid contains an empty row (no columns).")

    for coordinates in pixel_data:
        
        if not isinstance(coordinates, dict):
            raise ValueError("Each pixel entry must be a dictionary.")
        
        x = coordinates.get("x")
        y = coordinates.get("y")
        char = coordinates.get("character")

        if not all(isinstance(i, int) for i in [x, y]) or not isinstance(char, str):
            raise ValueError(f"Invalid pixel data: {coordinates}")

        if y >= len(grid) or x >= len(grid[0]):
            raise IndexError(f"Coordinates out of bounds: x={x}, y={y}")

        grid[y][x] = char


def render_grid_message(grid: list) -> None:
    """
    Renders a message from a two-dimensional grid by printing each row.

    Args:
        grid (list): A non-empty 2D list (matrix) where each cell contains
                     a character or is empty (None or '').

    Raises:
        ValueError: If `grid` is not a list or is empty.
        ValueError: If the data within the grid is invalid for rendering.
    """
    if not isinstance(grid, list) or not grid:
        raise ValueError(f"The grid must be a non-empty list. Got: {type(grid)}")

    try:
        for row in grid:
            print(''.join(cell or ' ' for cell in row))
    except (TypeError, AttributeError, IndexError) as e:
        raise ValueError(f"Invalid data in grid: {e}")



def validate_table(table: Tag) -> bool:
    """
    Validates a BeautifulSoup Tag to ensure it is a valid HTML <table> element 
    and contains at least one row.

    Args:
        table (Tag): The BeautifulSoup Tag to validate.

    Returns:
        bool: True if the table is valid.

    Raises:
        TypeError: If the input is not a BeautifulSoup Tag object.
        ValueError: If the tag is not a <table> element.
        ValueError: If the table does not contain any rows.
    """
    if not isinstance(table, Tag):
        raise TypeError("Expected a BeautifulSoup Tag object.")
    if table.name != "table":
        raise ValueError("Expected an HTML <table> element.")
    if not table.find_all("tr"):
        raise ValueError("Table has no rows.")
    return True



def is_url_valid(url):
    """
    Validates whether a URL is well-formed and uses http or https.

    Args:
        url (str): The URL string to validate.

    Returns:
        bool: True if the URL has a valid scheme and netloc, otherwise False.
    """
    if not isinstance(url, str):
        return False

    url = url.strip()
    url_data = urlparse(url)
    is_http_valid = url_data.scheme in ["http", "https"]
    
    return all([is_http_valid, url_data.netloc])


def cache_data(key: str, data: Any):
    
    if not isinstance(cache, dict):
        raise ValueError(f"Cache is not a dictionary, expected a dictionary but got type {type(cache)}")
    if not data:
        raise ValueError("The data cannot be empty")
    
    cache[key] = data
    return True
    

def get_cache(key: str):
    
    if not key:
        raise ValueError("The key cannot be empty")
    if not isinstance(cache, dict):
        raise ValueError(f"Cache is not a dictionary, expected a dictionary but got type {type(cache)}")
    return cache.get(key)


def main():

    url = "https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub"

    KEY = "raw_data"
    
    raw_data = get_cache(KEY)
    
    if not cache.get("raw_data"):
        raw_data  = get_data_from_url(url)
        cache_data(KEY, data=raw_data)

        
    table                          = fetch_table_from_raw_data(raw_data)
    parsed_data, columns_to_create = parse_bs4_coordinate_table(table) 
    grid                           = create_two_dimension_grid(num_rows=columns_to_create, num_cols=columns_to_create + 1)
    
    add_pixels_to_two_dimensional_grid(grid, parsed_data)
    
    grid.reverse()
    
    render_grid_message(grid)

    ## cached so it can call it without needing to calling the `get_data_from_url`
    ## Uncomment to get message
    # render_grid_message(grid)
    # render_grid_message(grid)

if __name__ == "__main__":
    main()