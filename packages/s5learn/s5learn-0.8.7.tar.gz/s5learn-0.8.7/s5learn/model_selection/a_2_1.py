def a_2_1():


    print("""
    
def compute_score(emissions, tags, seq_ends, mask, trans, start_trans, end_trans):
    # emissions: (seq_length, batch_size, num_tags)
    # tags: (seq_length, batch_size)
    # mask: (seq_length, batch_size)

    seq_length, batch_size = tags.shape
    mask = mask.astype(emissions.dtype)

    # Set score to the initial transition probability.
    # shape: (batch_size,)
    score = start_trans[tags[0]]
    # score += Probability of the first emission
    # shape: (batch_size,)
    score += emissions[0, mnp.arange(batch_size), tags[0]]

    for i in range(1, seq_length):
        # Probability that the label is transited from i-1 to i (valid when mask == 1).
        # shape: (batch_size,)
        score += trans[tags[i - 1], tags[i]] * mask[i]

        # Emission probability of tags[i] prediction(valid when mask == 1).
        # shape: (batch_size,)
        score += emissions[i, mnp.arange(batch_size), tags[i]] * mask[i]

    # End the transition.
    # shape: (batch_size,)
    last_tags = tags[seq_ends, mnp.arange(batch_size)]
    # score += End transition probability
    # shape: (batch_size,)
    score += end_trans[last_tags]

    return score
    
    """)