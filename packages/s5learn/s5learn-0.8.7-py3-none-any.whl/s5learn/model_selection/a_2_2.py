def a_2_2():


    print("""
    
def compute_normalizer(emissions, mask, trans, start_trans, end_trans):
    # emissions: (seq_length, batch_size, num_tags)
    # mask: (seq_length, batch_size)

    seq_length = emissions.shape[0]

    # Set score to the initial transition probability and add the first emission probability.
    # shape: (batch_size, num_tags)
    score = start_trans + emissions[0]

    for i in range(1, seq_length):
        # The score dimension is extended to calculate the total score.
        # shape: (batch_size, num_tags, 1)
        broadcast_score = score.expand_dims(2)

        # The emission dimension is extended to calculate the total score.
        # shape: (batch_size, 1, num_tags)
        broadcast_emissions = emissions[i].expand_dims(1)

        # Calculate score_i according to formula (7).
        # In this case, broadcast_score indicates all possible paths from token 0 to the current token.
        # log_sum_exp corresponding to score
        # shape: (batch_size, num_tags, num_tags)
        next_score = broadcast_score + trans + broadcast_emissions

        # Perform the log_sum_exp operation on score_i to calculate the score of the next token.
        # shape: (batch_size, num_tags)
        next_score = ops.logsumexp(next_score, axis=1)

        # The score changes only when mask == 1.
        # shape: (batch_size, num_tags)
        score = mnp.where(mask[i].expand_dims(1), next_score, score)

    # Add the end transition probability.
    # shape: (batch_size, num_tags)
    score += end_trans
    # Calculate log_sum_exp based on the scores of all possible paths.
    # shape: (batch_size,)
    return ops.logsumexp(score, axis=1)
    
    """)