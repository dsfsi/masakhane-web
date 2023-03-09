from src.seldon_core_components.app import create_app
from typing  import Tuple, List
from pydoc import locate
import argparse

def parse_args() -> Tuple[argparse.Namespace, List[str]]:
    """parse the following arguments
    --model_handler : the path to the class of the model handler
    --model_path : the path to the model
    --src_lang : the source language
    --trg_lang : the target language
    Returns:
        Tuple[argparse.Namespace, List[str]]: _description_
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_handler", type=str, required=True)
    parser.add_argument("--model_path", type=str, required=True)
    parser.add_argument("--src_lang", type=str, required=True)
    parser.add_argument("--trg_lang", type=str, required=True)
    args, unknown = parser.parse_known_args()
    return args, unknown


def main():
    args, _ = parse_args()
    ModelHandleClass = locate(args.model_handler)
    model_handler = ModelHandleClass(args.model_path, args.src_lang, args.trg_lang)
    app = create_app(model_handler)
    app.run()


if __name__ == "__main__":
    main()
