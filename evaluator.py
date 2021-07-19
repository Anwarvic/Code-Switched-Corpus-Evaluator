# from tqdm import tqdm
from collections import Counter

class Evaluator:

    def is_code_switched(self, tags, exclude_tags):
        """
        Checks if the given utterance is code-switched or not. An utterance is
        code-switched if it contains more than one language excluding the
        language-independent tag.

        Parameters
        ----------
        tags : list
            List of language tags in an utterance.
        exclude_tags : set
            A set of language-independent tags to exclude.
        
        Returns
        -------
        bool:
            True if the utterance is code-switched, False if not.
        """
        return len(set(tags) - exclude_tags) > 1
        
    def _count_alternations(self, tags, exclude_tags):
        """
        Counts the number of alternations between tags in an utterance
        excluding the exclude_tags.

        Parameters
        ----------
        tags : list
            List of language tags in an utterance.
        exclude_tags : set
            A set of language-independent tags to exclude.
        
        Returns
        -------
        alternations_count : int
            Number of alternations between tags excluding the exclude_tags.
        
        Examples
        --------
        >>> self._count_alternations(['O', 'O', 'O', 'O', 'O'], {'O'})
        0
        >>> self._count_alternations(['ar', 'ar', 'O', 'en', 'ar'], {'O'})
        2
        """
        alts = 0
        i = 0
        prev_tag = tags[i]
        while(i < len(tags) and prev_tag in exclude_tags):
            prev_tag = tags[i]
            i += 1
        # count alternations
        for tag in tags[i:]:
            if tag in exclude_tags:
                continue
            if tag != prev_tag:
                alts += 1
            prev_tag = tag
        return alts

    def _count_matrix_tokens(self, tags, exclude_tags):
        """
        Counts the number of tokens in the matrix language of an utterance; a
        matrix langauge is the most frequent language in the utterance.

        Parameters
        ----------
        tags : list
            List of language tags in an utterance.
        exclude_tags : set
            A set of language-independent tags to exclude.
        
        Returns
        -------
        matrix_tokens_count : int
            Number of tokens in the matrix language of an utterance.
        
        Examples
        --------
        >>> self._count_matrix_tokens(['O', 'O', 'O', 'O', 'O'], {'O'})
        0
        >>> self._count_matrix_tokens(['ar', 'ar', 'O', 'en', 'ar'], {'O'})
        3
        """
        matrix_tag = ""
        matrix_tokens_count = 0
        for tag, count in Counter(tags).items():
            if tag not in exclude_tags:
                if count > matrix_tokens_count:
                    matrix_tokens_count = count
                    matrix_tag = tag
        return matrix_tag, matrix_tokens_count

    def evaluate_utterance(self, tags, exclude_tags):
        """
        Evaluates the code-switch complexity of an utterance.

        Parameters
        ----------
        tags : list
            List of language tags in an utterance.
        exclude_tags : set
            A set of language-independent tags to exclude.
        
        Returns
        -------
        complexity : float
            Code-switch complexity of an utterance. Given a monolingual
            utterance will result in 0 complexity while a cross-lingual
            utterance will give a value greater than 0. The closer it gets to
            100, the higher the complexity is.
        
        Examples
        --------
        >>> self.evaluate_utterance(['O', 'O', 'O', 'O', 'O'], {'O'})
        0.0
        >>> self.evaluate_utterance(['O', 'ar', 'en', 'fr', 'O', 'de'], {'O'})
        75.0
        >>> self.evaluate_utterance(['ar', 'ar', 'O', 'en', 'ar'], {'O'})
        37.5
        """
        epsilon = 1e-8 # for numerical stability
        tags_counter = Counter(tags)
        _, matrix_tokens_count = self._count_matrix_tokens(tags, exclude_tags)
        number_of_tokens = len(tags) - sum([tags_counter[tag] for tag in exclude_tags])
        alternations_count = self._count_alternations(tags, exclude_tags)
        return 100 * ((number_of_tokens - matrix_tokens_count + alternations_count) / (2 * (number_of_tokens+epsilon)))

    def evaluate_corpus(self, corpus_tags, exclude_tags):
        """
        Evaluates the code-switch complexity of a corpus.

        Parameters
        ----------
        corpus_tags : list[list]
            List of utterances where each utterance is a list of language
            tags in a corpus.
        exclude_tags : str
            The language-independent tag to exclude from the counter.
        
        Returns
        -------
        complexity : float
            The complexity score of a code-switched corpus.
        """
        if len(corpus_tags) == 1:
            return self.evaluate_utterance(corpus_tags[0], exclude_tags)
        else:
            score = 0
            cw_utterances_count = 0 #code-switched utterances
            prev_matrix_tag = None
            for utter_tags in corpus_tags:
                if self.is_code_switched(utter_tags, exclude_tags):
                    cw_utterances_count += 1
                curr_matrix_tag, _ = self._count_matrix_tokens(utter_tags, exclude_tags)
                utter_score = self.evaluate_utterance(utter_tags, exclude_tags) / 50.0
                score += 1 - utter_score + int(prev_matrix_tag != curr_matrix_tag or prev_matrix_tag is None)
                prev_matrix_tag = curr_matrix_tag
            return (100 / len(corpus_tags)) * (0.5 * score + 5/6 * cw_utterances_count)

    def get_stats(self, corpus_utters, exclude_tags):
        tokens = 0
        switched_utters = 0
        for utter_tags in corpus_utters:
            tokens += len(utter_tags)
            if self.is_code_switched(utter_tags, exclude_tags):
                switched_utters += 1
        return tokens, len(corpus_utters), switched_utters


if __name__ == "__main__":
    ev = Evaluator()
    exclude_tags = {"o"}
    tags = ['o', 'o', 'o', 'o']
    assert ev._count_alternations(tags, exclude_tags) == 0
    assert ev.evaluate_utterance(tags, exclude_tags) == 0
    
    tags = ['o', 'ar', 'ar', 'ar']
    assert ev._count_alternations(tags, exclude_tags) == 0
    assert ev.evaluate_utterance(tags, exclude_tags) == 0
    
    tags = ['o', 'ar', 'o', 'ar']
    assert ev._count_alternations(tags, exclude_tags) == 0
    assert ev.evaluate_utterance(tags, exclude_tags) == 0

    tags = ['o', 'ar', 'en', 'o']
    assert ev._count_alternations(tags, exclude_tags) == 1
    assert round(ev.evaluate_utterance(tags, exclude_tags)) == 50

    tags = ['o', 'ar', 'en', 'ar']
    assert ev._count_alternations(tags, exclude_tags) == 2
    assert round(ev.evaluate_utterance(tags, exclude_tags)) == 50

    tags = ['o', 'ar', 'en', 'ar', 'o', 'ar']
    assert ev._count_alternations(tags, exclude_tags) == 2
    assert round(ev.evaluate_utterance(tags, exclude_tags), 1) == 37.5

    tags = ['o', 'ar', 'ar', 'o', 'en', 'ar']
    assert ev._count_alternations(tags, exclude_tags) == 2
    assert round(ev.evaluate_utterance(tags, exclude_tags), 1) == 37.5

    tags = ['o', 'ar', 'en', 'fr', 'o', 'de']
    assert ev._count_alternations(tags, exclude_tags) == 3
    assert round(ev.evaluate_utterance(tags, exclude_tags), 1) == 75
