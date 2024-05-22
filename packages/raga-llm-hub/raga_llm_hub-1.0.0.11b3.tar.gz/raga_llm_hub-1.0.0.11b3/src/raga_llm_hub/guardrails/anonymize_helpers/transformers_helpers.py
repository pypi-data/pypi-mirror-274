import importlib
from functools import lru_cache
from typing import Literal, Optional, get_args


# LOGGER = get_#LOGGER(__name__)
def device():
    torch = lazy_load_dep("torch")
    if torch.cuda.is_available():
        return torch.device("cuda:0")
    elif torch.backends.mps.is_available():
        return torch.device("mps")

    return torch.device("cpu")


def lazy_load_dep(import_name: str, package_name: Optional[str] = None):
    """Helper function to lazily load optional dependencies. If the dependency is not
    present, the function will raise an error _when used_.

    NOTE: This wrapper adds a warning message at import time.
    """

    if package_name is None:
        package_name = import_name

    spec = importlib.util.find_spec(import_name)
    if spec is None:
        print(
            f"Optional feature dependent on missing package: {import_name} was initialized.\n"
            f"Use `pip install {package_name}` to install the package if running locally."
        )

    return importlib.import_module(import_name)


@lru_cache(maxsize=None)  # Set maxsize=None for an unbounded cache
def get_tokenizer(model_identifier: str):
    """
    This function loads a tokenizer given a model identifier and caches it.
    Subsequent calls with the same model_identifier will return the cached tokenizer.

    Args:
        model_identifier (str): The model identifier to load the tokenizer for.
    """
    transformers = lazy_load_dep("transformers")
    tokenizer = transformers.AutoTokenizer.from_pretrained(model_identifier)
    return tokenizer


@lru_cache(maxsize=None)  # Unbounded cache
def is_onnx_supported() -> bool:
    is_supported = importlib.util.find_spec("optimum.onnxruntime") is not None
    if not is_supported:
        print(
            "ONNX Runtime is not available. "
            "Please install optimum: "
            "`pip install llm-guard[onnxruntime]` for CPU or "
            "`pip install llm-guard[onnxruntime-gpu]` for GPU to enable ONNX Runtime optimizations."
        )

    return is_supported


def _ort_model_for_sequence_classification(
    model: str, export: bool = False, subfolder: str = ""
):
    if device().type == "cuda":
        optimum_onnxruntime = lazy_load_dep(
            "optimum.onnxruntime", "optimum[onnxruntime-gpu]"
        )
        tf_model = (
            optimum_onnxruntime.ORTModelForSequenceClassification.from_pretrained(
                model,
                export=export,
                subfolder=subfolder,
                file_name="model.onnx",
                provider="CUDAExecutionProvider",
                use_io_binding=True,
            )
        )

        # LOGGER.debug("Initialized classification ONNX model", model=model, device=device())

        return tf_model

    optimum_onnxruntime = lazy_load_dep("optimum.onnxruntime", "optimum[onnxruntime]")
    tf_model = optimum_onnxruntime.ORTModelForSequenceClassification.from_pretrained(
        model,
        export=export,
        subfolder=subfolder,
        file_name="model.onnx",
    )
    # LOGGER.debug("Initialized classification ONNX model", model=model, device=device())

    return tf_model


def get_tokenizer_and_model_for_classification(
    model: str, onnx_model: Optional[str] = None, use_onnx: bool = False, **kwargs
):
    """
    This function loads a tokenizer and model given a model identifier and caches them.
    Subsequent calls with the same model_identifier will return the cached tokenizer.

    Args:
        model (str): The model identifier to load the tokenizer and model for.
        onnx_model (Optional[str]): The model identifier to load the ONNX model for. Defaults to None.
        use_onnx (bool): Whether to use the ONNX version of the model. Defaults to False.
        **kwargs: Keyword arguments to pass to the tokenizer and model.
    """
    tf_tokenizer = get_tokenizer(model)
    transformers = lazy_load_dep("transformers")

    if kwargs.get("max_length", None) is None:
        kwargs["max_length"] = tf_tokenizer.model_max_length

    if use_onnx and is_onnx_supported() is False:
        # LOGGER.warning("ONNX is not supported on this machine. Using PyTorch instead of ONNX.")
        use_onnx = False

    if use_onnx is False:
        tf_model = transformers.AutoModelForSequenceClassification.from_pretrained(
            model
        )
        # LOGGER.debug("Initialized classification model", model=model, device=device())

        return tf_tokenizer, tf_model

    subfolder = "onnx" if onnx_model == model else ""
    if onnx_model is not None:
        model = onnx_model

    # Hack for some models
    tf_tokenizer.model_input_names = ["input_ids", "attention_mask"]

    tf_model = _ort_model_for_sequence_classification(
        model, export=onnx_model is None, subfolder=subfolder
    )

    return tf_tokenizer, tf_model


ClassificationTask = Literal["text-classification", "zero-shot-classification", "ner"]


def pipeline(
    task: str,
    model: str,
    onnx_model: Optional[str] = None,
    use_onnx: bool = False,
    **kwargs,
):
    if task not in get_args(ClassificationTask):
        raise ValueError(f"Invalid task. Must be one of {ClassificationTask}")

    if task == "ner":
        return _pipeline_ner(model, onnx_model, use_onnx, **kwargs)

    transformers = lazy_load_dep("transformers")
    tf_tokenizer, tf_model = get_tokenizer_and_model_for_classification(
        model, onnx_model, use_onnx, **kwargs
    )

    return transformers.pipeline(
        task,
        model=tf_model,
        tokenizer=tf_tokenizer,
        device=device(),
        batch_size=1,
        **kwargs,
    )


def _pipeline_ner(
    model: str, onnx_model: Optional[str] = None, use_onnx: bool = False, **kwargs
):
    transformers = lazy_load_dep("transformers")
    tf_tokenizer = get_tokenizer(model)

    if use_onnx and is_onnx_supported() is False:
        # LOGGER.warning("ONNX is not supported on this machine. Using PyTorch instead of ONNX.")
        use_onnx = False

    if use_onnx:
        subfolder = "onnx" if onnx_model == model else ""
        if onnx_model is not None:
            model = onnx_model

        optimum_onnxruntime = lazy_load_dep(
            "optimum.onnxruntime",
            (
                "optimum[onnxruntime]"
                if device().type != "cuda"
                else "optimum[onnxruntime-gpu]"
            ),
        )
        tf_model = optimum_onnxruntime.ORTModelForTokenClassification.from_pretrained(
            model,
            export=onnx_model is None,
            subfolder=subfolder,
            provider=(
                "CUDAExecutionProvider"
                if device().type == "cuda"
                else "CPUExecutionProvider"
            ),
            use_io_binding=True if device().type == "cuda" else False,
        )
        # LOGGER.debug("Initialized NER ONNX model", model=model, device=device())
    else:
        tf_model = transformers.AutoModelForTokenClassification.from_pretrained(model)
        # LOGGER.debug("Initialized NER model", model=model, device=device())

    return transformers.pipeline(
        "ner",
        model=tf_model,
        tokenizer=tf_tokenizer,
        device=device(),
        batch_size=1,
        **kwargs,
    )
