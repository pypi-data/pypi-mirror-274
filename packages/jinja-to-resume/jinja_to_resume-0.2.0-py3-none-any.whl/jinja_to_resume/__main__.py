from jinja_to_resume import makepdf, parse_resume
import json
import argparse

def main():

    parser = argparse.ArgumentParser(description="Generate a resume from a json file.")
    parser.add_argument("resume", help="The resume json file.")
    parser.add_argument("theme", help="The theme file.")
    parser.add_argument("--output", help="The output pdf file.", default="resume.pdf")
    

    # Example usage:
    # jinja2resume resume.json basic.jinja.html

    args = parser.parse_args()

    resume = parse_resume(open(args.resume).read())

    theme = open(args.theme).read()

    pdf = makepdf(resume, theme)

    with open(args.output, "wb") as f:
        f.write(pdf)

    print(f"PDF saved at {args.output}")


if __name__ == "__main__":
    main()