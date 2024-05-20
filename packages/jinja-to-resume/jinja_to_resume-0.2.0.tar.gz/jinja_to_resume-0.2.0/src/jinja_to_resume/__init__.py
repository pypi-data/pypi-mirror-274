import json
import jsonschema
import pdfkit
from jinja2.sandbox import SandboxedEnvironment
import datetime
import addict

def main():
    with open("data/resume.json") as f:
        resume_str = f.read()

    resume = parse_resume(resume_str)
    validation = validate_schema(json.loads(resume_str))

    if validation:
        print("Schema is invalid: ", validation)
        return

    theme = open("theme/basic.jinja.html").read()
    pdf = makepdf(resume, theme)

    file_path = dest_file_path()
    with open(file_path, "wb") as f:
        f.write(pdf)

    print(f"PDF saved at {file_path}")

def parse_resume(resume: str) -> dict:
    """Parses the resume json and converts the dates to date objects.

    Args:
        resume (str): The resume json.

    Returns:
        dict: The parsed resume json.
    """
    return json.loads(resume, object_hook=date_hook)


def date_hook(json_dict):
    for key, value in json_dict.items():
        if key in {"startDate", "endDate"}:
            # Convert to date object
            json_dict[key] = datetime.datetime.strptime(value, "%Y-%m-%d").date()
    return json_dict

def dest_file_path():
    dir_ = "output"
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{dir_}/resume_{timestamp}.pdf"


def validate_schema(resume):
    with open("jsume/resources/schema.json") as f:
        schema = json.load(f)
    try:
        jsonschema.validate(resume, schema)
    except jsonschema.exceptions.ValidationError as e:
        return e.message

sandbox = SandboxedEnvironment()


def makepdf(resume, theme) -> bytes:
    resume = addict.Dict(resume)
    rendered = sandbox.from_string(theme).render(resume=resume)
    return pdfkit.from_string(rendered)


if __name__ == "__main__":
    main()