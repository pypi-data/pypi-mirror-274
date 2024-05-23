def ab_1_4():


    print("""
    
def prepare_sequence(seqs, word_to_idx, tag_to_idx):
    seq_outputs, label_outputs, seq_length = [], [], []
    max_len = max([len(i[0]) for i in seqs]) # 10  #

    for seq, tag in seqs:
        seq_length.append(len(seq))
        idxs = [word_to_idx[w] for w in seq]
        labels = [tag_to_idx[t] for t in tag]
        
        idxs.extend([word_to_idx['<pad>'] for i in range(max_len - len(seq))])
        labels.extend([tag_to_idx['O'] for i in range(max_len - len(seq))])
        seq_outputs.append(idxs)
        label_outputs.append(labels)

    return ms.Tensor(seq_outputs, ms.int64), \
            ms.Tensor(label_outputs, ms.int64), \
            ms.Tensor(seq_length, ms.int64)


data, label, seq_length = prepare_sequence([(x,y) for (x,y) in zip(a,b)], word_to_idx, tag_to_idx)
data.shape, label.shape, seq_length.shape
    
    """)