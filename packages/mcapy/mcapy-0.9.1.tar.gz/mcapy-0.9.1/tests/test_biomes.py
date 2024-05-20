from pytest import mark
from mca import Biome, Chunk, EmptyChunk, EmptyRegion, Block, Region


def test_basic_biome():
    blocks = ['stone', 'dirt', 'grass', 'water']
    biomes = ['plains', 'desert', 'mountains', 'ocean']

    region = EmptyRegion(0, 0)

    chunk = EmptyChunk(0, 0)
    for i in range(4):
        chunk.set_block(Block(blocks[i]), i, 0, 0)
        chunk.set_biome(Biome(biomes[i]), 0, i * 4, 0)

    region.add_chunk(Chunk(chunk.save()))
    #region.add_chunk(Chunk(empty_chunk.save()))

    region = Region(region.save())

    #for i in range(2):
    #    chunk = region.get_chunk(i, 0)
    #    for i, color in enumerate(colors):
    #        assert chunk.get_block(i, 0, 0).id == color
    chunk2 = region.get_chunk(0, 0)
    for i in range(4):
        assert chunk2.get_block(i, 0, 0).id == blocks[i]
        # TODO: get_biome doesn't work yet
        # assert chunk2.get_biome(0, i * 4, 0).id == biomes[i]
