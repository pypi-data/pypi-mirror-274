def a_2_3():

    print("""
    
def viterbi_decode(emissions, mask, trans, start_trans, end_trans):
    # emissions: (seq_length, batch_size, num_tags)
    # mask: (seq_length, batch_size)

    seq_length = mask.shape[0]

    score = start_trans + emissions[0]
    history = ()

    for i in range(1, seq_length):
        broadcast_score = score.expand_dims(2)
        broadcast_emission = emissions[i].expand_dims(1)
        next_score = broadcast_score + trans + broadcast_emission

        # Obtain the label with the maximum score corresponding to the current token and save the label.
        indices = next_score.argmax(axis=1)
        history += (indices,)

        next_score = next_score.max(axis=1)
        score = mnp.where(mask[i].expand_dims(1), next_score, score)

    score += end_trans

    return score, history

def post_decode(score, history, seq_length):
    # Use Score and History to calculate the optimal prediction sequence.
    batch_size = seq_length.shape[0]
    seq_ends = seq_length - 1
    # shape: (batch_size,)
    best_tags_list = []

    # Decode each sample in a batch in sequence.
    for idx in range(batch_size):
        # Search for the label that maximizes the prediction probability corresponding to the last token.
        # Add it to the list of best prediction sequence stores.
        best_last_tag = score[idx].argmax(axis=0)
        best_tags = [int(best_last_tag.asnumpy())]

        # Repeatedly search for the label with the maximum prediction probability corresponding to each token and add the label to the list.
        for hist in reversed(history[:seq_ends[idx]]):
            best_last_tag = hist[idx][best_tags[-1]]
            best_tags.append(int(best_last_tag.asnumpy()))

        # Reset the solved label sequence in reverse order to the positive sequence.
        best_tags.reverse()
        best_tags_list.append(best_tags)

    return best_tags_list




import mindspore as ms
import mindspore.nn as nn
import mindspore.ops as ops
import mindspore.numpy as mnp
from mindspore.common.initializer import initializer, Uniform

def sequence_mask(seq_length, max_length, batch_first=False):
    ###Generate the mask matrix based on the actual length and maximum length of the sequence.###
    range_vector = mnp.arange(0, max_length, 1, seq_length.dtype)
    result = range_vector < seq_length.view(seq_length.shape + (1,))
    if batch_first:
        return result.astype(ms.int64)
    return result.astype(ms.int64).swapaxes(0, 1)

class CRF(nn.Cell):
    def __init__(self, num_tags: int, batch_first: bool = False, reduction: str = 'sum') -> None:
        if num_tags <= 0:
            raise ValueError(f'invalid number of tags: {num_tags}')
        super().__init__()
        if reduction not in ('none', 'sum', 'mean', 'token_mean'):
            raise ValueError(f'invalid reduction: {reduction}')
        self.num_tags = num_tags
        self.batch_first = batch_first
        self.reduction = reduction
        self.start_transitions = ms.Parameter(initializer(Uniform(0.1), (num_tags,)), name='start_transitions')
        self.end_transitions = ms.Parameter(initializer(Uniform(0.1), (num_tags,)), name='end_transitions')
        self.transitions = ms.Parameter(initializer(Uniform(0.1), (num_tags, num_tags)), name='transitions')

    def construct(self, emissions, tags=None, seq_length=None):
        if tags is None:
            return self._decode(emissions, seq_length)
        return self._forward(emissions, tags, seq_length)

    def _forward(self, emissions, tags=None, seq_length=None):
        if self.batch_first:
            batch_size, max_length = tags.shape
            emissions = emissions.swapaxes(0, 1)
            tags = tags.swapaxes(0, 1)
        else:
            max_length, batch_size = tags.shape

        if seq_length is None:
            seq_length = mnp.full((batch_size,), max_length, ms.int64)

        mask = sequence_mask(seq_length, max_length)

        # shape: (batch_size,)
        numerator = compute_score(emissions, tags, seq_length-1, mask, self.transitions, self.start_transitions, self.end_transitions)
        # shape: (batch_size,)
        denominator = compute_normalizer(emissions, mask, self.transitions, self.start_transitions, self.end_transitions)
        # shape: (batch_size,)
        llh = denominator - numerator

        if self.reduction == 'none':
            return llh
        if self.reduction == 'sum':
            return llh.sum()
        if self.reduction == 'mean':
            return llh.mean()
        return llh.sum() / mask.astype(emissions.dtype).sum()

    def _decode(self, emissions, seq_length=None):
        if self.batch_first:
            batch_size, max_length = emissions.shape[:2]
            emissions = emissions.swapaxes(0, 1)
        else:
            batch_size, max_length = emissions.shape[:2]

        if seq_length is None:
            seq_length = mnp.full((batch_size,), max_length, ms.int64)

        mask = sequence_mask(seq_length, max_length)

        return viterbi_decode(emissions, mask, self.transitions, self.start_transitions, self.end_transitions)
    
    """)