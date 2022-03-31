import random
import string

from urlman.services import GEN_DELIMS


async def generate_shortcode(
    length: int = 8,
    upper_case: bool = True,
    digits: bool = True,
    gen_delims: bool = False,
) -> str:
    """Generate shortcode for URl."""
    temp = string.ascii_lowercase
    if upper_case:
        temp.join(string.ascii_uppercase)
    if digits:
        temp.join(string.digits)
    if gen_delims:
        temp.join(GEN_DELIMS)
    return "".join(
        [random.choice(temp) for i in range(0, length)],
    )
