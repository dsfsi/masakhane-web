- should not put the model in a docker container, use the file storage instead and make it available as a volume to the container
- use a model registry to store models, build one with mlflow.
- Run different services for each model, and use a load balancer to route the requests to the right model.



torch-model-archiver --model-name MasaknaneEnSwaRelNews \
--version 1.0 \
--serialized-file src/torchserve/transformer_models/masakhane/m2m100_418M_en_swa_rel_news/pytorch_model.bin \
--handler src/torchserve/transformer_handler.py \
--extra-files "src/torchserve/transformer_models/masakhane/m2m100_418M_en_swa_rel_news/config.json,
               src/torchserve/transformer_models/masakhane/m2m100_418M_en_swa_rel_news/special_tokens_map.json,
               src/torchserve/transformer_models/masakhane/m2m100_418M_en_swa_rel_news/tokenizer_config.json,
               src/torchserve/transformer_models/masakhane/m2m100_418M_en_swa_rel_news/vocab.json,
               src/torchserve/transformer_models/masakhane/m2m100_418M_en_swa_rel_news/generation_config.json,
               src/torchserve/transformer_models/masakhane/m2m100_418M_en_swa_rel_news/sentencepiece.bpe.model"   
