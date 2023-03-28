#!/usr/bin/env python3
import click
from api import Character, get_n_characters


@click.command()
@click.argument("num_chars", type=click.INT)
@click.option("--verbose", help="Show all characters", is_flag=True)
def main(num_chars: int, verbose):
    if (chars := get_n_characters(n=num_chars)) == "No builds found.":
        return chars
    num_chars = len(chars)
    num_unique_chars = _count_unique_names(chars)
    print(f"num chars: {num_chars}")
    print(f"num unique chars: {num_unique_chars}")
    print(f"Chars are {'all' if (num_unique_chars == num_chars) else 'not'} unique")
    if verbose:
        print(f"---------------------------")
        print("chars:")
        print(chars)


def _count_unique_names(chars: list[Character]) -> int:
    names: dict[str, int] = {}
    for c in chars:
        if c["name"] in names:
            names[c["name"]] += 1
        else:
            names[c["name"]] = 1
    return len(names)


if __name__ == "__main__":
    main()
