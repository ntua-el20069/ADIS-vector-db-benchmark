# Benchmark results - Qdrant & Milvus comparison

## Milvus

### upload constants
- `parallel`: `16`
- `index_params`: the `M` and `efConstruction` specified by the experiment

### search parameters
| **Search** | **parallel** | **ef** |
|------------|--------------|--------|
| **search-0** | 1 | 128 |
| **search-1** | 1 | 256 |
| **search-2** | 1 | 512 |
| **search-3** | 100 | 128 |
| **search-4** | 100 | 256 |
| **search-5** | 100 | 512 |

## Qdrant

### upload constants
- `parallel`: `16`
- `optimizers_config` : `memmap_threshold` is set to `10000000`
- `hnsw_config`: the `m` and `ef_construct` specified by the experiment

### search
| **Search** | **parallel** | **hnsw_ef** |
|------------|--------------|--------|
| **search-0** | 1 | 64 |
| **search-1** | 1 | 128 |
| **search-2** | 1 | 256 |
| **search-3** | 1 | 512 |
| **search-4** | 100 | 64 |
| **search-5** | 100 | 128 |
| **search-6** | 100 | 256 |
| **search-7** | 100 | 512 |

