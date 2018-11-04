def extract_vocab():
    with open('sampleTrain.vocab.txt') as f:
        words = f.read().splitlines()
        return {word: index for index, word in enumerate(words)}


def read_samples(path):
    with open(path) as f:
        samples = []
        string_samples = f.read().splitlines()

        for sample in string_samples:
            sample = sample.strip()
            sample_elements = sample.split('\t')
            document_id = sample_elements[0]
            real_class = int(sample_elements[1])
            words = sample_elements[2].split(' ')
            samples.append((document_id, real_class, words))
        return samples


def train_model(word_2_num):
    prior_probabilities = {}
    word_likelihoods_per_class = {}
    samples = read_samples('sampleTrain.txt')

    for sample in samples:
        prior_probabilities[sample[1]] = prior_probabilities.get(sample[1], 0.0) + 1.0
        word_likelihoods = word_likelihoods_per_class.setdefault(sample[1], {})
        for word in sample[2]:
            word_likelihoods[word_2_num[word]] = word_likelihoods.get(word_2_num[word], 0.0) + 1.0
    number_of_documents = sum(prior_probabilities.values())

    for class_index in prior_probabilities:
        prior_probabilities[class_index] /= number_of_documents

    for class_index in word_likelihoods_per_class:
        word_likelihoods = word_likelihoods_per_class[class_index]
        per_class_words = sum(word_likelihoods.values())

        for word_num in word_2_num.values():
            word_likelihoods[word_num] = (1.0 + word_likelihoods.get(word_num, 0.0)) / (
                    per_class_words + float(len(word_2_num)))
    return prior_probabilities, word_likelihoods_per_class


def classify(sample_words, word2num, prior_probabilities, word_likelihoods_per_class):
    class_aposteriori_probabilities = {}
    for class_index in prior_probabilities:
        class_probability = prior_probabilities[class_index]
        word_likelihoods = word_likelihoods_per_class[class_index]
        for sample_word in sample_words:
            class_probability *= word_likelihoods[word2num[sample_word]]
        class_aposteriori_probabilities[class_index] = class_probability

    total_sample_probability = sum(class_aposteriori_probabilities.values())

    for class_index in prior_probabilities:
        class_aposteriori_probabilities[class_index] /= total_sample_probability

    sorted_classes = sorted(class_aposteriori_probabilities.keys(), key=class_aposteriori_probabilities.get)
    return sorted_classes[-1]


def evaluate(path, word_2_num, prior_probabilities, word_likelihoods_per_class):
    samples = read_samples('sampleTest.txt')
    accuracy = 0.0
    print('Predictions on test data')

    for sample in samples:
        predicted_class = classify(sample[2], word_2_num, prior_probabilities, word_likelihoods_per_class)
        print('{} = {}'.format(sample[0], predicted_class))
        if predicted_class == sample[1]:
            accuracy += 1
    accuracy = accuracy * 100 / len(samples)
    print()
    print("Accuracy on test data = {}%".format(accuracy))


if __name__ == '__main__':
    word_2_num = extract_vocab()
    prior_probabilities, word_likelihoods_per_class = train_model(word_2_num)
    print('Prior probabilities')
    for class_index in prior_probabilities:
        print('class {} = {}'.format(class_index, prior_probabilities[class_index]))
    print()

    print('Feature likelihoods')
    words = sorted(word_2_num.keys())
    col_width = max(map(len, words)) + 5
    print(' ' * len('class 0   '), end='')
    for word in words:
        print(' ' * (col_width - len(word)), word, end=' ')
    print()
    for class_index in sorted(word_likelihoods_per_class.keys()):
        word_likelihoods = word_likelihoods_per_class[class_index]
        print('class {}'.format(class_index, ''), end=' ' * 3)
        for word in words:
            format_string = ' ' * (col_width - 7) + '{:.6f}'
            print(format_string.format(word_likelihoods.get(word_2_num[word], 0.0)), end=' ')
        print()
    print()

    evaluate('sampleTest.txt', word_2_num, prior_probabilities, word_likelihoods_per_class)
