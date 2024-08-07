from os.path import join

from sentence_transformers import SentenceTransformer
from tqdm import tqdm

from api.my import MyAPI
from core.utils_npz import NpzUtils
from e_pairs.api_fcp import FcpApi
from e_pairs.cfg_hla import HlaExperimentConfig
from e_pairs.cfg_spectrum import SpectrumConfig
from e_pairs.hla_models.spectrum.presets import PROMPT_PRESETS
from utils import CACHE_DIR, DATA_DIR


if __name__ == '__main__':

    fcp_api = FcpApi(personalities_path=join(DATA_DIR, "personalities.txt"))
    spectrum_cfg = SpectrumConfig()
    hla_cfg = HlaExperimentConfig(books_storage=MyAPI.books_storage)
    model = SentenceTransformer(spectrum_cfg.embedding_model_name, cache_folder=CACHE_DIR)

    X_norm = NpzUtils.load(spectrum_cfg.features_norm)
    X_diff = NpzUtils.load(spectrum_cfg.features_diff)
    preset = hla_cfg.hla_spectrum_preset
    prompts, _ = PROMPT_PRESETS[preset](X_norm, X_diff, fcp_api)

    desc = "Calculate sentence embedding [{m}-{p}]".format(
        m=spectrum_cfg.embedding_model_name, p=preset)

    X_st = []
    for prompt in tqdm(prompts, desc=desc):
        X_st.append(model.encode(prompt))

    # Save the result.
    target = spectrum_cfg.st_embeddings.format(preset=preset)
    NpzUtils.save(data=X_st, target=target)
    print(f"Saved: {target}")
