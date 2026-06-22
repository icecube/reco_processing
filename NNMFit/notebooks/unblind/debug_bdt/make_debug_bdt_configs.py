"""
Parse make_gradients.sh and create one cfg file per --outfile entry in:
  configs/flavor_globalfit/override/systematics/hese_combined/debug_bdt/<model>/

The model subfolder is read from the `model` variable in make_gradients.sh so
that configs for different models stay separated.

Each cfg overrides [Snowstorm_Gradients_hese_wpriors] with the gradient_pickle
pointing to the corresponding outfile from make_gradients.sh.
"""

import subprocess
from pathlib import Path

SCRIPT = Path(__file__).parent / "make_gradients.sh"
BASE_OUT_DIR = Path(
    "/data/user/tvaneede/GlobalFit/reco_processing/NNMFit/configs/"
    "flavor_globalfit/override/systematics/hese_combined/debug_bdt"
)

SECTION = "Snowstorm_Gradients_hese_wpriors"

TEMPLATE = """\
[{section}]
gradient_pickle = {pickle_path}
"""


def _bash_extract(script_path: Path) -> tuple[str, list[Path]]:
    """Return (model, [outfile paths]) by sourcing shell variables from the script."""
    extract_script = f"""
set -e
source <(grep -E '^(THIS_DIR|dataset|model|outpath|CONFIG_DIR)=' {script_path})
echo "MODEL=$model"
grep -v '^\s*#' {script_path} | grep -- '--outfile' | sed 's/.*--outfile\s\+//' | sed 's/\s.*//' | while read line; do
    eval echo "$line"
done
"""
    result = subprocess.run(
        ["bash", "-c", extract_script],
        capture_output=True,
        text=True,
        check=True,
    )
    lines = result.stdout.strip().splitlines()
    model = ""
    outfiles = []
    for line in lines:
        if line.startswith("MODEL="):
            model = line.removeprefix("MODEL=")
        elif line:
            outfiles.append(Path(line))
    return model, outfiles


def main():
    model, outfiles = _bash_extract(SCRIPT)
    if not outfiles:
        print("No --outfile entries found in make_gradients.sh")
        return

    out_dir = BASE_OUT_DIR / model
    out_dir.mkdir(parents=True, exist_ok=True)

    for pickle_path in outfiles:
        cfg_name = pickle_path.stem + ".cfg"
        cfg_path = out_dir / cfg_name
        content = TEMPLATE.format(section=SECTION, pickle_path=pickle_path)
        cfg_path.write_text(content)
        print(f"Written: {cfg_path}")

    print(f"\nCreated {len(outfiles)} config file(s) in {out_dir}")


if __name__ == "__main__":
    main()
