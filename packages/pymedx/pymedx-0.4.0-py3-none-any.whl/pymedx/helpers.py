"""Module for helper functions."""
from typing import Generator, List, Optional, Union, cast

import lxml.etree

from lxml.etree import _Element


def batches(
    iterable: List[str], n: int = 1
) -> Generator[List[str], str, None]:
    """
    Create batches from an iterable.

    Parameters
    ----------
    iterable: Iterable
        the iterable to batch.
    n: Int
        the batch size.

    Returns
    -------
    batches: List
        yields batches of n objects taken from the iterable.
    """
    # Get the length of the iterable
    length = len(iterable)

    # Start a loop over the iterable
    for index in range(0, length, n):
        # Create a new iterable by slicing the original
        yield iterable[index : min(index + n, length)]


def getContent(
    element: _Element,
    path: str,
    default: Optional[str] = None,
    separator: str = "\n",
) -> Optional[Union[str, int]]:
    """
    Retrieve text content of an XML element.

    Parameters
    ----------
    element: Element
        the XML element to parse.
    path: Str
        Nested path in the XML element.
    default: Str
        default value to return when no text is found.

    Returns
    -------
    text: Str
        text in the XML node.
    """
    # Find the path in the element
    result = element.findall(path)

    # Return the default if there is no such element
    if result is None or len(result) == 0:
        return default

    # Extract the text and return it
    return separator.join([sub.text for sub in result if sub.text is not None])


def getContentUnique(
    element: _Element,
    path: str,
    default: Optional[str] = None,
) -> Optional[Union[str, int]]:
    """
    Retrieve text content of an XML element. Returns a unique value.

    Parameters
    ----------
    element: Element
        the XML element to parse.
    path: Str
        Nested path in the XML element.
    default: Str
        default value to return when no text is found.

    Returns
    -------
    text: Str
        text in the XML node.
    """
    # Find the path in the element
    result = cast(List[_Element], element.findall(path))

    # Return the default if there is no such element
    if not result:
        return default

    # Extract the text and return it
    return cast(str, result[0].text)


def getAllContent(
    element: _Element,
    path: str,
    default: Optional[str] = None,
) -> Optional[Union[str, int]]:
    """
    Retrieve text content of an XML element.

    Return all the text inside the path and omit XML tags inside.

    Parameters
    ----------
    element: Element
        the XML element to parse.
    path: Str
        Nested path in the XML element.
    default: Str
        default value to return when no text is found.

    Returns
    -------
    text: str
        text in the XML node.
    """
    # Find the path in the element
    raw_result = element.findall(path)

    # Return the default if there is no such element
    if not raw_result:
        return default

    # Get all text avoiding the tags
    result = cast(
        str,
        lxml.etree.tostring(
            raw_result[0], method="text", encoding="utf-8"
        ).decode("utf-8"),
    )

    # Extract the text and return it
    return " ".join(result.split())


def getAbstract(
    element: _Element,
    path: str,
    default: Optional[str] = None,
) -> Optional[Union[str, int]]:
    """
    Retrieve text content of an XML element.

    Return all the text inside the path and omit XML tags inside.
    and omits abstract-type == scanned-figures

    Parameters
    ----------
    element: Element
        the XML element to parse.
    path: Str
        Nested path in the XML element.
    default: Str
        default value to return when no text is found.

    Returns
    -------
    text: str
        text in the XML node.
    """
    # Find the path in the element
    raw_result = element.findall(path)

    # Return the default if there is no such element
    if not raw_result:
        return default

    if raw_result[0].attrib.get("abstract-type", None) == "scanned-figures":
        return default

    for fig in raw_result[0].iter("fig"):
        parent = fig.getparent()
        if parent is not None:
            parent.remove(fig)

    # Get all text avoiding the tags
    result = cast(
        str,
        lxml.etree.tostring(
            raw_result[0], method="text", encoding="utf-8"
        ).decode("utf-8"),
    )

    # Extract the text and return it
    return " ".join(result.split())
